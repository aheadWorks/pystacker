from ....utils.common import Executor
from graphql import GraphQLError

executor = Executor()


async def subscribe_run_cmd(root, info, id, cmd):
    logger = info.context['app']['logger']
    s = info.context['app']['stacker']
    r = s.registry
    stack = await r.load(id)

    logger.info("Running cmd %s for stack %s" % (cmd, id))
    async for lines in getattr(r, cmd)(stack):
        yield lines
    logger.info("Finished running cmd %s for stack %s" % (cmd, id))


async def subscribe_run_service_cmd(root, info, stack_id, service_name, cmd):
    docker = info.context['app']['docker']
    stacker = info.context['app']['stacker']
    stack = await stacker.registry.load(stack_id)

    for cont in await docker.ps():
        labels = cont['Labels']
        if 'com.docker.compose.project' in labels and labels['com.docker.compose.project'] == stacker.stack_name(stack.uid, stack.id):
            if labels['com.docker.compose.service'] == service_name:
                return executor.stream_all("docker exec " + cont['Id'] + " sh -c \"" + cmd+"\"")
    raise GraphQLError('Service %s for stack #%s not found' % (service_name, stack_id))
