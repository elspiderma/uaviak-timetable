from typing import TYPE_CHECKING, Optional, Union

from db import ConnectionKeeper
from db.structures import Timetable, Departaments, TypesLesson, Group, Teacher, Lesson, TimetableForGroup
from db.structures.timetable_for_teacher import TimetableForTeacher

if TYPE_CHECKING:
    import datetime
    import asyncpg
    import uaviak_parser
    from db.structures import Departaments


class Database:
    """Класс для работы с БД.
    """

    def __init__(self, connection: 'asyncpg.Connection'):
        """
        Args:
            connection: Потключение к БД.
        """
        self.conn = connection

    async def search_teachers(self, q: str) -> list[Teacher]:
        """Поиск преподавателя по имени (short_name). При поиске игнорируются символ '.',
        а так же регистр символов. Разрешается не дописывать ФИО.

        Args:
            q: Поисковой запрос.

        Returns:
            Подходящие преподаватели.
        """
        q = q.replace('.', '').lower()
        pattern = f'{q}%'

        result = await self.conn.fetch(
            'SELECT * FROM teachers WHERE replace(teachers.short_name, \'.\', \'\') ILIKE $1',
            pattern
        )

        return Teacher.from_records(result)

    async def search_groups(self, q: str) -> list[Group]:
        """Поиск группы. При поиске игнорируются символы '-', ' ', а так же регистр символов.
        Разрешается не дописывать номер.

        Args:
            q: Поисковой запрос.

        Returns:
            Подходящие группы.
        """
        q = q.replace('-', '').replace(' ', '').lower()
        pattern = f'{q}%'

        result = await self.conn.fetch(
            'SELECT * FROM groups WHERE replace("groups"."number", \'-\', \'\') ILIKE $1',
            pattern
        )

        return Group.from_records(result)

    async def is_exist_timetable(self, date: 'datetime.date', departament: 'Departaments') -> bool:
        """Проверяет, существует ли расписание.

        Args:
            date: Дата.
            departament: Отделение.

        Returns:
            True, если существует или False, если не существует.
        """
        result = await self.conn.fetchrow(
            'SELECT COUNT(*) FROM timetables WHERE date = $1 AND departament = $2',
            date, departament.value
        )

        return result['count'] == 1

    async def get_group_by_id(self, group_id: int) -> Group:
        result = await self.conn.fetchrow('SELECT * FROM groups WHERE groups.id = $1', group_id)
        return Group.from_record(result)

    async def get_teacher_by_id(self, teacher_id: int) -> Teacher:
        result = await self.conn.fetchrow('SELECT * FROM teachers WHERE teachers.id = $1', teacher_id)
        return Teacher.from_record(result)

    async def get_timetables_for_group(self, group: Union[int, Group], count: int = 1) -> list[Timetable]:
        group_id = group.id if isinstance(group, Group) else group

        query = '''
            SELECT *
            FROM timetables
            WHERE
                timetables.id IN (SELECT DISTINCT lessons.id_timetable FROM lessons WHERE id_group = $1)
            ORDER BY date DESC
            LIMIT $2
        '''

        result = await self.conn.fetch(query, group_id, count)

        return Timetable.from_records(result)

    async def get_dates_timetable_for_group(self, group: Union[int, Group], count: int = 6) -> list['datetime.date']:
        group_id = group.id if isinstance(group, Group) else group

        query = '''
            SELECT date
            FROM timetables
            WHERE
                timetables.id IN (SELECT DISTINCT lessons.id_timetable FROM lessons WHERE id_group = $1)
            ORDER BY date DESC
            LIMIT $2
        '''

        result = await self.conn.fetch(query, group_id, count)

        return [i['date'] for i in result]

    async def get_timetable_lessons_for_group(self, group: Union[int, Group], timetable: Union[int, Timetable]) \
            -> list[Lesson]:
        group_id = group.id if isinstance(group, Group) else group
        timetable_id = timetable.id if isinstance(timetable, Timetable) else timetable

        queue = '''
            SELECT *
            FROM lessons
            WHERE
                id_timetable = $1 AND
                id_group = $2
            ORDER BY number
        '''
        result = await self.conn.fetch(queue, timetable_id, group_id)

        return Lesson.from_records(result)

    async def get_last_timetable_for_group_with_lesson(self, group: Union[int, Group]) -> TimetableForGroup:
        group = await self._get_group_or_return(group)

        timetables = await self.get_timetables_for_group(group, 1)
        timetable = timetables[0]

        lessons = await self.get_timetable_lessons_for_group(group, timetable)

        return TimetableForGroup(group=group, timetable=timetable, lessons=lessons)

    async def get_dates_timetable_for_teacher(self, teacher: Union[int, Teacher], count: int = 6) -> list['datetime.date']:
        teacher_id = teacher.id if isinstance(teacher, Teacher) else teacher

        query = '''
            SELECT date
            FROM timetables
            WHERE
                timetables.id IN (SELECT DISTINCT lessons.id_timetable FROM lessons WHERE id_teacher = $1)
            ORDER BY date DESC
            LIMIT $2
        '''

        result = await self.conn.fetch(query, teacher_id, count)

        return [i['date'] for i in result]

    async def get_timetables_for_teacher(self, teacher: Union[int, Teacher], count: int = 1) -> list[Timetable]:
        teacher_id = teacher.id if isinstance(teacher, Teacher) else teacher

        query = '''
            SELECT *
            FROM timetables
            WHERE
                timetables.id IN (SELECT DISTINCT lessons.id_timetable FROM lessons WHERE id_teacher = $1)
            ORDER BY date DESC
            LIMIT $2
        '''

        result = await self.conn.fetch(query, teacher_id, count)

        return Timetable.from_records(result)

    async def get_timetable_lessons_for_teacher(self, teacher: Union[int, Teacher], timetable: Union[int, Timetable]) \
            -> list[Lesson]:
        teacher_id = teacher.id if isinstance(teacher, Teacher) else teacher
        timetable_id = timetable.id if isinstance(timetable, Timetable) else timetable

        queue = '''
            SELECT *
            FROM lessons
            WHERE
                id_timetable = $1 AND
                id_teacher = $2
            ORDER BY number
        '''
        result = await self.conn.fetch(queue, timetable_id, teacher_id)

        return Lesson.from_records(result)

    async def get_last_timetable_for_teacher_with_lesson(self, teacher: Union[int, Teacher]) -> TimetableForTeacher:
        teacher = await self._get_teacher_or_return(teacher)

        timetables = await self.get_timetables_for_teacher(teacher, 1)
        timetable = timetables[0]

        lessons = await self.get_timetable_lessons_for_teacher(teacher, timetable)

        return TimetableForTeacher(teacher=teacher, timetable=timetable, lessons=lessons)

    async def get_timetable(self, date: 'datetime.date', departament: 'Departaments') -> Optional[Timetable]:
        """Получает расписание за определенную дату для определенного отделения.

        Args:
            date: Дата.
            departament: Отделение.

        Returns:
            Расписание или None, если расписание не найдено.
        """
        result = await self.conn.fetchrow(
            'SELECT * FROM timetables WHERE date = $1 AND departament = $2',
            date, departament.value
        )

        if not result:
            return None

        return Timetable.from_record(result)

    async def add_new_timetable(self, timetable: 'uaviak_parser.structures.Timetable') -> None:
        """Добавляет новое расписание.

        Args:
            timetable: Расписание полученное с сайта
        """
        result = await self.conn.fetch(
            'INSERT INTO timetables(additional_info, date, departament) VALUES ($1, $2, $3) RETURNING id',
            timetable.additional_info, timetable.date, Departaments.from_parser_departaments(timetable.departament).value
        )
        timetable_id = result[0]['id']

        for lesson in timetable.lessons:
            lesson_types = [TypesLesson.from_parser_type_lesson(i).value for i in lesson.types]
            await self.conn.fetch(
                'SELECT * FROM add_lesson'
                '($1,         $2,            $3,             $4,             $5,           $6,           $7)',
                timetable_id, lesson.number, lesson.subject, lesson.cabinet, lesson_types, lesson.group, lesson.teacher
            )

    async def _get_group_or_return(self, group: Union[int, Group]) -> Group:
        return group if isinstance(group, Group) else await self.get_group_by_id(group)

    async def _get_teacher_or_return(self, teacher: Union[int, Group]) -> Teacher:
        return teacher if isinstance(teacher, Teacher) else await self.get_teacher_by_id(teacher)

    @classmethod
    def from_keeper(cls) -> 'Database':
        return Database(ConnectionKeeper.get_connection())
