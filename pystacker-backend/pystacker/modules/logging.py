import logging
from aiohttp import web


def init_logging(app: web.Application):
    app['logger'] = logging.getLogger(__name__)
    app['logger'].setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    app['logger'].addHandler(ch)

