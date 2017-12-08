from compiler.ast import Name

__freed = []
__temp_vars = 0


class InternalName(Name):
    """
    Behaves exactly like Name, but allows distinction between temp vars
    allocated internally by the flattener and those allocated explicitly by
    the program, so we only free locally allocated vars
    """
    pass


def allocate():
    # type: () -> Name
    global __temp_vars
    try:
        return __freed.pop()
    except IndexError:
        __temp_vars += 1
        # Hash (#) added so no conflicts can arise with program names
        return InternalName("#PYYC_TEMP_" + str(__temp_vars))


def free(name):
    # type: (Name) -> ()
    if isinstance(name, InternalName):
        __freed.append(name)
