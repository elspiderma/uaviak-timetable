import enum
from typing import Optional, TYPE_CHECKING, List

import db
from utils.timetable import is_group

if TYPE_CHECKING:
    from datetime import date


class TypeTimetable(enum.Enum):
    TEACHER = enum.auto()
    GROUP = enum.auto()


class TimetableNotFound(Exception):
    def __init__(self, query: str, type_: TypeTimetable, is_autodetect_type: bool):
        self.query = query
        self.is_autodetect_type = is_autodetect_type
        self.type = type_
        super().__init__(f'Not fount "{self.query}"')


class TimetableABC:
    def __init__(self, date: 'date', lessons: List['db.Lesson']):
        self.date = date
        self.lessons = lessons

    def get_title_according(self):
        """Возвращает заголовок объекта, по которому было сформировано расписание."""
        raise NotImplemented

    def __repr__(self):
        return f'<Timetable for "{self.get_title_according()}" {self.date}>'


class TimetableGroup(TimetableABC):
    def __init__(self, date: 'date', lessons: List['db.Lesson'], group: 'db.Group'):
        super().__init__(date, lessons)
        self.group = group

    def get_title_according(self) -> str:
        return self.group.title


class TimetableTeacher(TimetableABC):
    def __init__(self, date: 'date', lessons: List['db.Lesson'], teacher: 'db.Teacher'):
        super().__init__(date, lessons)
        self.teacher = teacher

    def get_title_according(self) -> str:
        return self.teacher.short_name


class TimetableModel:
    __RATION = {
        TypeTimetable.GROUP: {'orm': db.Group, 'result': TimetableGroup},
        TypeTimetable.TEACHER: {'orm': db.Teacher, 'result': TimetableTeacher}
    }

    def __init__(self, query: str, date_: 'date', type_: Optional[TypeTimetable] = None):
        self.date = date_
        self.query = query
        self.is_autodetect_type = False if type_ else True
        if self.is_autodetect_type:
            self.type = TypeTimetable.GROUP if is_group(query) else TypeTimetable.TEACHER
        else:
            self.type = type_

    async def exec(self) -> List['TimetableABC']:
        found_objects = await self.__RATION[self.type]['orm'].approximate_search(self.query)

        if len(found_objects) == 0:
            raise TimetableNotFound(self.query, self.type, self.is_autodetect_type)

        timetables = []
        for obj in found_objects:
            lessons = await obj.get_timetable(self.date)
            timetables.append(self.__RATION[self.type]['result'](self.date, lessons, obj))

        return timetables
