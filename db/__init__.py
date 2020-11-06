from db.teacher import Teacher
from db.group import Group
from db.chat import Chat
from db.notify import NotifyGroup, NotifyTeacher
from db.timetable import Timetable
from tortoise import Tortoise
from config import DATA_BASE


async def init():
    await Tortoise.init(
        db_url=DATA_BASE,
        modules={'models': [
            'db.chat',
            'db.group',
            'db.teacher',
            'db.notify',
            'db.timetable'
        ]}
    )
    await Tortoise.generate_schemas()


async def stop():
    await Tortoise.close_connections()
