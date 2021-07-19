from typing import TYPE_CHECKING
from config import Configuration, IniReader

if TYPE_CHECKING:
    from argparse import Namespace


class AbstractModule:
    def __init__(self, args: 'Namespace'):
        self.args = args

    def run(self) -> None:
        raise NotImplemented()


class AbstractConfigModule(AbstractModule):
    def __init__(self, args: 'Namespace'):
        super().__init__(args)
        self.config = Configuration(IniReader.from_file(self.args.config))
