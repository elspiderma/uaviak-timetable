from tortoise import Tortoise

from config import DATA_BASE
from db.chat import Chat
from db.group import Group
from db.notify import NotifyGroup, NotifyTeacher
from db.teacher import Teacher
from db.timetable import Timetable


async def init():
    await Tortoise.init(
        db_url=DATA_BASE,
        modules={'models': ['db']}
    )
    await Tortoise.generate_schemas()


async def stop():
    await Tortoise.close_connections()


__all__ = ['Teacher', 'Group', 'Chat', 'NotifyGroup', 'NotifyTeacher', 'Timetable']
