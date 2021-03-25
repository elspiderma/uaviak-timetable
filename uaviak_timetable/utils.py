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
