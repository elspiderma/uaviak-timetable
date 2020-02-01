def to_list(val):
    if val is None:
        return []

    if isinstance(val, list):
        return val

    return [val]


def bool2int(val: bool):
    return int(val) if val is not None else None
