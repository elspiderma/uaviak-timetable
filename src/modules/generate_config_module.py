import os

from config import IniReader, Configuration
from modules import AbstractModule
from utils import ask_yes_no


class GenerateConfigModule(AbstractModule):
    """Модуль, генерирующий пример конфиг-файла.
    """
    def run(self) -> None:
        """Генерирует пример конфиг-файла.

        Args:
            filename: Имя файла.
        """
        if os.path.isfile(self.args.config):
            if not ask_yes_no('Overwrite?'):
                return

        conf = Configuration(IniReader())
        conf.generate_simple()
        conf.save(self.args.config)
