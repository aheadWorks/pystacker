import asyncio
from aiofile import AIOFile
import pathlib
import yaml
import re

from ..utils.common import envsubst
from .service import Service
from .info import StackerNodeInfo


class ComposeTemplate:

    def __init__(self, path: str or pathlib.Path, name: (str or None)=None, components={}):
        p = pathlib.Path(path)
        if not p.exists():
            raise ValueError("{} does not exist".format(path))
        self.path = p
        self.name = name or self.path.name
        self._posix_variable = re.compile(r'\${([^\}]*)}')
        self._components = components

    async def validate(self) -> bool:
        cmd = 'docker-compose -f {} config'.format((self.path / 'docker-compose.yml').as_posix())
        ps = await asyncio.create_subprocess_shell(cmd, stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await ps.communicate()
        if ps.returncode:
            raise ValueError(stderr)
        return True

    async def get_other(self) -> dict:

        l = StackerNodeInfo(self.path)
        d = await l.load()

        skip_yml = ['docker-compose.yml', 'vars.yml']
        for n in [x for x in self.path.glob('*.yml') if x.name not in skip_yml]:
            async with AIOFile(str(n)) as afp:
                d[n.name.replace('.yml', '')] = yaml.load(await afp.read())
        return d

    async def get_ports(self) -> dict:
        async with AIOFile(self.path / 'docker-compose.yml') as afp:
            cfg = yaml.load(await afp.read())
        return {k: v['ports'] for k, v in cfg['services'].items() if 'ports' in v}

    async def _apply_component(self, variable: dict, type='source', *args):
        if not type in variable:
            return {}
        source = variable[type]
        if not isinstance(source, (list,)):
            _func_name, _raw_args, _func_args = re.findall(r'([^(]+)(\((.*)\))?', source)[0]
            _func_args = [x.strip() for x in _func_args.split(',')] if _func_args else []
            return await self._components[_func_name](*list(args) + list(_func_args))

        for f in source:
            _func_name, _raw_args, _func_args = re.findall(r'([^(]+)(\((.*)\))?', f)[0]
            _func_args = [x.strip() for x in _func_args.split(',')] if _func_args else []
            return await self._components[_func_name](*list(args) + list(_func_args))

    async def get_vars(self, app)-> dict:
        try:
            ni = StackerNodeInfo(self.path)
            all_vars = (await ni.load())['vars']
        except KeyError:
            async with AIOFile(self.path / 'vars.yml') as afp:
                all_vars = yaml.load(await afp.read())['vars']
        vars, runtime_vars = all_vars, {}

        async with AIOFile(self.path / 'docker-compose.yml') as afp:
            cfg = await afp.read()

        vars_from_compose = {m[1].split(':-', maxsplit=1)[0]: {} for m in self._posix_variable.finditer(cfg)}
        vars_from_compose.update(vars)
        for k in runtime_vars:
            del(vars_from_compose[k])

        vars = vars_from_compose

        for x in vars:
            vars[x].update(await self._apply_component(vars[x], 'source', app))

        return vars

    async def convert_to_yml(self, ctx=None, **variables) -> str:
        """
        Convert template to single docker-compose file text
        :param ctx: Context for filters
        :param variables: Variables to replace
        :return:
        """
        async with AIOFile(self.path / 'docker-compose.yml') as afp:
            compose_text = await afp.read()

        ni = StackerNodeInfo(self.path)
        info = await ni.load()
        compose_vars = info['vars']

        for k, v in compose_vars.items():
            compose_vars[k]['value'] = None
            # 1. Value = default if applicable
            if 'default' in v:
                compose_vars[k]['value'] = v['default']
            # 2. Override from kwargs
            if k in variables:
                compose_vars[k]['value'] = str(variables[k] if variables[k] else '').replace('$', '$$')
            # 3. Apply filters
            compose_vars[k].update(await self._apply_component(compose_vars[k], 'filters', compose_vars[k]['value'], ctx))

        # Replace vars
        repl = {k: v['value'] for k, v in compose_vars.items()}

        compose_text = envsubst(compose_text, **repl)
        processed = StackerNodeInfo(compose_text)
        w = await processed.load()
        w['vars'] = repl
        w['from_template'] = self.name
        w.update(ctx)
        compose_text = await processed.save(w)

        return compose_text


class Stack:

    def __init__(self, yml: pathlib.Path):
        self._lock = asyncio.Lock()

        self.yml = yml
        self.config = {}
        self.info_node = {}
        self.services = {}

    def __getattr__(self, name):
        try:
            return self.info_node[name]
        except KeyError:
            raise AttributeError

    async def init(self):
        async with AIOFile(self.yml.absolute().as_posix()) as afp:
            self.config = yaml.load(await afp.read())

        l = StackerNodeInfo(self.yml.parent)
        self.info_node = await l.load()

        self.services = self.init_services()

    def init_services(self) -> dict:
        return {name: Service(name, self) for name in self.config['services'].keys() if name != 'stacker'}



