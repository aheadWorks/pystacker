import pathlib
import yaml
import aiofile
import trafaret as t


SCHEMA = t.Dict({
    t.Key('id'): t.Int(),
    t.Key('uid'): t.String(max_length=32),
    t.Key('name'): t.String(),
    t.Key('from_template'): t.String(),
    t.Key('vars', optional=True): t.Dict(allow_extra='*'),
    t.Key('meta', optional=True): t.Dict(allow_extra='*'),
    t.Key('links', optional=True): t.Dict(allow_extra='*'),
    t.Key('other', optional=True): t.Dict(allow_extra='*')
})


class AIOFileResource:
    def __init__(self, p: pathlib.Path):
        self._f = p

    async def read(self):
        async with aiofile.AIOFile(self._f.absolute().as_posix()) as afp:
            return await afp.read()

    async def write(self, data):
        async with aiofile.AIOFile(self._f.absolute().as_posix()) as afp:
            await afp.write(data)
            return data

class StrResource:
    def __init__(self, st):
        self._str = st

    async def read(self):
        return self._str

    async def write(self, data):
        self._str = data
        return data



class InfoNode:
    def __init__(self, root: pathlib.Path):
        self._root = root

    async def load(self, *args):
        ret = {}
        for l in args:
            loader = l(self._root)
            ret.update(await loader.load())
        return ret


class OtherInfo:
    def __init__(self, path: pathlib.Path):
        self._path =  path / 'other.yml'

    async def load(self):
        async with aiofile.AIOFile(self._path.absolute().as_posix()) as afp:
            return yaml.load(await afp.read())

    async def save(self, obj):
        self._path.write_text(yaml.dump(obj, default_flow_style=False, default_style=''))


class StackerImageInfo:
    def __init__(self, path: pathlib.Path):
        self._path =  path / 'docker-compose.yml'

    async def load(self):
        async with aiofile.AIOFile(self._path.absolute().as_posix()) as afp:
            st = yaml.load(await afp.read())
            node = {}
            try:
                for k, v in st['services']['stacker']['labels'].items():
                    node[k.replace('com.stacker.', '')] = v
            except KeyError:
                node = {}
            return node

    async def save(self, obj):
        async with aiofile.AIOFile(self._path.absolute().as_posix()) as afp:
            st = yaml.load(await afp.read())
            st['services']['stacker'] = {
                'image': 'busybox',
                'labels': {('com.stacker.%s' % k): v for k, v in obj.items()}
            }
            self._path.write_text(yaml.dump(st, default_flow_style=False, default_style=''))


class StackerNodeInfo:
    """
    Get info from x-stacker note in docker-compose
    """
    def __init__(self, resource: pathlib.Path or str, key='x-stacker'):
        self._key = key
        if isinstance(resource, pathlib.Path):
            self._res = AIOFileResource(resource / 'docker-compose.yml')
        else:
            self._res = StrResource(resource)

    async def load(self):
        try:
            st = yaml.load(await self._res.read(), Loader=yaml.FullLoader)
            return st[self._key]
        except KeyError:
            return {}

    async def save(self, obj):
        st = yaml.load(await self._res.read())
        SCHEMA.check(obj)
        st[self._key] = obj
        return await self._res.write(yaml.dump(st, default_flow_style=False, default_style=''))

