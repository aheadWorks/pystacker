import asyncio
from aiohttp import web
import traceback


class Worker:
    """
    Regular async function executor
    """
    def __init__(self, loop, worker: asyncio.coroutine, timeout: float):
        self._loop = loop
        self._waiter = asyncio.Event()
        self._worker = worker
        self._future = None

        self.interval = timeout

    @property
    def name(self):
        return self._worker.__name__

    def start(self, *args, **kwargs):
        """
        Start worker with params
        :param args:
        :param kwargs:
        :return:
        """
        self._future = self._loop.create_task(self._run(*args, **kwargs))

    async def stop(self):
        """
        Shutdown worker
        :return:
        """
        self._future.cancel()
        await self._future

    def force(self):
        """
        Force worker to execute
        :return:
        """
        self._waiter.set()

    async def _run(self, *args, **kwargs):
        while True:
            try:
                await asyncio.wait_for(self._waiter.wait(), timeout=self.interval, loop=self._loop)
            except asyncio.TimeoutError:
                pass
            await self._worker(*args, **kwargs)
            self._waiter.clear()


def init_workers(app: web.Application):
    app['workers'] = []

    async def register_workers(app):
        stacker = app['stacker']
        for w in app['config']['workers']:
            fn = stacker.components[w['name']]
            name = w['name']

            async def worker(*args, **kwargs):
                try:
                    app['logger'].info('Worker {name} is running'.format(name=name))
                    return await fn(*args, **kwargs)
                except Exception as e:
                    app['logger'].error("Worker {name} raised unhandled exception: {}".format(e, name=name))
                    app['logger'].error(traceback.format_exc())
                finally:
                    app['logger'].info('Worker {name} exited'.format(name=name))
            worker.__name__ = w['name']
            app['workers'].append(Worker(app.loop, worker, w['interval']))

        for w in app['workers']:
            app['logger'].info("Worker %s started" % w.name)
            w.start(app)

    async def unregister_workers(app):
        for w in app['workers']:
            try:
                await w.stop()
            except asyncio.CancelledError as e:
                app['logger'].info("Worker %s canceled" % w.name)

    app.on_startup.append(register_workers)
    app.on_shutdown.append(unregister_workers)
