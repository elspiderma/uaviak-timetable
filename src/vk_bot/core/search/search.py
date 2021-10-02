from db import Database
from vk_bot.core import GroupResult, TeacherResult


def _is_group(query: str):
    return query[0].isnumeric()


async def search_lessons(query: str):
    db = Database.from_keeper()

    if _is_group(query):
        return [GroupResult(i) for i in await db.search_groups(query)]
    else:
        return [TeacherResult(i) for i in await db.search_teachers(query)]
