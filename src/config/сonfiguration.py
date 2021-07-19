from typing import TYPE_CHECKING, Optional

from config import TypesValue

if TYPE_CHECKING:
    from config import AbstractReader


class Configuration:
    """Класс, представляющий конфигурацию приложения.
    """

    # Структура конфигурации.
    _CONFIG_STRUCTURE = {
        'postgres': {
            'login': {'type': TypesValue.STRING, 'simple': 'login db'},
            'password': {'type': TypesValue.STRING, 'simple': 'password db'},
            'ip': {'type': TypesValue.STRING, 'simple': 'ip db'},
            'database': {'type': TypesValue.STRING, 'simple': 'database name'}
        },
        'vk_api': {
            'token': {'type': TypesValue.STRING, 'simple': 'api token'},
            'admin_ids': {'type': TypesValue.LIST, 'simple': ['00001', '00002']}
        },
        'api': {
            'api_keys': {'type': TypesValue.LIST, 'simple': ['key1', 'key2']},
            'listen_adders': {'type': TypesValue.STRING, 'simple': '0.0.0.0'},
            'port': {'type': TypesValue.INT, 'simple': 8888}
        }
    }

    def __init__(self, reader: 'AbstractReader'):
        self._reader = reader

    def save(self, filename: str) -> None:
        """Сохраняет файл на диск.

        Args:
            filename: Имя файла.
        """
        self._reader.write_file(filename)

    def generate_simple(self) -> None:
        """Генерирует конфигурацию-пример.
        """
        for section, options in self._CONFIG_STRUCTURE.items():
            for option, option_prop in options.items():
                self._reader.set(section, option, option_prop['simple'])

    @classmethod
    def _get_section_and_option_by_name_attr(cls, s: str) -> Optional[tuple[str, str]]:
        """Разделяет секцию и опцию в строке в формате {section}_{option}.

        Args:
            s: Строка в формате {section}_{option}.

        Returns:
            Секция и название опции, если такая секция или опция не найдена, то возвращает None
        """
        option_name_worlds = s.split('_')

        section_name_worlds = []
        section_name_worlds += [option_name_worlds.pop(0)]

        # Так как имя секции тоже может сожержать "_",
        # то сперва мы считаем, что имя секции идет до первого "_", потом до 2 "_" и т.д.
        while len(option_name_worlds) != 0:
            section = '_'.join(section_name_worlds)
            option = '_'.join(option_name_worlds)

            if section in cls._CONFIG_STRUCTURE and option in cls._CONFIG_STRUCTURE[section]:
                return section, option

            section_name_worlds += [option_name_worlds.pop(0)]

        return None

    def __getattr__(self, item: str):
        """Возвращает значение опции по ключу {section}_{option}.

        Args:
            item: Ключ.

        Returns:
            Значение опции.

        Raises:
            AttributeError -- опция не найдена.
        """
        section_option = self._get_section_and_option_by_name_attr(item)
        if not section_option:
            raise AttributeError()

        return self._reader.get(section_option[0],
                                section_option[1],
                                self._CONFIG_STRUCTURE[section_option[0]][section_option[1]]['type'])
