

async def resolve_delete_stack(root, info, id) -> bool:
    st = info.context['app']['stacker']
    return await st.registry.delete(id)


async def resolve_create_stack(root, info, name, from_template, vars):
    vars = dict(vars)
    st = info.context['app']['stacker']
    template = st.templates.one(from_template)
    return await st.registry.create_from_template(name, template, vars)