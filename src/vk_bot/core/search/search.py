from typing import TYPE_CHECKING

from db.structures import WhoseTimetable
from vk_bot.core.search import GroupResult, TeacherResult

if TYPE_CHECKING:
    from vk_bot.core.search.result.group_result import AbstractResult


def _is_group(query: str):
    """Проверяет, является ли запрос группой или преподавателем.

    Args:
        query: Поисковой запрос.

    Returns:
        True - если запрос содержит группу, иначе False.
    """
    return query[0].isnumeric()


async def search_by_query(query: str) -> list['AbstractResult']:
    """Ищет подходящие группы или преподавателей в БД по поисковому запросу.

    Args:
        query: Поисковой запрос.

    Returns:
        Подходящие группы/преподаватели.
    """
    if _is_group(query):
        return await GroupResult.search(query)
    else:
        return await TeacherResult.search(query)


async def search_by_id(whose: 'WhoseTimetable', id_: int) -> 'AbstractResult':
    """Ищет группы или преподавателей по payload'у.

    Args:
        whose: Тип объекта.
        id_: ID искомого объекта.

    Returns:
        Результаты поиска.
    """
    if whose is WhoseTimetable.FOR_GROUP:
        return await GroupResult.search_by_id(id_)
    elif whose is WhoseTimetable.FOR_TEACHER:
        return await TeacherResult.search_by_id(id_)
    else:
        raise RuntimeError('Not supported whose_timetable.')
