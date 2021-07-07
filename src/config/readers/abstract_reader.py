from abc import ABC
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from config import TypesValue


class AbstractReader(ABC):
    """Класс, представляющий читателя файла.
    """
    def get(self, section: str, option: str, type_value: 'TypesValue') -> Union[int, str, list, None]:
        """Получает значение из конфигурации.

        Args:
            section: Категория.
            option: Имя значения.
            type_value: Тип значения.

        Returns:
            Запрашиваемое значение.

        Raises:
            NotFoundOption - опция не найдена
            TypeError - неудалось найти такой тип
        """
        raise NotImplemented

    def set(self, section: str, option: str, value: Union[int, str, list, None]) -> None:
        """Изменяет/создает значение конфигурации.

        Args:
            section: Категория.
            option: Имя значения.
            value: Новое значение.

        Raises:
            TypeError - тип значения не поддерживается
        """
        raise NotImplemented

    @classmethod
    def from_file(cls, filename: str) -> 'AbstractReader':
        """Чиатет кинфигурацию из файла.

        Args:
            filename: Имя файла.
        """
        raise NotImplemented

    def write_file(self, filename: str) -> None:
        """Сохраняет конфигурцию в файл.

        Args:
            filename: Имя файла.
        """
        raise NotImplemented
