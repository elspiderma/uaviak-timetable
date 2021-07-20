from typing import TYPE_CHECKING

from aiohttp import web

if TYPE_CHECKING:
    from config import Configuration


class AbstractEndpoint:
    ENDPOINT: str = None
    METHOD = None

    def __init__(self, config: 'Configuration'):
        self.config = config

    def add_in_app(self, app: web.Application):
        app.add_routes([self.__class__.METHOD(self.ENDPOINT, self.run)])

    async def run(self, request: web.Request, *args, **kwargs) -> web.Response:
        return await self._endpoint(request, *args, **kwargs)

    async def _endpoint(self, request: web.Request) -> web.Response:
        raise NotImplemented


class AbstractEndpointApi(AbstractEndpoint):
    async def run(self, request: web.Request, *args, **kwargs) -> web.Response:
        token = request.headers.get('Authorization')
        if token in self.config.api_api_keys:
            return await self._endpoint(request, *args, **kwargs)

        response = web.json_response({'error': {'message': 'need authorization'}})
        response.set_status(401)
        return response
