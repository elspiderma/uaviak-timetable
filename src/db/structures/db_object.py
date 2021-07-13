from abc import ABC
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from db import Database
    from asyncpg import Record


class DbObject(ABC):
    def __init__(self, db: 'Database' = None):
        self._db = db

    @classmethod
    def from_dict(cls, data: dict, db: 'Database' = None) -> 'DbObject':
        """
        Десериализация объекта из словаря.

        Args:
            data: Словарь.

        Returns:
            Десериализируеммый объект.
        """
        return cls(**data, db=db)

    @classmethod
    def from_record(cls, data: Union['Record', dict], db: 'Database' = None) -> 'DbObject':
        """
        Десериализация объекта из записи в БД.

        Args:
            data: Запись в БД.
            db: Клиент базы данных.

        Returns:
            Десериализируеммый объект.
        """
        data_dict = dict(data)
        return cls.from_dict(data_dict, db=db)
