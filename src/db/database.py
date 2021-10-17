from typing import TYPE_CHECKING, Optional, Union, Collection, Any

from db import ConnectionKeeper
from db.structures import Timetable, TypesLesson, Group, Teacher, Lesson, TimetableForGroup, \
    TimetableForTeacher, Chat, VKCachePhoto

if TYPE_CHECKING:
    import datetime
    import asyncpg
    import uaviak_parser


class Database:
    """Класс для работы с БД.
    """

    def __init__(self, connection: 'asyncpg.Connection'):
        """
        Args:
            connection: Потключение к БД.
        """
        self.conn = connection

    # Search

    async def _search(
            self,
            q: str,
            table: str,
            column: str,
            ignore_chars: Collection[str] = None
    ) -> list['asyncpg.Record']:
        """Поиск записей соответствующих запросу.

        Args:
            q: Поисковой запрос.
            table: Таблица для поиска.
            column: Колонка сравнения запросу.
            ignore_chars: Игнорируемые символы.

        Returns:
            Подходящие записи.
        """
        if ignore_chars:
            remove_char = ''.join(ignore_chars).lower()
            for char in ignore_chars:
                q = q.replace(char.lower(), '')
        else:
            remove_char = ''

        pattern = f'{q.lower()}%'

        sql_query = f'SELECT * FROM "{table}" WHERE translate(lower("{column}"), $1, \'\') LIKE $2 ORDER BY {column}'
        result = await self.conn.fetch(sql_query, remove_char, pattern)

        return result

    async def search_teachers(self, q: str) -> list[Teacher]:
        """Поиск преподавателя по имени (short_name). При поиске игнорируются символ '.',
        а так же регистр символов. Разрешается не дописывать ФИО.

        Args:
            q: Поисковой запрос.

        Returns:
            Подходящие преподаватели.
        """
        found_teachers = await self._search(q, 'teachers', 'short_name', ('.', ' ', ))
        return Teacher.from_records(found_teachers)

    async def search_groups(self, q: str) -> list[Group]:
        """Поиск группы. При поиске игнорируются символы '-', ' ', а так же регистр символов.
        Разрешается не дописывать номер.

        Args:
            q: Поисковой запрос.

        Returns:
            Подходящие группы.
        """
        found_groups = await self._search(q, 'groups', 'number', ('-', ' ', ))
        return Group.from_records(found_groups)

    # Timetable

    async def is_exist_timetable(self, date: 'datetime.date') -> bool:
        """Проверяет, существует ли расписание.

        Args:
            date: Дата.

        Returns:
            True, если существует или False, если не существует.
        """
        result = await self.conn.fetchrow('SELECT COUNT(*) FROM timetables WHERE date = $1', date)

        return result['count'] == 1

    # Search by id

    async def _search_by_id(self, id_: int, table: str) -> Optional['asyncpg.Record']:
        """Ищет запись по id, из таблицы table.

        Args:
            id_: ID записи.
            table: Таблица, где искать ID.

        Returns:
            Строка из БД или None, если такого ID не существует.
        """
        return await self.conn.fetchrow(f'SELECT * FROM "{table}" WHERE id = $1', id_)

    async def search_group_by_id(self, group_id: int) -> Optional[Group]:
        """Ищет группу с group_id.

        Args:
            group_id: ID группы.

        Returns:
            Группа или None, если такой группы не существует.
        """
        result = await self._search_by_id(group_id, 'groups')
        return Group.from_record(result) if result else None

    async def search_teacher_by_id(self, teacher_id: int) -> Optional[Teacher]:
        """Ищет преподавателя с teacher_id.

        Args:
            teacher_id: ID преподавателя.

        Returns:
            Преподаватель или None, если такого преподавателя не существует.
        """
        result = await self._search_by_id(teacher_id, 'teachers')
        return Teacher.from_record(result) if result else None

    # Search timetables with certain lesson

    async def _search_timetables_with_certain_lesson(
            self,
            column: str,
            value: Any,
            order_by_column: str = None,
            is_desc_order: bool = False,
            limit: int = None,
            fields: Collection[str] = None
    ) -> list['asyncpg.Record']:
        """Получает расписание содержащяя пару удовлетворяющее условие "column == value"

        Args:
            column: Столбец пары в котором мы ищем значение.
            value: Искомое значение.
            order_by_column: Столбец для сортировки, если None, сортировка не производится.
            is_desc_order: Если True сортировка производится в обратном порядке.
            limit: Максимальное количество записей.
            fields: Возвращаемы поля в записи, если None, то возвращаются все поля.
        Returns:
            Список расписаний содержащий нужную пару.
        """
        if fields:
            fields_sql = ', '.join(f'"{i}"' for i in fields)
        else:
            fields_sql = '*'

        query = f'''
            SELECT {fields_sql}
            FROM timetables
            WHERE
                timetables.id IN (SELECT DISTINCT id_timetable FROM lessons WHERE "{column}" = $1)
        '''
        args_query = [value]

        if order_by_column and is_desc_order:
            query += f' ORDER BY "{order_by_column}" DESC '
        elif order_by_column and not is_desc_order:
            query += f' ORDER BY "{order_by_column}" '

        if limit:
            args_query.append(limit)
            query += f' LIMIT $2 '

        result = await self.conn.fetch(query, *args_query)
        return result

    async def get_date_timetables_with_lesson_for_group(
            self,
            group: Union[int, Group],
            sort_by_date: bool = False,
            sort_new_to_old: bool = True,
            count: int = None
    ) -> list['datetime.date']:
        """Возвращает даты расписаниий содержащих пару для группы group.

        Args:
            group: Группа или ID группы.
            sort_by_date: Если True, то сортирует расписания по дате.
            sort_new_to_old: Если True, то сортирует от новых расписаний до стрых.
            count: Количество дат.

        Returns:
            Даты расписаний содержащию пару для группы group.
        """
        group_id = group.id if isinstance(group, Group) else group

        result = await self._search_timetables_with_certain_lesson(
            'id_group',
            group_id,
            'date' if sort_by_date else False,
            sort_new_to_old,
            count,
            ('date', )
        )

        return [i['date'] for i in result]

    async def get_date_timetables_with_lesson_for_teacher(
            self,
            teacher: Union[int, Teacher],
            sort_by_date: bool = False,
            sort_new_to_old: bool = True,
            count: int = None
    ) -> list['datetime.date']:
        """Возвращает даты расписаниий содержащих пару для преподавателя teacher.

        Args:
            teacher: Преподаватель или ID преподавателя.
            sort_by_date: Если True, то сортирует расписания по дате.
            sort_new_to_old: Если True, то сортирует от новых расписаний до стрых.
            count: Количество дат.

        Returns:
            Даты расписаний содержащию пару для преподавателя teacher.
        """
        teacher_id = teacher.id if isinstance(teacher, Teacher) else teacher

        result = await self._search_timetables_with_certain_lesson(
            'id_teacher',
            teacher_id,
            'date' if sort_by_date else False,
            sort_new_to_old,
            count,
            ('date', )
        )

        return [i['date'] for i in result]

    async def _get_full_information_timetable_lessons_by_date(
            self,
            column: str,
            value: Any,
            date: 'datetime.date'
    ) -> list['asyncpg.Record']:
        """Получение полной информации о парах для дня date для которые подходят под условие "column = value".

        Args:
            column: Столбец в котором мы ищем значение value.
            value: Искомое значение.
            date: Дата искомых пар.

        Returns:
            Полная информация о парах.
        """
        column = '.'.join(f'"{i}"' for i in column.split('.'))
        query = f"""
            SELECT
                l.id as l_id,
                l.id_timetable,
                l."number" as l_number,
                l.subject,
                l.cabinet,
                l."types",
                l.id_group,
                l.id_teacher,
                g."id" as g_id,
                g."number" as g_number,
                t.id as t_id,
                t.short_name,
                t.full_name,
                tt.id as tt_id,
                tt.date
            FROM
                lessons l
                INNER JOIN groups g on g.id = l.id_group
                INNER JOIN teachers t on t.id = l.id_teacher
                INNER JOIN timetables tt on tt.id = l.id_timetable
            WHERE
                  {column} = $1 AND
                  tt.date = $2
            ORDER BY
                l.number
        """
        return await self.conn.fetch(query, value, date)

    async def get_full_information_timetable_by_date_for_group(
            self,
            date: 'datetime.date',
            group: Union[int, Group]
    ) -> Optional[TimetableForGroup]:
        """Получение полной информации о расписании группы group за день date.

        Args:
            date: Дата расписания.
            group: Группа.

        Returns:
            Полная информация о расписании группы group за день date.
        """
        group = await self._get_group_or_return(group)

        result = await self._get_full_information_timetable_lessons_by_date(
            'g.id',
            group.id,
            date
        )
        return TimetableForGroup.from_combined_records(result, group)

    async def get_full_information_timetable_by_date_for_teacher(
            self,
            date: 'datetime.date',
            teacher: Union[int, Teacher]
    ) -> Optional[TimetableForTeacher]:
        """Получение полной информации о расписании преподавателя teacher за день date.

        Args:
            date: Дата расписания.
            teacher: Преподаватель.

        Returns:
            Полная информация о расписании преподавателя teacher за день date.
        """
        teacher = await self._get_teacher_or_return(teacher)

        result = await self._get_full_information_timetable_lessons_by_date(
            't.id',
            teacher.id,
            date
        )
        return TimetableForTeacher.from_combined_records(result, teacher)

    async def get_timetable(self, date: 'datetime.date') -> Optional[Timetable]:
        """Получает расписание за определенную дату для определенного отделения.

        Args:
            date: Дата.

        Returns:
            Расписание или None, если расписание не найдено.
        """
        result = await self.conn.fetchrow('SELECT * FROM timetables WHERE date = $1', date)

        if not result:
            return None

        return Timetable.from_record(result)

    async def add_new_timetable(self, timetable: 'uaviak_parser.structures.Timetable') -> None:
        """Добавляет новое расписание.

        Args:
            timetable: Расписание полученное с сайта
        """
        result = await self.conn.fetch('INSERT INTO timetables(date) VALUES ($1) RETURNING id', timetable.date)
        timetable_id = result[0]['id']

        for lesson in timetable.lessons:
            lesson_types = [TypesLesson.from_parser_type_lesson(i).value for i in lesson.types]
            await self.conn.fetch(
                'SELECT * FROM add_lesson'
                '($1,         $2,            $3,             $4,             $5,           $6,           $7)',
                timetable_id, lesson.number, lesson.subject, lesson.cabinet, lesson_types, lesson.group, lesson.teacher
            )

    async def _get_group_or_return(self, group: Union[int, Group]) -> Group:
        """Если передан int, то получает группу по ID, иначе возвращает ее.

        Args:
            group: Группа или ID группы.

        Returns:
            Группа.
        """
        return group if isinstance(group, Group) else await self.search_group_by_id(group)

    async def _get_teacher_or_return(self, teacher: Union[int, Group]) -> Teacher:
        """Если передан int, то получает преподавателя по ID, иначе возвращает ее.

        Args:
            teacher: Преподаватель или ID преподавателя.

        Returns:
            Преподаватель.
        """
        return teacher if isinstance(teacher, Teacher) else await self.search_teacher_by_id(teacher)

    async def get_chat_by_vk_id(self, vk_id: int) -> Optional[Chat]:
        """Получает чат VK из БД.

        Args:
            vk_id: VK ID чата.

        Returns:
            Чат VK.
        """
        result = await self.conn.fetchrow('SELECT * FROM chats WHERE vk_id = $1', vk_id)

        if not result:
            return None

        return Chat.from_record(result)

    async def create_new_chat(self, vk_id: int) -> None:
        """Добавляет запись о чате VK в бд.

        Args:
            vk_id: VK ID чата.
        """
        await self.conn.execute('INSERT INTO chats(vk_id) VALUES ($1)', vk_id)

    async def get_chat_and_create_if_not_exist(self, vk_id) -> Chat:
        """Получает чат VK, предварительно добавив запись о нем в БД, если его нет.

        Args:
            vk_id: VK ID чата.

        Returns:
            Чат VK.
        """
        chat = await self.get_chat_by_vk_id(vk_id)
        if chat:
            return chat

        await self.create_new_chat(vk_id)
        return await self.get_chat_by_vk_id(vk_id)

    async def get_cache_photo_id_by_key(self, key: str) -> Optional[VKCachePhoto]:
        """Получает ID кэшированого фото.

        Args:
            key: Ключ кэша.

        Returns:
            Кэшированное фото или None, если его нет.
        """
        result = await self.conn.fetchrow('SELECT * FROM vk_cache_photo WHERE key_cache = $1', key)

        if not result:
            return None

        return VKCachePhoto.from_record(result)

    async def set_cache_photo(self, key: str, photo_id: str) -> None:
        """Добавляет кэш фотографии.

        Args:
            key: Ключ кэша.
            photo_id: ID фотографии.
        """
        await self.conn.execute('CALL add_or_update_vk_cache($1, $2)', key, photo_id)

    async def change_format_timetable_for_chat(self, chat: Union[int, Chat]) -> None:
        """Изменяет настройку отвечающию за формат фотографии с фото на текст и наоборот.

        Args:
            chat: ID чата из БД (не VK'онтактовский)
        """
        chat_id = chat if isinstance(chat, int) else chat.id

        await self.conn.execute('UPDATE chats SET timetable_photo = NOT timetable_photo WHERE id = $1', chat_id)

    @classmethod
    def from_keeper(cls) -> 'Database':
        """Получает объект Database используя подключение из ConnectionKeeper.

        Returns:
            Объект Database.
        """
        return Database(ConnectionKeeper.get_connection())
