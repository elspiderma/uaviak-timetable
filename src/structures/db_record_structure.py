from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import asyncpg


@dataclass
class DbRecordStructure:
    @classmethod
    def from_record_dict(cls, data: dict) -> 'DbRecordStructure':
        """
        Десериализация объекта из словаря.

        Args:
            data: Словарь.

        Returns:
            Десериализируеммый объект.
        """
        _TYPE_CONVERTERS = {
            Enum: lambda type_in_dataclass, v: type_in_dataclass(v)
        }

        def convert(val, type_in_dataclass):
            for type_, convertor in _TYPE_CONVERTERS.items():
                if issubclass(type_in_dataclass, type_):
                    return convertor(type_in_dataclass, val)

            raise TypeError(f'no converter for {type(type_in_dataclass)}')

        data = data.copy()
        for name_field_in_data in data:
            if name_field_in_data not in cls.__dataclass_fields__:
                raise ValueError(f'field {name_field_in_data} does not exist')

            type_in_dataclass = cls.__dataclass_fields__[name_field_in_data].type
            if not isinstance(data[name_field_in_data], type_in_dataclass):
                data[name_field_in_data] = convert(data[name_field_in_data], type_in_dataclass)

        return cls(**data)

    @classmethod
    def from_record(cls, data: 'asyncpg.Record') -> 'DbRecordStructure':
        """
        Десериализация объекта из записи в БД.

        Args:
            data: Запись в БД.

        Returns:
            Десериализируеммый объект.
        """
        return cls.from_record_dict(dict(data))
