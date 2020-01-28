def to_list(val):
    if val is None:
        return []

    if isinstance(val, list):
        return val

    return [val]
