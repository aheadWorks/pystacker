
async def subscribe_get_logs(root, info, stack_id, service_name):
    docker = info.context['app']['docker']
    st = info.context['app']['stacker']

    stack = await st.registry.load(stack_id)

    for cont in await docker.ps():
        labels = cont['Labels']
        if 'com.docker.compose.project' in labels and labels['com.docker.compose.project'] == st.stack_name(stack.uid, stack.id):
            if labels['com.docker.compose.service'] == service_name:
                async for l in await cont.log(stdout=True, stderr=True, follow=True, tail=200):
                    yield l

