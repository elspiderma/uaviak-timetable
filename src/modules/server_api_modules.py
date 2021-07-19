from typing import TYPE_CHECKING

from api import Server
from db import ConnectionKeeper
from modules import AbstractConfigModule

if TYPE_CHECKING:
    from argparse import Namespace


class ServerApiModules(AbstractConfigModule):
    def __init__(self, args: 'Namespace'):
        super().__init__(args)

        self.server = Server(self.config, self.args.debug)
        self.server.app.on_startup.append(self._on_start)
        self.server.app.on_shutdown.append(self._on_stop)

    async def _on_start(self, *args):
        await ConnectionKeeper.init_connection_from_config(self.config)

    async def _on_stop(self, *args):
        await ConnectionKeeper.close_connection()

    def run(self) -> None:
        self.server.run()
