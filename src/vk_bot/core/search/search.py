from typing import TYPE_CHECKING

from db import Database
from vk_bot.core import GroupResult, TeacherResult

if TYPE_CHECKING:
    from vk_bot.core.search.result.group_result import InterfaceResult


def _is_group(query: str):
    """Проверяет, является ли запрос группой или преподавателем.

    Args:
        query: Поисковой запрос.

    Returns:
        True - если запрос содержит группу, иначе False.
    """
    return query[0].isnumeric()


async def search_lessons(query: str) -> list['InterfaceResult']:
    """Ищет подходящие группы или преподавателей в БД.

    Args:
        query: Поисковой запрос.

    Returns:
        Подходящие группы/преподаватели.
    """
    db = Database.from_keeper()

    if _is_group(query):
        return [GroupResult(i) for i in await db.search_groups(query)]
    else:
        return [TeacherResult(i) for i in await db.search_teachers(query)]
