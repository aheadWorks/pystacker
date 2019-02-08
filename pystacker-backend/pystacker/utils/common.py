import asyncio
from collections.abc import AsyncIterable, Mapping
import re

from typing import Tuple, Dict


async def run_cmd(cmd: str) -> AsyncIterable:
    buf = b''
    ps = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while True:
        out = asyncio.create_task(ps.stdout.read(1024))
        err = asyncio.create_task(ps.stderr.read(1024))
        done, pending = await asyncio.wait({out, err}, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        for task in done:
            r = task.result()
            buf += r
            yield buf.decode()
        if not r:
            break


async def run_cmd2(cmd: str) -> Tuple[bytes, bytes, int]:
    ps = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await ps.communicate()
    return stdout, stderr, ps.returncode


def envsubst(data: str, **kwargs) -> str:
    """
    Substitute variables from kwargs in data using envsubst format, with default support
    :param data:
    :param kwargs:
    :return:
    """
    for m in re.findall(r'\${([^}]+)}', data):
        value = None
        key = m
        if ':-' in m:
            key, value = (m.split(':-'))
        if key in kwargs:
            value = kwargs[key] or ''
        regex = re.compile(r'\${' + re.escape(m) + '[^}]*}')
        if value is not None:
            data = re.sub(regex, value, data)
    return data


def deep_update(d, u, strict=False):
    """
    Deep update the dict
    :param d:
    :param u:
    :param strict: raise ValueError if mapping going to be replaced with scalar
    :return:
    """
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = deep_update(d.get(k, {}), v, strict=strict)
        else:
            if(strict):
                print(k, d)
            if strict \
                    and (k in d) \
                    and (
                        (isinstance(d[k], Mapping) and not isinstance(v, Mapping))
                        or (not isinstance(d[k], Mapping) and isinstance(v, Mapping))
                    ):
                raise ValueError(
                    "Can't update scalar value to mapping and vice-versa at key '%s' cause it already has value" % k
                )
            d[k] = v
    return d


class Executor:

    def __init__(self):
        self._lock = asyncio.Lock()

    async def cmd(self, cmd, raise_on_error=False, lock=None):
        if not lock:
            lock = self._lock
        async with lock:
            out, err, code = await run_cmd2(cmd)
            if not raise_on_error or not code:
                return out, err, code
            raise OSError(err)

    async def stream_all(self, cmd, lock=None):
        if not lock:
            lock = self._lock
        async with lock:
            async for cmd_res in run_cmd(cmd):
                yield cmd_res