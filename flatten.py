from compiler.ast import *
from typing import *


class VariableAllocator:
	"""
	A namespace to unify all actions and variables
	"""
	__temp_vars = 0
	__freed = []

	class InternalName(Name):
		"""
		Behaves exactly like Name, but allows distinction between temp vars
		allocated internally by the flattener and those allocated explicitly by
		the program, so we only free locally allocated vars
		"""
		pass

	@staticmethod
	def allocate():
		# type: () -> Name
		try:
			return VariableAllocator.__freed.pop()
		except IndexError:
			VariableAllocator.__temp_vars += 1
			# Hash (#) added so no conflicts can arise with program names
			return VariableAllocator.InternalName("#PYYC_FLATTEN_TEMP_" + str(VariableAllocator.__temp_vars))

	@staticmethod
	def free(name):
		return
		# type: (Node) -> ()
		if isinstance(name, VariableAllocator.InternalName):
			VariableAllocator.__freed.append(name)


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
		map(VariableAllocator.free, nodes)
		return flattened + [Printnl(nodes, stmt.dest)]

	elif isinstance(stmt, Assign):
		for node in stmt.nodes:
			if not isinstance(node, AssName):
				raise TypeError("Cannot assign value to non-name Node.")
		# Flatten the expr, then bind it to a temp name once so it is not
		# run again for each binding.
		flattened, expr_name = _flatten_expr(stmt.expr, True)
		# Bind to the temp name
		VariableAllocator.free(expr_name)
		return flattened + [_assignment(node.name, expr_name) for node in stmt.nodes]

	elif isinstance(stmt, Discard):
		flattened, _ = _flatten_expr(stmt.expr, False)
		return flattened

	else:
		raise TypeError("Inexhaustive pattern match.", stmt)


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

	def do_save(flattened, res, name = None):
		if save:
			if name is None:
				name = VariableAllocator.allocate()
			return flattened + [_assignment(name.name, res)], name
		else:
			return flattened + [Discard(res)], None

	if isinstance(expr, Add):
		flattened, [left_name, right_name] = _flatten_and_sequence([expr.left, expr.right])

		# this temp Var is so that the add maps more closely to the x86 addl
		# instruction. Specifically, this ensures that it has the form `x = ? + x`
		name = VariableAllocator.allocate()
		flattened += [_assignment(name.name, right_name)]

		res = Add((left_name, name))
		VariableAllocator.free(left_name)
		VariableAllocator.free(right_name)
		VariableAllocator.free(name)
		return do_save(flattened, res, name)

	elif isinstance(expr, UnarySub):
		flattened, [name] = _flatten_and_sequence([expr.expr])
		res = UnarySub(name)
		VariableAllocator.free(name)
		return do_save(flattened, res)

	elif isinstance(expr, CallFunc):
		flattened_arg_ops, args = _flatten_and_sequence(expr.args)
		flattened_func, [func_name] = _flatten_and_sequence([expr.node])
		# Sequence the evaluation of the expression to get the function
		# before the steps to get the args.
		# type: List[Node]
		flattened = flattened_func + flattened_arg_ops
		res = CallFunc(func_name, args)
		map(VariableAllocator.free, args)
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
						"top level structure to match Module(Stmt([...]))")

	ast_acc = []
	for node in ast.node.nodes:
		flattened = _flatten_stmt(node)
		ast_acc = ast_acc + flattened

	return Module(ast.doc, Stmt(ast_acc))
