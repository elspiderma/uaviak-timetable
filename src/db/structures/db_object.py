from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from asyncpg import Record


class DbObject:
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
    def from_record(cls, data: Union['Record', dict]) -> 'DbObject':
        """
        Десериализация объекта из записи в БД.

        Args:
            data: Запись в БД.

        Returns:
            Десериализируеммый объект.
        """
        data_dict = dict(data)
        return cls.from_dict(data_dict)

    @classmethod
    def from_records(cls, data: Union[list['Record'], list[dict]]) -> list['DbObject']:
        return [cls.from_record(i) for i in data]
