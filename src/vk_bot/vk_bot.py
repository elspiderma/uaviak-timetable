from typing import TYPE_CHECKING

from vkbottle import Bot, LoopWrapper

from vk_bot import routers

if TYPE_CHECKING:
    from config import Configuration
    from vkbottle.bot import Blueprint


class VkBot:
    BLUEPRINTS: tuple['Blueprint'] = (
        routers.bp_base,
        routers.bp_setting,
        routers.bp_timetable
    )

    def __init__(self, config: 'Configuration') -> None:
        self.config = config

        self.loop_wrapper = LoopWrapper()
        self.bot = Bot(token=config.vk_bot_token, loop_wrapper=self.loop_wrapper)

        self._init_blueprint()

    def _init_blueprint(self) -> None:
        for i in self.BLUEPRINTS:
            i.load(self.bot)

    def run(self) -> None:
        self.bot.run_forever()
