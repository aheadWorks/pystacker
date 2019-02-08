from aiohttp import web
from ..app.registry import Registry
from ..app.stack import ComposeTemplate
import pathlib
from ..com import components


class FsStorage:
    def __init__(self, path: pathlib.Path, constructor, glob:str='*', **kwargs):
        self._path = path
        self._kwargs = kwargs
        self._constructor = constructor
        self._glob = '*'

    def one(self, name):
        return self._constructor(self._path / name, **self._kwargs)

    def all(self):
        return list([self.one(t.name) for t in self._path.glob(self._glob)])


class Stacker:

    def __init__(self, *, config, components: dict):

        # Private
        self._id = config['app']['id']

        # Public
        self.components = components
        self.templates = FsStorage(config['path']['templates_dir'], ComposeTemplate, components=self.components)
        self.registry = Registry(config['path']['data_dir'] / 'stacks', prefix=self._id + "_", min_id=config['app']['min_id'], max_id=config['app']['max_id'])

    def stack_name(self, *args):
        return self._id + '_' + "_".join(map(str, args))


def init_stacker(app: web.Application):

    app['stacker'] = Stacker(
        config=app['config'],
        components=components
    )
