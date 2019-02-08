import asyncio
from aiohttp import web
from .routes import init_routes
from .session import init_session

from .api import make_app as make_api

from .utils.config import init_config

from .modules.plugin import init_plugins
from .modules.logging import init_logging
from .modules.worker import init_workers
from .modules.docker import init_docker
from .modules.stacker import init_stacker



def make_app():

    loop = asyncio.get_event_loop()

    app = web.Application(loop=loop, debug=True)

    async def on_prepare(request, response):
        response.headers['Service-Worker-Allowed'] = '/'

    app.on_response_prepare.append(on_prepare)

    init_plugins(app)

    init_config(app)

    init_docker(app)

    init_stacker(app)

    # Init logging
    init_logging(app)

    init_workers(app)

    # Setup session
    init_session(app)

    # Setup routes
    init_routes(app)

    api = make_api(app)
    app.add_subapp('/api/v1', api)
    return app


async def gunicorn_app():
    return make_app()
