import asyncpg
from typing import Optional


_connection: Optional[asyncpg.Connection] = None


class ConnectionNotInit(Exception):
    """Подключение к БД не инициализировано"""
    pass


async def init_connection(user: str, password: str, database: str, ip: str, **kwargs) -> None:
    """
    Инициализирует подключение к базе данных. Если оно уже существует, то переинициализирует его.

    Args:
        user: Пользователь.
        password: Пароль.
        database: Название базы данных.
        ip: Адрес СУБД.
        **kwargs: Дополнительные передаваемые параметры.
    """
    global _connection

    if _connection is not None:
        await close_connection()

    _connection = await asyncpg.connect(
        user=user,
        password=password,
        database=database,
        host=ip,
        **kwargs
    )


def get_connection() -> asyncpg.Connection:
    """
    Возвращает подключение к БД. Перед вызовом необходимо вызвать `init_connection`

    Returns:
        Подключение к БД.
    """
    global _connection

    if _connection is None:
        raise ConnectionNotInit('first you need execute init_connection')

    return _connection


async def close_connection():
    """Закрывает подключение к БД."""
    if _connection is None:
        raise ConnectionNotInit('first you need execute init_connection')

    await _connection.close()
