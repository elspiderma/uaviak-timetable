import asyncio
import typing

import db
from timetable.timetable_async import TimetableCache


async def update_timetable():
    modified = {
        'lessons': set(),
        'teachers': set(),
        'groups': set()
    }

    timetable = await TimetableCache.load()
    if not timetable:
        return modified

    for lesson in timetable:
        group = await db.Group.filter(title=lesson.group).first()
        if group is None:
            group = await db.Group.create(title=lesson.group)

        teacher = await db.Teacher.filter(short_name=lesson.teacher).first()
        if teacher is None:
            teacher = await db.Teacher.create(short_name=lesson.teacher)

        is_exists_lesson = await db.Timetable.filter(
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
            lesson = await db.Timetable.create(
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
    print(await update_timetable())
    await db.stop()


if __name__ == '__main__':
    asyncio.run(main())
