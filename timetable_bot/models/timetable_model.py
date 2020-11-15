from typing import List, Optional, TYPE_CHECKING, Union, ClassVar

from tortoise.functions import Max

import db
from structures import Teacher, Group, TimetableForTeacher, TimetableForGroup, Lesson

if TYPE_CHECKING:
    from datetime import date


class TimetableModel:
    def __init__(self, date: 'date'):
        self.date = date
        self._cache_db = dict()

    async def _get_orm_object(self, obj: ClassVar[Group] or ClassVar[Teacher]) -> List[Union[Group, Teacher]]:
        """Получает элементы за дату `self.date`.

        @param obj: Класс, объекты которого нужно полуить.
        @return: Найденные объекты.
        """
        if obj.__name__ not in self._cache_db:
            self._cache_db[obj.__name__] = await obj.filter(lessons__date=self.date).distinct()

        return self._cache_db[obj.__name__]

    @property
    async def _teachers(self) -> List[db.Teacher]:
        return await self._get_orm_object(db.Teacher)

    @property
    async def _groups(self) -> List[db.Group]:
        return await self._get_orm_object(db.Group)

    @classmethod
    async def for_last_day(cls) -> 'TimetableModel':
        """Последнее расписание.

        @return Объект расписания
        """
        return cls(await cls._get_last_date())

    @classmethod
    async def _get_last_date(cls) -> 'date':
        """ Получает дату последнего расписания. """
        last_date = await db.Timetable.annotate(last_date=Max('date')).values_list('last_date', flat=True)
        return last_date[0]

    @classmethod
    def _approximate_match(cls, template: str, search_query: str, ignore_char: Optional[List[str]] = None,
                           ignore_case: bool = True) -> bool:
        """Проверяет, начинается ли `template` с `search_query`.

        Example:
            >>> cls._approximate_match('H.ello-World', 'helloW', ['-', '.'])
            False
        
        @param template: Шаблон.
        @param search_query: Преверяемая сторока.
        @param ignore_char: Символы, игнорируемые при сравнении.
        @param ignore_case: Если `True`, то игнорирует регистор символов, иначе регистор символов учитывается.
        @return: `True` - если `template` начинается с `search_query`, иначе `False`.
        """
        def _del_unnecessary_chars(s: str):
            if ignore_char is None:
                return s

            for i in ignore_char:
                s = s.replace(i, '')
            return s

        template = _del_unnecessary_chars(template)
        search_query = _del_unnecessary_chars(search_query)

        if ignore_case:
            template = template.lower()
            search_query = search_query.lower()

        return template.startswith(search_query)

    async def get_teachers(self, query: str, approximate: bool = False) -> List['Teacher']:
        """Получает список преподавателей, соответствующие `query`.

        @param query: Запрос поиска.
        @param approximate: Если `True`, происходит не четкий поиск, иначе строка сравнивается символ в символ.
        @return: Список найденных преподавателей.
        """
        suitable_teachers = list()
        for teacher in await self._teachers:
            if (self._approximate_match(teacher.short_name, query, ['.', ' ']) and approximate) or \
                    (teacher.short_name == query and not approximate):
                suitable_teachers.append(Teacher(id=teacher.id, name=teacher.short_name, full_name=teacher.full_name))

        return suitable_teachers

    async def get_groups(self, query: str, approximate: bool = False) -> List['Group']:
        """Получает список групп, соответствующие `query`.

        @param query: Запрос поиска.
        @param approximate: Если `True`, происходит не четкий поиск, иначе строка сравнивается символ в символ.
        @return: Список найденных групп.
        """
        suitable_groups = list()
        for group in await self._groups:
            if (self._approximate_match(group.title, query, ['-', ' ']) and approximate) or \
                    (group.title == query and not approximate):
                suitable_groups.append(Group(id=group.id, title=group.title))

        return suitable_groups

    async def _get_timetable(self, *, group_id: int = None, teacher_id: int = None):
        assert group_id is None or teacher_id is None, 'only one parameter needs to be passed'

        orm_filter = {'date': self.date}
        if group_id is not None:
            object_which = await db.Group.filter(id=group_id).first()
            orm_filter['group'] = object_which
        else:
            object_which = await db.Teacher.filter(id=teacher_id).first()
            orm_filter['teacher'] = object_which

        lessons = list()
        lessons_orm = await db.Timetable.filter(**orm_filter).order_by('number').all()
        for lesson in lessons_orm:
            group = await lesson.group.prefetch_related() if group_id is None else object_which
            teacher = await lesson.teacher.prefetch_related() if teacher_id is None else object_which

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

    async def get_timetable_for_teacher(self, teacher: Union[Teacher, int]) -> TimetableForTeacher:
        """Получает расписание для учителя.

        @param teacher: Учитель, для которого необходимо расписание. Это может быть объект `structures.Teacher`, либо
            его ID
        """
        return await self._get_timetable(teacher_id=teacher if isinstance(teacher, int) else teacher.id)

    async def get_timetable_for_group(self, group: Union[Group, int]):
        """Получает расписание для учителя.

        @param group: Группа, для которого необходимо расписание. Это может быть объект `structures.Group`, либо
            его ID
        """
        return await self._get_timetable(group_id=group if isinstance(group, int) else group.id)
