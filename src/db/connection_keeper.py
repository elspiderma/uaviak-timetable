import asyncpg
from typing import Optional


class ConnectionNotInit(Exception):
    """Подключение к БД не инициализировано"""
    pass


class ConnectionKeeper:
    _connection: Optional[asyncpg.Connection] = None

    @classmethod
    async def init_connection(cls, user: str, password: str, database: str, ip: str, **kwargs) -> None:
        """
        Инициализирует подключение к базе данных. Если оно уже существует, то переинициализирует его.

        Args:
            user: Пользователь.
            password: Пароль.
            database: Название базы данных.
            ip: Адрес СУБД.
            **kwargs: Дополнительные передаваемые параметры.
        """

        if cls._connection is not None:
            await cls.close_connection()

        cls._connection = await asyncpg.connect(
            user=user,
            password=password,
            database=database,
            host=ip,
            **kwargs
        )
        await cls._connection.execute('SET search_path TO public')

    @classmethod
    def get_connection(cls) -> asyncpg.Connection:
        """
        Возвращает подключение к БД. Перед вызовом необходимо вызвать `init_connection`

        Returns:
            Подключение к БД.
        """
        if cls._connection is None:
            raise ConnectionNotInit('first you need execute init_connection')

        return cls._connection

    @classmethod
    async def close_connection(cls) -> None:
        """Закрывает подключение к БД."""
        if cls._connection is None:
            raise ConnectionNotInit('first you need execute init_connection')

        await cls._connection.close()
        cls._connection = None
