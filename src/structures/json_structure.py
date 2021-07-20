import json
from dataclasses import dataclass
from enum import Enum
from datetime import date


@dataclass
class JsonStructure:
    """Абстрактный класс, представляющий дата-класс, который можно сериализовать в JSON.
    """
    def to_json_dict(self) -> dict:
        """Сериализация дата-класса в словарь.

        Returns:
            Словарь.
        """
        _TYPE_CONVERTERS = {
            JsonStructure: lambda v: v.to_json_dict(),
            date: lambda v: v.isoformat(),
            Enum: lambda v: v.value,
            list: lambda v: [convert(i) for i in v],
            dict: lambda v: {k: convert(n) for k, n in v.items()},
            tuple: lambda v: tuple(convert(i) for i in v),
            int: lambda v: v,
            str: lambda v: v,
            bool: lambda v: v,
            type(None): lambda v: v
        }

        def convert(val):
            """Преобразование Python типов в Json-совместимые типы.

            Args:
                val: Значение в Py

            Returns:
                Значение в формате совместимым с JSON
            """
            for type_, converter in _TYPE_CONVERTERS.items():
                if isinstance(val, type_):
                    return converter(val)

            raise TypeError(f'no converter for {type(val)}')

        result = {k: n for k, n in self.__dict__.items() if not k.startswith('_')}

        for name_field, value_field in result.items():
            result[name_field] = convert(value_field)

        return result

    def to_json(self) -> str:
        """Сериализация дата-класса в JSON.

        Returns:
            JSON.
        """
        return json.dumps(self.to_json_dict())

    # TODO: form_json и from_json_dict
