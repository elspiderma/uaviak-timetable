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
    iter_str = tuple(enumerate(s))
    if revers:
        iter_str = reversed(iter_str)

    for n, i in iter_str:
        if i.isupper():
            return n

    raise ValueError("Upper letter case not found")
