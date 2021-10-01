from typing import TYPE_CHECKING, Optional

from db import ConnectionKeeper
from db.structures import Timetable, Departaments, TypesLesson, Group, Teacher

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

    async def search_teacher(self, q: str) -> list[Teacher]:
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

        return Teacher.from_records(result, db=self)

    async def search_group(self, q: str) -> list[Group]:
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

        return Group.from_records(result, db=self)

    async def is_exist_timetable(self, date: 'datetime.date', departament: 'Departaments'):
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

        return Timetable.from_record(result, db=self)

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

    @classmethod
    def from_keeper(cls) -> 'Database':
        return Database(ConnectionKeeper.get_connection())
