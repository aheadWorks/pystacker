from pystacker.modules import worker
import asyncio
from unittest import mock
import pytest


@pytest.mark.asyncio
async def test_register_worker(event_loop):

    with mock.MagicMock(return_value=lambda: False) as fn:
        async def work():
            fn()

        w = worker.Worker(event_loop, work, timeout=0.1)
        w.start()
        await asyncio.sleep(0.12)

    fn.assert_called_once()
