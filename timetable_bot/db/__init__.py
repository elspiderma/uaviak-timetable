from tortoise import Tortoise

from config import TORTOISE_ORM
from db.chat import Chat
from db.group import Group
from db.lesson import Lesson
from db.notify import NotifyGroup, NotifyTeacher
from db.teacher import Teacher


async def init():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def stop():
    await Tortoise.close_connections()


__all__ = ['Teacher', 'Group', 'Chat', 'NotifyGroup', 'NotifyTeacher', 'Lesson']
