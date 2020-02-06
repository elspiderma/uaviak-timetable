def to_list(val):
    if val is None:
        return []

    if isinstance(val, list):
        return val

    return [val]


def string_list_lower(list_str: list):
    return [i.lower() for i in list_str]


def bool2int(val: bool):
    return int(val) if val is not None else None
