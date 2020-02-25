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


def get_user(session):
    pass


def number_weekday_to_text(number):
    if number == 0:
        return 'Пн'
    elif number == 1:
        return 'Вт'
    elif number == 2:
        return 'Ср'
    elif number == 3:
        return 'Чт'
    elif number == 4:
        return 'Пт'
    elif number == 5:
        return 'Сб'
    elif number == 6:
        return 'Вс'
