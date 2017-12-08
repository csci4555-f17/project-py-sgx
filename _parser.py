# coding=utf-8
from compiler.ast import *

"""
Grammar for P0 implemented by this parser:

module ::= stmts
stmts ::= stmt stmts
        | stmt cmt stmts
        | cmt stmts
        | ε 
stmt ::= expr
       | print expr
       | name "=" expr
expr ::= int
       | "(" expr ")"
       | name
       | "-" expr
       | expr "+" expr
       | "input" "(" ")"
cmt ::= "#" .*
"""


#
# Lexer
#

tokens = (
    "PRINT",
    "NAME",
    "ASSIGN",
    "PLUS",
    "NEG",
    "INT",
    "LPAREN",
    "RPAREN",
    "COMMENT",
    "INPUT"
)

# Unordered tokens
t_ASSIGN = "="
t_PLUS = r"\+"
t_NEG = r"\-"
t_INT = r"\d+"
t_LPAREN = r"\("
t_RPAREN = r"\)"

def t_COMMENT(t):
    r"\#[^\n]*"
    return t

def t_INPUT(t):
    "input"

# Ordered tokens (see https://stackoverflow.com/questions/2910338/python-yacc-lexer-token-priority):
def t_PRINT(t):
    "print"
    return t

def t_NAME(t):
    r"[a-zA-Z_][a-zA-Z_\d]*"
    return t

# Non-token

t_ignore = " ;\t"

def t_newline(t):
    r"\n|\r\n"
    t.lexer.lineno += 1

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

import libs.ply.lex as lex
lex.lex()


#
# Parser
#

precedence = (
    ("left", "PLUS"),
    ('right', 'NEG'),
    ('left', 'LPAREN'),
)

def p_module(stack):
    """
    module : stmts
    """
    stack[0] = Module(None, stack[1])

def p_stmts_some(stack):
    """
    stmts : stmt stmts
    """
    stack[0] = Stmt([stack[1]] + stack[2].nodes)

def p_stmts_some_comment(stack):
    """
    stmts : stmt COMMENT stmts
    """
    stack[0] = Stmt([stack[1]] + stack[3].nodes)

def p_stmts_none(stack):
    """
    stmts :
    """
    stack[0] = Stmt([])

def p_stmts_none_comment(stack):
    """
    stmts : COMMENT stmts
    """
    stack[0] = stack[2]


# Stmt:

def p_stmt_print(stack):
    """
    stmt : PRINT expr
    """
    stack[0] = Printnl([stack[2]], None)

def p_stmt_expr(stack):
    """
    stmt : expr
    """
    stack[0] = Discard(stack[1])

def p_stmt_assign(stack):
    """
    stmt : NAME ASSIGN expr
    """
    stack[0] = Assign([AssName(stack[1], "OP_ASSIGN")], stack[3])


# Expr:

def p_expr_int(stack):
    """
    expr : INT
    """
    stack[0] = Const(int(stack[1]))

def p_expr_paren(stack):
    """
    expr : LPAREN expr RPAREN
    """
    stack[0] = stack[2]

def p_expr_name(stack):
    """
    expr : NAME
    """
    stack[0] = Name(stack[1])

def p_expr_neg(stack):
    """
    expr : NEG expr
    """
    stack[0] = UnarySub(stack[2])

def p_expr_plus(stack):
    """
    expr : expr PLUS expr
    """
    stack[0] = Add((stack[1], stack[3]))

def p_expr_call(stack):
    """
    expr : INPUT LPAREN RPAREN
    """
    stack[0] = CallFunc(stack[1], [])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

import libs.ply.yacc as yacc
yacc.yacc(start="module", debug=False, write_tables=False)

parse = yacc.parse
