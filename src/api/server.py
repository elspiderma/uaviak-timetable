from aiohttp import web


class Server:
    def __init__(self):
        self.aiohttp_application = web.Application()

    def run(self):
        web.run_app(self.aiohttp_application, host='localhost')
