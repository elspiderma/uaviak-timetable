import asyncio

from aiohttp import web
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import Configuration


class Server:
    def __init__(self, config: 'Configuration', debug: bool = False):
        self.config = config
        self.app = web.Application(debug=debug)

    def run(self):
        web.run_app(app=self.app,
                    host=self.config.api_listen_adders,
                    port=self.config.api_port)
