

async def resolve_force_worker(root, info, name):
    workers = [x for x in info.context['app']['workers'] if x.name == name]
    workers[0].force()
    return workers[0]