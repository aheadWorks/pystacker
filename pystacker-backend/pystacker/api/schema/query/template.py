
async def resolve_get_template(field, info, name):
    c = info.context['app']['stacker']
    return c.templates.one(name)

async def all_templates_resolver(field, info):
    c = info.context['app']['stacker']
    return c.templates.all()