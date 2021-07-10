import os

from config import IniReader, Configuration
from utils import ask_yes_no


def generate_simple_config(filename: str) -> None:
    """Генерирует пример конфиг-файла.

    Args:
        filename: Имя файла.
    """
    if os.path.isfile(filename):
        if not ask_yes_no('Overwrite?'):
            return

    ini_reader = IniReader()
    conf = Configuration(ini_reader)
    conf.generate_simple()
    conf.save(filename)
