from typing import TYPE_CHECKING

from db import ConnectionKeeper
from modules import AbstractConfigModule
from vk_bot import VkBot

if TYPE_CHECKING:
    from argparse import Namespace


class VkBotModules(AbstractConfigModule):
    def __init__(self, args: 'Namespace'):
        super().__init__(args)

        self.bot = VkBot(self.config)
        self.bot.loop_wrapper.on_startup.append(self._on_start())
        self.bot.loop_wrapper.on_shutdown.append(self._on_stop())

    async def _on_start(self) -> None:
        await ConnectionKeeper.init_connection_from_config(self.config)

    async def _on_stop(self) -> None:
        await ConnectionKeeper.close_connection()

    def run(self) -> None:
        self.bot.run()
