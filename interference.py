from graph import Graph
from instructions import *
from compiler.ast import Name

def interference(instructions):
    # type: ([x86instruction]) -> Graph

    g = Graph()
    # Color registers
    for reg in caller_save_regs | callee_save_regs | reserved_regs:
        g.insert_colored(reg, reg)

    def add_edges(data, guard=None):
        for v in i.live_vars_after:
            if guard is None or guard(v):
                g.add_edge(data, v)

    for i in instructions:
        for var in i.vars:
            if isinstance(var, Name):
                g.insert(var.name)
        if isinstance(i, unspillableMovl):
            [s, t] = i.vars
            g.insert(t.name, color_first=True)
            add_edges(t.name, lambda v: v != t.name and (not isinstance(s, Name) or v != s.name))
        elif isinstance(i, movl):
            [s, t] = i.vars
            add_edges(t.name, lambda v: v != t.name and (not isinstance(s, Name) or v != s.name))
        elif isinstance(i, addl):
            [_, t] = i.vars
            add_edges(t.name, lambda v: v != t.name)
        elif isinstance(i, negl):
            [t] = i.vars
            add_edges(t.name, lambda v: v != t.name)
        elif isinstance(i, call):
            for reg in caller_save_regs:
                add_edges(reg)
        elif isinstance(i, pushl):
            pass
        elif isinstance(i, pad_args):
            # "%esp" is written and read, but it is reserved, so no interference
            pass
        elif isinstance(i, unpad_args):
            # "%esp" is written and read, but it is reserved, so no interference
            pass
        else:
            raise TypeError
    return g
