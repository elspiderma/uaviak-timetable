from typing import TYPE_CHECKING

from aiohttp import web

if TYPE_CHECKING:
    from config import Configuration


class Server:
    """Сервер web api.
    """
    def __init__(self, config: 'Configuration', debug: bool = False):
        """
        Args:
            config: Конфигурация приложения.
            debug: Если `True`, то запускается в режиме отладки.
        """
        self.config = config
        self.app = web.Application(debug=debug)

    def run(self):
        """Запуск сервера.
        """
        web.run_app(app=self.app,
                    host=self.config.api_listen_adders,
                    port=self.config.api_port)
