from compiler.ast import *


int_tag  = Const(0b00)
bool_tag = Const(0b01)
big_tag  = Const(0b11)


#
# Expressions
#

class GetTag(Node):
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.arg))


class Box(Node):
    """
    InjectFrom
    """
    def __init__(self, type, arg):
        # type = "int" | "bool" | "big"
        self.type = type
        self.arg = arg

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.type), repr(self.arg))

class UnBox(Node):
    """
    ProjectTo
    """
    def __init__(self, type, arg):
        # type = "small" | "big"
        self.type = type
        self.arg = arg

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.type), repr(self.arg))


class Let(Node):
    def __init__(self, var, rhs, body):
        # type: (str, Node, Node) -> ()
        self.var = var
        self.rhs = rhs
        self.body = body

    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__, repr(self.var), repr(self.rhs), repr(self.body))


class Bop(Node):
    def __init__(self, leftright):
        left, right = leftright
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.left), repr(self.right))


class Eq(Bop):
    pass


class NEq(Bop):
    pass


class Is(Bop):
    pass


class Seq(Bop):
    pass


#
# Statements
#

class IfStmt(Node):
    def __init__(self, test, then_, else_):
        # type: (Node, Stmt, Stmt) -> ()
        self.test = test
        self.then_ = then_
        self.else_ = else_

    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__, repr(self.test), repr(self.then_), repr(self.else_))
