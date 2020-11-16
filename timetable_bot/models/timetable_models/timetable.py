from typing import List, TYPE_CHECKING, Union, ClassVar

import db
from structures import Teacher, Group, TimetableForTeacher, TimetableForGroup, Lesson
from utils.timetable import get_last_date_timetable

if TYPE_CHECKING:
    from datetime import date


class TimetableABCModel:
    def __init__(self, date: 'date'):
        self.date = date
        self._cache_db = dict()

    async def get_timetable(self, obj: Union['Teacher', 'Group']) -> Union['TimetableForGroup', 'TimetableForTeacher']:
        raise NotImplemented

    @property
    async def _list(self) -> List[Union[db.Teacher, db.Group]]:
        raise NotImplemented

    @classmethod
    def _match_object(cls, query: str, obj: Union['db.Teacher', 'db.Group'], approximate: bool) -> bool:
        """Подходил ли запрос объекту.

        @param query: Запрос поиска.
        @param obj: Объект сравниваемый с запросом.
        @param approximate: Если `True`, происходит не четкий поиск, иначе строка сравнивается символ в символ.
        @return:
        """
        raise NotImplemented

    @classmethod
    async def _parse_orm_object(cls, obj: Union['db.Group', 'db.Teacher']) -> Union['Teacher', 'Group']:
        raise NotImplemented

    async def search(self, query: str, approximate: bool = False) -> List[Union['Teacher', 'Group']]:
        """Ищет объекты соответствующие `query`.

        @param query: Запрос поиска.
        @param approximate: Если `True`, происходит не четкий поиск, иначе строка сравнивается символ в символ.
        @return: Список найденных преподавателей.
        """
        suitable = list()
        for orm_object in await self._list:
            if self._match_object(query, orm_object, approximate):
                suitable.append(await self._parse_orm_object(orm_object))

        return suitable

    async def _get_orm_object(self, obj: ClassVar[Group] or ClassVar[Teacher], order_by) -> List[Union[Group, Teacher]]:
        """Получает элементы за дату `self.date`.

        @param obj: Класс, объекты которого нужно полуить.
        @param order_by: Поле для сортировки.
        @return: Найденные объекты.
        """
        if obj.__name__ not in self._cache_db:
            self._cache_db[obj.__name__] = await obj.filter(lessons__date=self.date).order_by(order_by).distinct()

        return self._cache_db[obj.__name__]

    @classmethod
    async def for_last_day(cls) -> 'TimetableABCModel':
        """Последнее расписание.

        @return Объект расписания.
        """
        return cls(await get_last_date_timetable())

    async def _get_timetable(self, *, group_id: int = None, teacher_id: int = None) -> Union['TimetableForGroup',
                                                                                             'TimetableForTeacher']:
        assert group_id is None or teacher_id is None, 'only one parameter needs to be passed'

        is_group_timetable = group_id is not None

        orm_filter = {'date': self.date}
        if is_group_timetable:
            object_which = await db.Group.filter(id=group_id).first()
            orm_filter['group'] = object_which
        else:
            object_which = await db.Teacher.filter(id=teacher_id).first()
            orm_filter['teacher'] = object_which

        lessons = list()
        lessons_orm = await db.Timetable.filter(**orm_filter).order_by('number').all()
        for lesson in lessons_orm:
            group = await lesson.group.prefetch_related() if not is_group_timetable else object_which
            teacher = await lesson.teacher.prefetch_related() if is_group_timetable else object_which

            lessons.append(Lesson(id=lesson.id,
                                  department=lesson.department,
                                  date=lesson.date,
                                  group=Group(id=group.id, title=group.title),
                                  number=lesson.number,
                                  cabinet=lesson.cabinet,
                                  teacher=Teacher(id=teacher.id, name=teacher.short_name, full_name=teacher.full_name),
                                  subject=lesson.subject,
                                  is_splitting=lesson.is_splitting,
                                  is_practice=lesson.is_practice,
                                  is_consultations=lesson.is_consultations,
                                  is_exam=lesson.is_exam))

        if group_id is not None:
            return TimetableForGroup(date=self.date, group=Group(id=object_which.id, title=object_which.title),
                                     lessons=lessons)
        else:
            return TimetableForTeacher(date=self.date,
                                       teacher=Teacher(id=object_which.id, name=object_which.short_name,
                                                       full_name=object_which.full_name),
                                       lessons=lessons)
