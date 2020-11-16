from typing import List, Optional


def approximate_match(template: str, search_query: str, ignore_char: Optional[List[str]] = None,
                      ignore_case: bool = True) -> bool:
    """Проверяет, начинается ли `template` с `search_query`.

    Example:
        >>> approximate_match('H.ello-World', 'helloW', ['-', '.'])
        False

    @param template: Шаблон.
    @param search_query: Преверяемая сторока.
    @param ignore_char: Символы, игнорируемые при сравнении.
    @param ignore_case: Если `True`, то игнорирует регистор символов, иначе регистор символов учитывается.
    @return: `True` - если `template` начинается с `search_query`, иначе `False`.
    """

    def _del_ignore_chars(s: str):
        if ignore_char is None:
            return s

        for i in ignore_char:
            s = s.replace(i, '')
        return s

    # Удаляем игнорируемые симвлы
    template = _del_ignore_chars(template)
    search_query = _del_ignore_chars(search_query)

    # Приводим к нижнему регистру, если задан `ignore_case`.
    if ignore_case:
        template = template.lower()
        search_query = search_query.lower()

    return template.startswith(search_query)
