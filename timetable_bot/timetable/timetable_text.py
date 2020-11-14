import typing
from datetime import date

from tortoise.functions import Max

import db
from utils.multiline_text import MultilineText


class Timetable:
    def __init__(self, date: 'date'):
        self.date = date

    @classmethod
    async def for_last_day(cls):
        return cls(await cls._last_date())

    async def list(self):
        raise NotImplemented

    async def get_text(self, search_query: str) -> typing.List[str]:
        raise NotImplemented

    @classmethod
    def _del_unnecessary_chars(cls, text: str):
        raise NotImplemented

    @classmethod
    def _imprecise_comparison(cls, template: str, search_query: str) -> bool:
        template = cls._del_unnecessary_chars(template)
        search_query = cls._del_unnecessary_chars(search_query)

        return template.startswith(search_query)

    @classmethod
    async def _last_date(cls) -> date:
        last_date = await db.Timetable.annotate(last_date=Max('date')).values_list('last_date', flat=True)
        return last_date[0]


class TimetableGroup(Timetable):
    async def list(self) -> typing.List[db.Group]:
        return await db.Group.filter(lessons__date=self.date).distinct()

    @classmethod
    def _del_unnecessary_chars(cls, group_name: str) -> str:
        group_name = group_name.lower()
        group_name = group_name.replace('-', '')
        group_name = group_name.replace(' ', '')
        return group_name

    async def get_text(self, search_query: str) -> typing.Optional[typing.List[str]]:
        suitable_group = []
        for group in await self.list():
            if self._imprecise_comparison(group.title, search_query):
                suitable_group.append(group)

        if len(suitable_group) == 0:
            return None

        text = MultilineText()
        for group in suitable_group:
            text.add_line(f'{group.title}:')
            lessons = await db.Timetable.filter(date=self.date, group=group).order_by('number').all()
            for lesson in lessons:
                teacher = await lesson.teacher.prefetch_related()
                text.add_line(f'{lesson.number}) {lesson.cabinet} каб. {teacher.short_name} {lesson.subject}')

            text.add_line('')

        return text.get()


class TimetableTeacher(Timetable):
    async def list(self) -> typing.List[db.Teacher]:
        return await db.Teacher.filter(lessons__date=self.date).distinct()

    @classmethod
    def _del_unnecessary_chars(cls, teacher_name):
        teacher_name = teacher_name.lower()
        teacher_name = teacher_name.replace('.', '')
        teacher_name = teacher_name.replace(' ', '')
        return teacher_name

    async def get_text(self, search_query: str) -> typing.Optional[typing.List[str]]:
        suitable_teacher = []
        for teacher in await self.list():
            if self._imprecise_comparison(teacher.short_name, search_query):
                suitable_teacher.append(teacher)

        if len(suitable_teacher) == 0:
            return None

        text = MultilineText()
        for teacher in suitable_teacher:
            text.add_line(f'{teacher.short_name}:')
            lessons = await db.Timetable.filter(date=self.date, teacher=teacher).order_by('number').all()
            for lesson in lessons:
                group = await lesson.group.prefetch_related()
                text.add_line(f'{lesson.number}) {lesson.cabinet} каб. {group.title} {lesson.subject}')

            text.add_line('')

        return text.get()