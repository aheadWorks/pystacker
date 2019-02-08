
async def resolve_all_stacks(field, info):
    c = info.context['app']['stacker']
    stacks = []
    async for stack in c.registry.list():
        stacks.append(stack)
    return stacks


async def resolve_one_stack(field, info, id):
    c = info.context['app']['stacker']
    return await(c.registry.load(id))

