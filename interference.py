from graph import Graph
from instructions import *
from compiler.ast import Name


def interference(instructions, g=None):
    # type: ([x86instruction]) -> Graph

    if g is None:
        g = Graph()
    # Color registers
    for reg in caller_save_regs | callee_save_regs | reserved_regs:
        g.insert_colored(reg, reg)

    def add_edges(data, guard=None):
        if isinstance(data, Name):
            data = data.name
        assert isinstance(data, str)
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
            add_edges(t, lambda v: not isinstance(s, Name) or v != s.name)
        elif isinstance(i, movl):
            [s, t] = i.vars
            add_edges(t, lambda v: not isinstance(s, Name) or v != s.name)
        elif isinstance(i, cmove):
            [s, t] = i.vars
            add_edges(t, lambda v: not isinstance(s, Name) or v != s.name)
        elif isinstance(i, cmovne):
            [s, t] = i.vars
            add_edges(t, lambda v: not isinstance(s, Name) or v != s.name)
        elif isinstance(i, movzbl_cl):
            [t] = i.vars
            add_edges(t)
        elif isinstance(i, addl):
            [t] = i.vars_written()
            add_edges(t)
        elif isinstance(i, negl):
            [t] = i.vars
            add_edges(t)
        elif isinstance(i, sall):
            [_, t] = i.vars
            add_edges(t)
        elif isinstance(i, sarl):
            [_, t] = i.vars
            add_edges(t)
        elif isinstance(i, andl):
            [_, t] = i.vars
            add_edges(t)
        elif isinstance(i, orl):
            [_, t] = i.vars
            add_edges(t)
        elif isinstance(i, call):
            for reg in caller_save_regs:
                add_edges(reg)
        elif isinstance(i, pad_args):
            # "%esp" is written and read, but it is reserved, so no interference
            pass
        elif isinstance(i, unpad_args):
            # "%esp" is written and read, but it is reserved, so no interference
            pass
        elif isinstance(i, if_instr):
            ts = i.vars_written()
            for t in ts:
                add_edges(t)
            g = interference(i.then_, g)
            g = interference(i.else_, g)
        elif isinstance(i, while_instr):
            ts = i.vars_written()
            for t in ts:
                add_edges(t)
            g = interference(i.test_instrs, g)
            g = interference(i.body, g)
        elif isinstance(i, sete_cl):
            [t] = i.vars_written()
            add_edges(t)
        elif isinstance(i, setne_cl):
            [t] = i.vars_written()
            add_edges(t)
        elif isinstance(i, sete_cl):
            [t] = i.vars_written()
            add_edges(t)
        # Read only instructions
        elif isinstance(i, pushl):
            pass
        elif isinstance(i, cmpl):
            pass
        else:
            raise TypeError("instruction class interference not implemented.", i.__class__.__name__)
    return g
