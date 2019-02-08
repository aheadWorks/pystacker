from pystacker import make_app
from aiohttp import web

if __name__ == '__main__':
    app = make_app()
    web.run_app(app, port=app['config']['app']['port'], host=app['config']['app']['listen'])