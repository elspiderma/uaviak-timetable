class ConfigError(Exception):
    """Базовый класс для исключений, связаных с конфиг-файлом.
    """
    pass


class NotFoundOption(ConfigError):
    """Не найден параметр."""
    def __init__(self, section: str, option: str):
        """
        Args:
            section: Секция конфигурации.
            option: Опция конфигурации.
        """
        self.section = section
        self.option = option

        super().__init__(f'No found option "{self.option}". Section: {self.section}')
