import base64
from aiohttp import web
import aiodocker
from aiodocker.containers import DockerContainer

from typing import List


class AsyncDocker:
    """Async docker client based on aiodocker"""
    def __init__(self, username=None, password=None):
        self._auth = AsyncDocker.create_auth(username, password) if username else None
        self.client = aiodocker.Docker()

    @staticmethod
    def create_auth(username, password):
        return base64.b64encode(b"%b:%b" % (bytes(username, 'utf-8'), bytes(password, 'utf-8')))

    async def pull(self, from_image, **kwargs):
        if (from_image.count('/') == 1) and self._auth and 'auth' not in kwargs:
                kwargs['auth'] = self._auth
        if ':' not in from_image and 'tag' not in kwargs:
            from_image += ':latest'
        return await self.client.pull(from_image, **kwargs)

    async def ps(self, **kwargs) -> List[DockerContainer]:
        return await self.client.containers.list(**kwargs)

    async def close(self):
        return await self.client.close()


def init_docker(app: web.Application):

    async def init_docker(app):
        app['logger'].info('Starting docker client')
        app['docker'] = AsyncDocker(app['config']['docker']['hub_username'], app['config']['docker']['hub_password'])

    async def close_docker(app):
        app['logger'].info('Closing docker client')
        await app['docker'].close()

    app.on_startup.append(init_docker)
    app.on_cleanup.append(close_docker)
