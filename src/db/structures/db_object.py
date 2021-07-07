import json
from abc import ABC
from typing import TYPE_CHECKING

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
    def from_json(cls, data: json, db: 'Database' = None) -> 'DbObject':
        """
        Десериализация объекта из JSON.

        Args:
            data: Строка в формате JSON.

        Returns:
            Десериализируеммый объект.
        """
        return cls.from_dict(json.loads(data), db=db)

    @classmethod
    def from_record(cls, data: 'Record', db: 'Database' = None) -> 'DbObject':
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
