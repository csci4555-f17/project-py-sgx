from instructions import *
from compiler.ast import Name, Const
from utils import union, keys_to_dict
import copy


IFS = 0


# Remove name collisions resulting from different control flow paths being
# followed on different executions.
def rm_cf_name_collisions(i):
    # type: (x86instruction) -> x86instruction
    def renamings(written_in_then, written_in_else):
        # type: ({str}, {str}) -> ({str: Name}, {str: Name})
        # creates dictionaries of renamings
        def thenify(name):
            return Name("if#%d_then_" % IFS + name)
        def elsify(name):
            return Name("if#%d_else_" % IFS + name)
        return keys_to_dict(written_in_then, thenify), keys_to_dict(written_in_else, elsify)

    if isinstance(i, if_instr):
        global IFS
        IFS += 1
        tag = IFS
        then_vars_written = union(map(vars_written, i.then_))
        else_vars_written = union(map(vars_written, i.else_))
        then_renamings, else_renamings = renamings(then_vars_written, else_vars_written)
        renamed_then = map(lambda i_then: rename(then_renamings, i_then), i.then_)
        renamed_else = map(lambda i_else: rename(else_renamings, i_else), i.else_)
        renamed_then_inits = [movl(Name(old), new) for old, new in then_renamings.iteritems()]
        renamed_else_inits = [movl(Name(old), new) for old, new in else_renamings.iteritems()]
        safe_then = renamed_then_inits + map(lambda i_renamed_then: rm_cf_name_collisions(i_renamed_then), renamed_then)
        safe_else = renamed_else_inits + map(lambda i_renamed_else: rm_cf_name_collisions(i_renamed_else), renamed_else)
        test = i.vars[0]
        collisionless_if = if_instr(test, safe_then, safe_else)
        collisionless_if.then_renamings = then_renamings
        collisionless_if.else_renamings = else_renamings
        collisionless_if.tag = tag
        return collisionless_if

    else:
        return i


def vars_written(i):
    # type: (x86instruction) -> {str}
    if isinstance(i, if_instr):
        return union(map(vars_written, i.then_)) | union(map(vars_written, i.else_))
    else:
        return set(only_names(i.vars_written()))

def rename(renamings, instr):

    def _rename(instr_prime):
        return rename(renamings, instr_prime)

    # Padding has no vars, so not copying is safe, and pad is linked to unpad,
    # meaning a copy would break semantics.
    instr_cpy = instr if isinstance(instr, pad_args) or isinstance(instr, unpad_args) else copy.deepcopy(instr)
    renamed_vars = map(lambda v: renamings.get(v.name, v) if is_name(v) else v, instr_cpy.vars)
    instr_cpy.vars = renamed_vars
    if isinstance(instr_cpy, if_instr):
        instr_cpy.then_ = map(_rename, instr_cpy.then_)
        instr_cpy.else_ = map(_rename, instr_cpy.else_)
    return instr_cpy

def is_name(v):
    return isinstance(v, Name) or isinstance(v, str) and v[0] != "%"
    # return isinstance(v, Name)

def only_names(l):
    return filter(is_name, l)
