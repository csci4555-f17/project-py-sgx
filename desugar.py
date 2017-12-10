from explicate_ast import *
from allocator import allocate

def _desugar_stmts(stmts):
    # type: (Stmt) -> Stmt

    def _desugar_stmt(stmt):
        # type: (Node) -> Node

        if isinstance(stmt, If):
            def elif_to_else_if(l, else_):
                # type: ([(Node, Stmt)], Stmt) -> Stmt
                """
                This function is a helper to turn an `If` (which has a list of
                `elif`s) into an `IfStmt` (which only uses recursive if: ... else: ...
                """
                if len(l) == 0:
                    if else_ is None:
                        else_ = Stmt([])
                    return _desugar_stmts(else_)
                else:
                    test, then_ = l[0]
                    return Stmt([IfStmt(
                        _desugar_expr(test),
                        _desugar_stmts(then_),
                        elif_to_else_if(l[1:], else_)
                    )])
            if_else = elif_to_else_if(stmt.tests, stmt.else_)
            assert len(if_else.nodes) == 1
            return if_else.nodes[0]

        elif isinstance(stmt, While):
            assert stmt.else_ is None
            return While(
                _desugar_expr(stmt.test),
                Stmt(map(_desugar_stmt, stmt.body)),
                None
            )

        elif isinstance(stmt, Assign):
            assert len(stmt.nodes) == 1
            node = stmt.nodes[0]
            rhs = _desugar_expr(stmt.expr)
            if isinstance(node, Subscript):
                container = _desugar_expr(node.expr)
                assert len(node.subs) == 1
                [sub] = node.subs
                sub = _desugar_expr(sub)
                return Discard(CallFunc(Name("set_subscript"), [container, sub, rhs]))
            else:
                assert isinstance(node, AssName)
                name = Name(node.name)
                return Assign([name], rhs)

        elif isinstance(stmt, Discard):
            expr = _desugar_expr(stmt.expr)
            return Discard(expr)

        elif isinstance(stmt, Printnl):
            assert len(stmt.nodes) == 1
            expr = _desugar_expr(stmt.nodes[0])
            return Printnl([expr], stmt.dest)

        else:
            raise TypeError("Inexhaustive pattern match.", stmt)

    return Stmt(map(_desugar_stmt, stmts.nodes))


def _desugar_expr(expr):
    # type: (Node) -> Node

    if isinstance(expr, Add):
        left = _desugar_expr(expr.left)
        right = _desugar_expr(expr.right)
        return Add((left, right))

    elif isinstance(expr, UnarySub):
        return UnarySub(_desugar_expr(expr.expr))

    elif isinstance(expr, CallFunc):
        return CallFunc(_desugar_expr(expr.node), map(_desugar_expr, expr.args))

    elif isinstance(expr, Compare):
        if len(expr.ops) != 1:
            raise ValueError("Compare operator used with more than two operands.", expr)

        left = _desugar_expr(expr.expr)
        right = _desugar_expr(expr.ops[0][1])

        comparator = expr.ops[0][0]
        if comparator == "==":
            comp = Eq
        elif comparator == "!=":
            comp = NEq
        elif comparator == "is":
            comp = Is
        else:
            raise ValueError("Passed a comparator that is not yet handled.", expr)

        return comp((left, right))

    elif isinstance(expr, IfExp):
        test = _desugar_expr(expr.test)
        then = _desugar_expr(expr.then)
        else_ = _desugar_expr(expr.else_)
        return IfExp(test, then, else_)

    elif isinstance(expr, And):
        assert len(expr.nodes) == 2, "And with more than 2 nodes"
        left = _desugar_expr(expr.nodes[0])
        right = _desugar_expr(expr.nodes[1])
        left_name = allocate()
        # Desugar to if-expression since it short circuits
        return Let(left_name.name, left, IfExp(
            left_name,
            right,
            left_name
        ))

    elif isinstance(expr, Not):
        not_expr = _desugar_expr(expr.expr)
        # Desugar to if-expression since it short circuits
        return IfExp(
            not_expr,
            Const(0),
            Const(1)
        )

    elif isinstance(expr, Or):
        assert len(expr.nodes) == 2, "Or with more than 2 nodes"
        left = _desugar_expr(expr.nodes[0])
        right = _desugar_expr(expr.nodes[1])
        left_name = allocate()
        # Desugar to if-expression since it short circuits
        return Let(left_name.name, left, IfExp(
            left_name,
            left_name,
            right
        ))

    elif isinstance(expr, List):
        nodes = expr.nodes
        num_nodes = len(nodes)

        l_name = allocate()
        def fill_list(i, nodes):
            if len(nodes) == 0:
                return l_name
            else:
                return Seq((
                    CallFunc(Name("set_subscript"), [l_name, Const(i), _desugar_expr(nodes[0])]),
                    fill_list(i + 1, nodes[1:])
                ))
        l = Let(l_name.name, CallFunc(Name("create_list"), [Const(num_nodes)]), fill_list(0, nodes))
        return l

    elif isinstance(expr, Dict):
        pairs = expr.items

        d_name = allocate()
        def fill_dict(pairs):
            if len(pairs) == 0:
                return d_name
            else:
                sub, data = pairs[0]
                return Seq((
                    CallFunc(Name("set_subscript"), [d_name, _desugar_expr(sub), _desugar_expr(data)]),
                    fill_dict(pairs[1:])
                ))
        d = Let(d_name.name, CallFunc(Name("create_dict"), []), fill_dict(pairs))
        return d

    # Base cases
    elif isinstance(expr, Const):
        return expr

    elif isinstance(expr, Name):
        if expr.name == "True":
            return Const(1)
        elif expr.name == "False":
            return Const(0)
        else:
            return expr

    elif isinstance(expr, Subscript):
        container = _desugar_expr(expr.expr)
        assert len(expr.subs) == 1
        [sub] = expr.subs
        sub = _desugar_expr(sub)
        return CallFunc(Name("get_subscript"), [container, sub])

    else:
        raise TypeError("Inexhaustive pattern match.", expr)


def desugar(ast):
    # type: (Module) -> Module

    if not isinstance(ast, Module) or not isinstance(ast.node, Stmt):
        raise TypeError("Could not Desugar improperly formatted AST (expected "
                        "top level structure to match Module(Stmt([...]))")
    else:
        return Module(ast.doc, _desugar_stmts(ast.node))
