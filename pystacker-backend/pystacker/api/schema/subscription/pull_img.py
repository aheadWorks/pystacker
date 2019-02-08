import re

from graphql import GraphQLObjectType, GraphQLField, GraphQLString, GraphQLInt

pull_img_type = GraphQLObjectType(
    name="imagePullStatus",
    fields={
        'status': GraphQLField(GraphQLString),
        'service': GraphQLField(GraphQLString),
        'progressDetail': GraphQLField(GraphQLObjectType(
            name='imageProgress',
            fields={
                'current': GraphQLField(GraphQLInt),
                'total': GraphQLField(GraphQLInt),
            }
            )
        ),
        'id': GraphQLField(GraphQLString),
        'stack_id': GraphQLField(GraphQLInt)
    }
)


async def subscribe_pull_img(root, info, id):
    app = info.context['app']
    docker = app['docker']
    r = app['stacker'].registry
    stack = await r.load(id)
    for srv in stack.services.values():
        async for st in await docker.pull(srv.image, stream=True):
            # Skip status updates w/o id
            if ('id' not in st) or (not st['id']) or (not re.match("^[a-f0-9]+$", st['id'])):
                _id = -1

            else:
                _id = st['id']

            if 'progressDetail' in st and len(st['progressDetail'].keys()):
                _progress = st['progressDetail']
            else:
                _progress = {'total': 0, 'current': 0}

            r = {
                'status': st['status'],
                'service': srv.name,
                'progressDetail': _progress,
                'id': _id,
                'stack_id': id
            }
            yield r