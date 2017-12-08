from explicate_ast import *
from typing import *
from allocator import *


def _assignment(name, expr):
	# type: (str, Node) -> Assign
	return Assign([Name(name)], expr)


def _sequence(list_of_lists):
	# type: (List[List[TypeVar["T"]]]) -> List[TypeVar["T"]]
	"""
	[[a], [b, c]] -> [a, b, c]
	"""
	return [item for list in list_of_lists for item in list]


def _flatten_and_sequence(exprs):
	# type: (List[Node]) -> (List[Node], List[Union[Const, Name]])
	"""
	Recursive helper when multiple sub-expressions need to be flattened, like
	in a function call.
	"""

	# Flatten
	flattened_exprs = map(lambda expr: _flatten_expr(expr, True), exprs)  # type: List[(List[Node], Union[Const, Name])]

	# Get a list of the saved results
	non_recursive_res = map(lambda pair: pair[1], flattened_exprs)  # type: List[Union[Const, Name]]

	# Get a list of lists of operations to perform to get each expr by name or
	# value
	flattened = _sequence(map(lambda pair: pair[0], flattened_exprs))  # type: List[Node]

	return flattened, non_recursive_res


def _flatten_stmt(stmt):
	# type: (Node) -> List[Node]
	"""
	Top level flattener, calls the recursive expression flattener on top level
	sub-expressions
	"""
	if isinstance(stmt, Printnl):
		flattened, nodes = _flatten_and_sequence(stmt.nodes)
		return flattened + [Printnl(nodes, stmt.dest)]

	elif isinstance(stmt, Assign):
		for node in stmt.nodes:
			if not isinstance(node, Name):
				raise TypeError("Cannot assign value to non-name Node.", node)
		# Flatten the expr, then bind it to a temp name once so it is not
		# run again for each binding.
		flattened, expr_name = _flatten_expr(stmt.expr, True)
		# Bind to the temp name
		return flattened + [_assignment(node.name, expr_name) for node in stmt.nodes]

	elif isinstance(stmt, Discard):
		flattened, _ = _flatten_expr(stmt.expr, False)
		return flattened

	elif isinstance(stmt, IfStmt):
		flattened_test, test_name = _flatten_expr(stmt.test, True)
		return flattened_test + [
			IfStmt(
				test_name,
				Stmt(_flatten_stmts(stmt.then_.nodes)),
				Stmt(_flatten_stmts(stmt.else_.nodes))
			)
		]

	elif isinstance(stmt, If):
		raise TypeError("If class should be removed by explicate", stmt)

	else:
		raise TypeError("Inexhaustive pattern match.", stmt)


def _flatten_stmts(stmts):
	# type: ([Node]) -> [Node]
	stmts_acc = []
	for stmt in stmts:
		flattened = _flatten_stmt(stmt)
		stmts_acc += flattened
	return stmts_acc


def _flatten_expr(expr, save):
	# type: (Node) -> (List[Node], Union[Const, Name, None])
	"""
	Recursively sequences assignments to create an equivalent program to the
	expr given. Returns the sequence as a list paired with the `Node` representing
	the result type (currently `Const` or `Name` when `save` is `True`. The result
	is passed back as `None` if `save` is `False`.
	:param save: True if the result should be saved to an `Assign`, False if it
				 should be discarded (with None returned for the result). The
				 list is still returned if save is False.
	:return: The list of operations that are equivalent to the given ast
	"""

	def do_save(flattened, res, name=None):
		if save:
			if name is None:
				name = allocate()
			return flattened + [_assignment(name.name, res)], name
		else:
			return flattened + [Discard(res)], None

	if isinstance(expr, Add):
		flattened, [left_name, right_name] = _flatten_and_sequence([expr.left, expr.right])

		# this temp Var is so that the add maps more closely to the x86 addl
		# instruction. Specifically, this ensures that it has the form `x = ? + x`
		name = allocate()
		flattened += [_assignment(name.name, right_name)]

		res = Add((left_name, name))
		return do_save(flattened, res, name)

	elif isinstance(expr, UnarySub):
		flattened, [name] = _flatten_and_sequence([expr.expr])
		res = UnarySub(name)
		return do_save(flattened, res)

	elif isinstance(expr, CallFunc):
		flattened_arg_ops, args = _flatten_and_sequence(expr.args)
		flattened_func, [func_name] = _flatten_and_sequence([expr.node])
		# Sequence the evaluation of the expression to get the function
		# before the steps to get the args.
		# type: List[Node]
		flattened = flattened_func + flattened_arg_ops
		res = CallFunc(func_name, args)
		return do_save(flattened, res)

	elif isinstance(expr, Bop):
		flattened, [left_name, right_name] = _flatten_and_sequence([expr.left, expr.right])

		# this temp Var is so that the add maps more closely to the x86 addl
		# instruction. Specifically, this ensures that it has the form `x = ? + x`
		name = allocate()
		flattened += [_assignment(name.name, right_name)]

		# Special Bop for internal use only
		if isinstance(expr, Seq):
			res = name
		else:
			res = expr.__class__((left_name, name))
		return do_save(flattened, res, name)

	elif isinstance(expr, IfExp):
		flattened_test, [test_name] = _flatten_and_sequence([expr.test])
		flattened_then_, [then_name] = _flatten_and_sequence([expr.then])
		flattened_else_, [else_name] = _flatten_and_sequence([expr.else_])

		name = allocate()
		# Assign the result in the left and right to `name`
		flattened = flattened_test + [IfStmt(
			test_name,
			Stmt(flattened_then_ + [_assignment(name.name, then_name)]),
			Stmt(flattened_else_ + [_assignment(name.name, else_name)])
		)]
		return flattened, name

	elif isinstance(expr, Let):
		flattened_rhs, rhs_name = _flatten_expr(expr.rhs, True)
		flattened = flattened_rhs + [_assignment(expr.var, rhs_name)]
		flattened_body, body_name = _flatten_expr(expr.body, True)
		flattened += flattened_body
		return flattened, body_name

	elif isinstance(expr, GetTag):
		flattened, name = _flatten_expr(expr.arg, True)
		res = GetTag(name)
		return do_save(flattened, res)

	elif isinstance(expr, Box):
		flattened, name = _flatten_expr(expr.arg, True)
		res = Box(expr.type, name)
		return do_save(flattened, res)

	elif isinstance(expr, UnBox):
		flattened, name = _flatten_expr(expr.arg, True)
		res = UnBox(expr.type, name)
		return do_save(flattened, res)

	# Base cases
	elif isinstance(expr, Const):
		return [], expr
	elif isinstance(expr, Name):
		return [], expr

	else:
		raise TypeError("Inexhaustive pattern match.", expr)


def flatten(ast):
	# type: (Module) -> Module

	if not isinstance(ast, Module) or not isinstance(ast.node, Stmt):
		raise TypeError("Could not flatten improperly formatted AST (expected "
						"top level structure to match Module(Stmt([...]))", ast)

	return Module(ast.doc, Stmt(_flatten_stmts(ast.node.nodes)))
