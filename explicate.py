from allocator import allocate
from explicate_ast import *


def _int_or_bool(expr_name):
    return IfExp(
        # If int
        Eq((GetTag(expr_name), int_tag)),
        Const(1),
        # If bool
        IfExp(
            Eq((GetTag(expr_name), bool_tag)),
            Const(1),
            Const(0),
        )
    )


def _explicate_stmts(stmts):
    # type: (Stmt) -> Stmt

    def _explicate_stmt(stmt):
        # type: (Node) -> Node

        if isinstance(stmt, IfStmt):
            test = _explicate_expr(stmt.test)
            then_ = _explicate_stmts(stmt.then_)
            else_ = _explicate_stmts(stmt.else_)
            test_name = allocate()
            return Let(
                test_name.name,
                test,
                IfExp(
                    IfExp(
                        _int_or_bool(test_name),
                        UnBox("small", test_name),
                        CallFunc("is_true", [test_name])
                    ),
                    then_,
                    else_
                )
            )

        elif isinstance(stmt, Assign):
            names = map(lambda n: Name(n.name), stmt.nodes)
            rhs = _explicate_expr(stmt.expr)
            return Assign(names, rhs)

        elif isinstance(stmt, Discard):
            expr = stmt.expr
            return Discard(_explicate_expr(expr))

        elif isinstance(stmt, Printnl):
            expr = stmt.nodes[0]
            return Printnl([_explicate_expr(expr)], stmt.dest)

        else:
            raise TypeError("Inexhaustive pattern match.", stmt)

    return Stmt(map(_explicate_stmt, stmts.nodes))


def _explicate_expr(expr):
    # type: (Node) -> Node

    def binary(left, right, box_type, unbox_type, bop, big_func, big_ret_type):
        left_name = allocate()
        right_name = allocate()
        return Let(left_name.name, left, Let(right_name.name, right, IfExp(
            _int_or_bool(left_name),
            Box(
                box_type,
                bop(
                    (
                        UnBox(unbox_type, left_name),
                        UnBox(unbox_type, right_name)
                    )
                )
            ),
            Box(big_ret_type, CallFunc(Name(big_func), [UnBox("big", left_name), UnBox("big", right_name)]))
        )))

    def unary(expr, box_type, unbox_type, uop, big_func, big_ret_type):
        expr_name = allocate()
        return Let(expr_name.name, expr, IfExp(
            # getTag == int or bool
            _int_or_bool(expr_name),
            Box(
                box_type,
                uop(UnBox(unbox_type, expr_name))
            ),
            Box(big_ret_type, CallFunc(Name(big_func), [UnBox("big", expr_name)]))
        ))

    if isinstance(expr, Add):
        left = _explicate_expr(expr.left)
        right = _explicate_expr(expr.right)
        return binary(left, right, "int", "small", Add, "add", "big")

    if isinstance(expr, Bop):
        left = _explicate_expr(expr.left)
        right = _explicate_expr(expr.right)
        # Weird cases
        if isinstance(expr, Is):
            return Box("bool", Eq((left, right)))
        elif isinstance(expr, Seq):
            return Seq((left, right))
        else:
            if isinstance(expr, Eq):
                func = "equal"
            elif isinstance(expr, NEq):
                func = "not_equal"
            else:
                raise TypeError("new Bop that isn't handled on big py obj's")
            return binary(left, right, "bool", "small", expr.__class__, func, "bool")

    elif isinstance(expr, UnarySub):
        return unary(_explicate_expr(expr.expr), "int", "small", UnarySub, "input", "big")  # TODO func

    elif isinstance(expr, CallFunc):
        eplicated_args = map(_explicate_expr, expr.args)
        eplicated_func = CallFunc(expr.node, eplicated_args)
        # Properly box builtins
        if isinstance(eplicated_func.node, Name):
            type = None
            name = eplicated_func.node.name
            if name == "input":
                type = "int"
            elif name == "create_list":
                type = "big"
            elif name == "create_dict":
                type = "big"
            elif name == "set_subscript":
                pass
            elif name == "get_subscript":
                pass
            else:
                raise ValueError("Unhandled builtin", eplicated_func)
            return Box(type, eplicated_func) if type else eplicated_func
        else:
            return eplicated_func

    elif isinstance(expr, IfExp):
        test = _explicate_expr(expr.test)
        then = _explicate_expr(expr.then)
        else_ = _explicate_expr(expr.else_)
        test_name = allocate()
        return Let(
            test_name.name,
            test,
            IfExp(
                IfExp(
                    _int_or_bool(test_name),
                    UnBox("small", test_name),
                    CallFunc(Name("is_true"), [test_name])
                ),
                then,
                else_
            )
        )

    elif isinstance(expr, Let):
        rhs = _explicate_expr(expr.rhs)
        body = _explicate_expr(expr.body)
        return Let(expr.var, rhs, body)

    # Base cases
    elif isinstance(expr, Const):
        if isinstance(expr.value, bool):
            explicated_expr = Const(1) if expr.value else Const(0)
            return Box("bool", explicated_expr)
        elif expr.value is None:
            # Null pointer
            return Box("big", Const(0))
        # So far, could only be int
        else:
            assert isinstance(expr.value, int)
            return Box("int", expr)

    elif isinstance(expr, Name):
        return expr

    else:
        raise TypeError("Inexhaustive pattern match.", expr)


def explicate(ast):
    # type: (Module) -> Module

    if not isinstance(ast, Module) or not isinstance(ast.node, Stmt):
        raise TypeError("Could not flatten improperly formatted AST (expected "
                        "top level structure to match Module(Stmt([...]))")
    else:
        return Module(ast.doc, _explicate_stmts(ast.node))
