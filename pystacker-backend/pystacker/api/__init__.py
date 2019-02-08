from aiohttp import web
from .routes import init_routes


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response in (True, False, None):
            return web.Response()
        if response.status != 404:
            return response
        status = response.status
        message = response.message
    except web.HTTPException as ex:
        if ex.status == 500:
            raise
        message = ex.reason
        status = ex.status
    return web.json_response({'error': message}, status=status)


def make_app(app: web.Application):
    api = web.Application(middlewares=[error_middleware])

    api['config'] = app['config']
    api['logger'] = app['logger']
    api['stacker'] = app['stacker']
    api['workers'] = app['workers']

    async def init(api):
        api['docker'] = app['docker']

    api.on_startup.append(init)

    init_routes(api)

    return api
