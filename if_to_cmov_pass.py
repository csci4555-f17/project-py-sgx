from instructions import *
from compiler.ast import Name, Const
from utils import flat_map


def if_to_cmov(instr, outer_test = None):
    if isinstance(instr, if_instr):
        saved_test = Name("if#%d_test" % instr.tag)
        res = []
        res.append(movl(instr.vars[0], saved_test))
        if outer_test:
            # make this test result in 0 if outer test was 0
            res.append(movl(Const(0), "%ecx"))
            res.append(cmpl(Const(0), outer_test))
            res.append(cmove("%ecx", saved_test))
        const_then = flat_map(lambda i: if_to_cmov(i, outer_test), instr.then_)
        const_else = flat_map(lambda i: if_to_cmov(i, outer_test), instr.else_)
        res += const_then
        res += const_else
        # then
        for old, new in instr.then_renamings.iteritems():
            res.append(movl(Name(old), "%ecx"))
            res.append(cmpl(Const(0), saved_test))
            res.append(cmovne(new, "%ecx"))
            res.append(movl("%ecx", Name(old)))
        # else
        for old, new in instr.else_renamings.iteritems():
            res.append(movl(Name(old), "%ecx"))
            res.append(cmpl(Const(0), saved_test))
            res.append(cmove(new, "%ecx"))
            res.append(movl("%ecx", Name(old)))
        return res

    elif isinstance(instr, while_instr):
        instr.test_instrs = flat_map(if_to_cmov, instr.test_instrs)
        instr.body = flat_map(if_to_cmov, instr.body)
        return [instr]

    else:
        return [instr]