from aiohttp import web


def init_routes(app):
    """
    Add routes to web app
    :param app:
    :return:
    """

    async def index(r):
        f = r.app['config']['path']['frontend_dir'] / 'index.html'
        return web.FileResponse(f)

    app.router.add_static('/css', app['config']['path']['frontend_dir'] / 'css', name='css')
    app.router.add_static('/js', app['config']['path']['frontend_dir'] / 'js', name='js')

    app.router.add_get('/', index)
    app.router.add_get('/stack/{a:.*}', index)
    app.router.add_get('/more/{a:.*}', index)