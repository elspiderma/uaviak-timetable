import configparser
from configparser import ConfigParser
from typing import Union

from config import AbstractReader, TypesValue, NotFoundOption


class IniReader(AbstractReader):
    """Класс, представляющий читателя ini файла.
    """
    DELIMITER_LIST = ','  # Разделитель элементов в списке.

    def __init__(self, confparser: ConfigParser = None):
        """
        Args:
            confparser: Свой объект `ConfigParser`, если не задан, создается автоматически.
        """
        if confparser:
            self.confparser = confparser
        else:
            self.confparser = ConfigParser()

    def get(self, section: str, option: str, type_value: TypesValue) -> Union[int, str, list, None]:
        """Получает значение из конфигурации.

        Args:
            section: Категория.
            option: Имя значения.
            type_value: Тип значения

        Returns:
            Запрашиваемое значение.

        Raises:
            NotFoundOption - опция не найдена
            TypeError - неудалось найти такой тип
        """
        try:
            value = self.confparser.get(section, option)
            if not value:
                return None

            if type_value == TypesValue.STRING:
                return value
            elif type_value == TypesValue.INT:
                return int(value)
            elif type_value == TypesValue.LIST:
                return value.split(self.DELIMITER_LIST)
            else:
                raise TypeError('Config not support this type.')
        except configparser.NoOptionError:
            raise NotFoundOption(section, option)
        except configparser.NoSectionError:
            raise NotFoundOption(section, option)

    def set(self, section: str, option: str, value: Union[int, str, list, None]) -> None:
        """Изменяет/создает значение конфигурации.

        Args:
            section: Категория.
            option: Имя значения.
            value: Новое значение.

        Raises:
            TypeError - тип значения не поддерживается
        """
        if section not in self.confparser:
            self.confparser.add_section(section)

        if isinstance(value, str):
            self.confparser.set(section, option, value)
        elif isinstance(value, int):
            self.confparser.set(section, option, str(value))
        elif isinstance(value, list):
            self.confparser.set(section, option, self.DELIMITER_LIST.join([str(i) for i in value]))
        elif value is None:
            self.confparser.set(section, option, '')
        else:
            raise TypeError('Config not support this type.')

    @classmethod
    def from_file(cls, filename: str) -> 'IniReader':
        """Чиатет кинфигурацию из файла.

        Args:
            filename: Имя файла.
        """
        confparser = ConfigParser()

        with open(filename, 'r') as f:
            confparser.read_file(f)

        return cls(confparser)

    def write_file(self, filename: str) -> None:
        """Сохраняет конфигурцию в файл.

        Args:
          filename: Имя файла.
        """
        with open(filename, 'w') as f:
            self.confparser.write(f)
