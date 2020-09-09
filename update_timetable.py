import asyncio

from utils.timetablecache import TimetableCache
import db


async def update_timetable() -> bool:
    timetable = await TimetableCache.load_from_site_if_updated()
    if timetable is None:
        return False

    db.session.query(db.TimetableDB).delete()

    for lesson in timetable:
        db.session.add(db.TimetableDB(
            date=timetable.date,
            group=lesson.group,
            number=lesson.number,
            cabinet=lesson.cabinet,
            teacher=lesson.teacher,
            subject=lesson.subject,
            is_splitting=lesson.is_splitting,
            is_practice=lesson.is_practice,
            is_consultations=lesson.is_consultations,
            is_exam=lesson.is_exam
        ))

    db.session.commit()

if __name__ == '__main__':
    print(asyncio.run(update_timetable()))
