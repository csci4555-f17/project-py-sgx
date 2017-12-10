def union(sets):
    return set.union(*sets) if sets else set()


def keys_to_dict(keys, value_of_key):
    values = map(value_of_key, keys)
    return dict(zip(keys, values))


def unzip(l):
    return [a for a, _ in l], [b for _, b in l]


def flat_map(f, l):
    """
    Similar to `map`, but allows f to return a list, after which each list
    will be concatenated together, in the order.
    """
    return reduce(lambda l1, l2: l1 + l2, map(f, l), [])


def sequence(l_of_ls):
    """
    [[a], [b, c]] -> [a, b, c]
    """
    return [item for l in l_of_ls for item in l]
