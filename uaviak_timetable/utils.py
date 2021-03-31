import typing


def is_string_one_unique_char(s: str, char: str) -> bool:
    """
    Проверяет, состоит ли строка только из одного уникального символа.
    Args:
        s: Проверяемая строка.
        char: Символ.

    Returns:
        True - если в строке только один уникальный символ, иначе False.
    """
    unique_chars = set(s)
    return len(unique_chars) == 1 and char in unique_chars


def ittr_string_with_index(s: str, revers: bool = False) -> typing.Generator[tuple[int, str], None, None]:
    """
    Итеррирует строку.

    Args:
        s: Иттерируемая строка.
        revers: Если `True`, то строка иттерируется в обратном порятке.
    """
    if not revers:
        ittr = s
        index = 0
        step = 1
    else:
        ittr = reversed(s)
        index = len(s) -1
        step = -1

    for char in ittr:
        yield index, char
        index += step


def index_upper(s: str, revers: bool = False):
    """
    Ищет первую заглавную букву.
    Args:
        s: Строка.
        revers: Искать в обраном порядке.

    Returns:
        Индекс первой (или последней, если `revers==True`) заглавной буквы.

    Raises:
        ValueError: В строке нет заглавных букв.
    """
    for n, i in ittr_string_with_index(s, revers):
        if i.isupper():
            return n

    raise ValueError("upper letter case not found")
