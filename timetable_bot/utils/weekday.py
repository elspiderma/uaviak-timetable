def number_weekday_to_text(number: int) -> str:
    """Возвращает сокращенный день недели по его номеру. Например, 1 => "Вт"."""
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
