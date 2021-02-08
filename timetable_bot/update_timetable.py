import asyncio

import db
from utils.timetable import TimetableAsync, get_last_date_timetable

from models.timetable import TimetableModel, TimetableNotFound
from datetime import date
from tortoise.functions import Max


async def update_timetable() -> dict:
    """Получает новое расписание колледжа.

    @return: Словарь из ключей `lessons`, `teachers`, `groups`.
        lessons - множество новых уроков
        teachers - множество учителей, для который обновилось расписание
        groups - множество групп, для который обновилось расписание
    """
    modified = {
        'lessons': set(),
        'teachers': set(),
        'groups': set()
    }

    timetables = await TimetableAsync.load()

    for timetable in timetables:
        for lesson in timetable:
            group = await db.Group.filter(title=lesson.group).first()
            if group is None:
                group = await db.Group.create(title=lesson.group)

            teacher = await db.Teacher.filter(short_name=lesson.teacher).first()
            if teacher is None:
                teacher = await db.Teacher.create(short_name=lesson.teacher)

            is_exists_lesson = await db.Lesson.filter(
                department=timetable.department.value,
                date=timetable.date,
                group=group,
                number=lesson.number,
                cabinet=lesson.cabinet,
                teacher=teacher,
                subject=lesson.subject,
                is_splitting=lesson.is_splitting,
                is_practice=lesson.is_practice,
                is_consultations=lesson.is_consultations,
                is_exam=lesson.is_exam
            ).exists()
            if not is_exists_lesson:
                lesson = await db.Lesson.create(
                    department=timetable.department.value,
                    date=timetable.date,
                    group=group,
                    number=lesson.number,
                    cabinet=lesson.cabinet,
                    teacher=teacher,
                    subject=lesson.subject,
                    is_splitting=lesson.is_splitting,
                    is_practice=lesson.is_practice,
                    is_consultations=lesson.is_consultations,
                    is_exam=lesson.is_exam
                )
                modified['lessons'].add(lesson)
                modified['teachers'].add(teacher)
                modified['groups'].add(group)

    return modified


async def main():
    await db.init()
    # print(await update_timetable())
    a = TimetableModel('19ис-1', await get_last_date_timetable())
    b = await a.exec()
    c = await b[0].lessons[0].teacher.prefetch_related()
    print(c.short_name)
    await db.stop()


if __name__ == '__main__':
    asyncio.run(main())
