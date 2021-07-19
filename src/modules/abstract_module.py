from typing import TYPE_CHECKING
from config import Configuration, IniReader

if TYPE_CHECKING:
    from argparse import Namespace


class AbstractModule:
    """Абстрактный модуль приложения.
    """
    def __init__(self, args: 'Namespace'):
        self.args = args

    def run(self) -> None:
        """Запускает модуль программы.
        """
        raise NotImplemented()


class AbstractConfigModule(AbstractModule):
    """Абстрактный модуль приложения, использующий конфигурацию.
    """
    def __init__(self, args: 'Namespace'):
        super().__init__(args)
        self.config = Configuration(IniReader.from_file(self.args.config))
