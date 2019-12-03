import re
import pathlib
import asyncio
import shortuuid
import shlex
from contextlib import asynccontextmanager

from .stack import ComposeTemplate, Stack
from ..utils.common import Executor


class Registry():

    def __init__(self, path: pathlib.Path, *, prefix: str = 'stacker_', min_id: int = 10, max_id: int = 99):
        self.path = path
        self.stack_id_re = re.compile("^[0-9]+$")

        self._lock = asyncio.Lock()
        self._executor = Executor()

        self._max_id = int(max_id)
        self._min_id = int(min_id)
        self.prefix = prefix

        self._statuses = {}


    def reserve_id(self, ids):
        for sid in ids:
            try:
                (self.path / str(sid)).mkdir(parents=True)
                return sid
            except FileExistsError:
                pass
        raise Exception("No free IDs left")

    @asynccontextmanager
    async def bind_id(self):
        """
        Context manager to reserve stack id
        :return:
        """
        async with self._lock:
            try:
                current_ids = [x for x in self.path.iterdir() if x.is_dir() and self.stack_id_re.match(x.name)]
            except OSError:
                current_ids = []
            available_ids = [x for x in range(self._min_id, self._max_id) if x not in current_ids]
            new_id = self.reserve_id(available_ids)
        try:
            yield str(new_id)
        finally:
            if new_id and not len(list((self.path / str(new_id)).glob('*'))):
                (self.path / str(new_id)).rmdir()

    async def create_from_template(self, name: str, tpl: ComposeTemplate, vars: dict):
        async with self.bind_id() as sid:
            if not name or not len(name.strip()):
                name = "stack_%s" % sid
            compose_yml = await tpl.convert_to_yml(ctx={
                'id': sid,
                'uid': shortuuid.ShortUUID(alphabet="qwertyuiopasdfghjklzxcvbnm").random(length=8),
                'name': name
            }, **vars)
            (self.path / sid / 'docker-compose.yml').write_text(compose_yml)
            return await self.load(sid)

    async def load(self, id: str or int) -> Stack:
        try:
            yml = (self.path / str(id) / 'docker-compose.yml')
            stack = Stack(yml)
            await stack.init()
            return stack
        except FileNotFoundError:
            raise FileNotFoundError("Stack #%s not found at %s" % (id, self.path))

    async def delete(self, id: int) -> bool:
        for f in (self.path / str(id)).glob('*'):
            f.unlink()
        (self.path / str(id)).rmdir()
        return True

    async def list(self):
        for sp in self.path.glob('*'):
            yield await self.load(sp.name)

    async def _run_compose(self, stack: Stack, cmd: str, env: None or dict=None):
        if env:
            env = " ".join(["%s=%s" % (shlex.quote(k), shlex.quote(v)) for k, v in env.items()])
        else:
            env = ""

        cmd = "COMPOSE_HTTP_TIMEOUT=180 {env} docker-compose --no-ansi -p {prefix}{uid}_{id} -f {yml} {cmd}".format(
            env=env, prefix=self.prefix, uid=stack.uid, id=stack.id, yml=stack.yml, cmd=cmd
        )

        async for cmd_res in self._executor.stream_all(cmd, lock=stack._lock):
            yield cmd_res

    def up(self, s: Stack, env: None or dict=None):
        return  self._run_compose(s, "up --force-recreate -d", env)

    def down(self, s: Stack):
        return self._run_compose(s, "down")

    def pause(self, s: Stack):
        return self._run_compose(s, "pause")

    def unpause(self, s: Stack):
        return self._run_compose(s, "unpause")

    async def destroy(self, s: Stack):
        async for cmd_res in self._run_compose(s, "down -v"):
            yield cmd_res
        await self.delete(s.id)
