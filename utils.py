def union(sets):
    return set.union(*sets)

def keys_to_dict(keys, value_of_key):
    values = map(value_of_key, keys)
    return dict(zip(keys, values))
