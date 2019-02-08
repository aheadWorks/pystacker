
async def resolve_list_workers(root, info):
    return info.context['app']['workers']



