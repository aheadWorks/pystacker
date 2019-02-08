from aiohttp import web
import aiohttp
import json

from graphql import graphql, parse

from .graphql import schema

from ..app.stack import ComposeTemplate

from graphql.subscription import subscribe
from graphql import ExecutionResult



async def graphql_query(request: web.Request) -> web.Response:
    """
    For query/mutation methods
    :param request:
    :return:
    """
    if request.method == "POST":
        q = await request.text()
    else:
        q = request.rel_url.query['query']
    resp = await graphql(schema, q, context_value={'app': request.app})
    if resp.errors:
        raise web.HTTPBadRequest(reason="; ".join([str(k) for k in resp.errors]))
    return web.json_response(resp.data)


async def graphql_subscribe(request: web.Request):
    """
    For subscription method - websocket
    :param request:
    :return:
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    close_args = {}
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                payload = json.loads(msg.data)
                q = payload['query']
                subscription_result = await subscribe(schema, parse(q), context_value={'app': request.app})
                if isinstance(subscription_result, ExecutionResult):
                    close_args = dict(code=aiohttp.WSCloseCode.UNSUPPORTED_DATA, message=";".join([str(k) for k in subscription_result.errors])[0:100])
                    await ws.close(**close_args)
                    return
                else:
                    async for resp in subscription_result:
                        if resp.errors:
                            close_args = dict(message="; ".join([str(k) for k in resp.errors])[0:100], code=aiohttp.WSCloseCode.PROTOCOL_ERROR)
                            await ws.close(**close_args)
                            return ws
                        await ws.send_json(resp.data)
                    await ws.close()
                    return ws
            except (Exception) as e:
                close_args = dict(message="Error: %s" % str(e)[0:100],
                               code=aiohttp.WSCloseCode.PROTOCOL_ERROR)
                await ws.close(**close_args)
                return ws

        if msg.type == aiohttp.WSMsgType.ERROR:
            close_args=dict(message="Websocket connection closed with exception %s" % ws.exception(), code=aiohttp.WSCloseCode.PROTOCOL_ERROR)
    await ws.close(**close_args)
    return ws



async def preview_stack(request: web.Request) -> web.Response:
    j = await request.json()
    tpl = j['id']
    t = ComposeTemplate( request.app['config']['path']['templates_dir'] / tpl)
    yml = await t.convert_to_yml(**j['vars'])

    return web.json_response({'yml': yml})




