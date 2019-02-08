
async def resolve_services(stack, info):
    return stack.services.values()


async def resolve_status(service, info) -> int:
    docker = info.context['app']['docker']
    st = info.context['app']['stacker']

    states = {
        'running': 1,
        'exited': 0,
        'created': 0,
        'paused': -1,
        'not_exist': 0
    }

    for cont in await docker.ps(all=True):
        labels = cont['Labels']
        if 'com.docker.compose.project' in labels and labels['com.docker.compose.project'] == st.stack_name('%s_%s' % (service.stack.uid, service.stack.id)):
            if labels['com.docker.compose.service'] == service.name:
                return states[cont['State']]
    return states['not_exist']


