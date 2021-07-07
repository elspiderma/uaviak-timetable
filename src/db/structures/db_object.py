from typing import TYPE_CHECKING
from abc import ABC
import json

if TYPE_CHECKING:
    from db import Database
    from asyncpg import Record


class DbObject(ABC):
    def __init__(self, db: 'Database'):
        self.db = db

    @classmethod
    def from_dict(cls, data: dict) -> 'DbObject':
        """
        Десериализация объекта из словаря.

        Args:
            data: Словарь.

        Returns:
            Десериализируеммый объект.
        """
        return cls(**data)

    @classmethod
    def from_json(cls, data: json):
        """
        Десериализация объекта из JSON.

        Args:
            data: Строка в формате JSON.

        Returns:
            Десериализируеммый объект.
        """
        return json.loads(data)

    @classmethod
    def from_record(cls, data: 'Record') -> 'DbObject':
        """
        Десериализация объекта из записи в БД.

        Args:
            data: Запись в БД.

        Returns:
            Десериализируеммый объект.
        """
        data_dict = dict(data)
        return cls.from_dict(data_dict)
