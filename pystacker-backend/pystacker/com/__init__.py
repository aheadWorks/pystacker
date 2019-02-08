from .host import name
from .dockerhub import tags_for_repo
from .json import compact
from .gc import garbage_collector


async def portmap(value, context, postfix):
    try:
        return {'value': "%s%s" % (context['id'], postfix)}
    except (TypeError, KeyError):
        return {'value': None}


async def not_match(value, context, pattern):
    if pattern not in value:
        return {'value': value}
    return {'value': None}



components = {
        'com.source.dockerhub.tags_for_repo': tags_for_repo,
        'com.source.host_name': name,
        'com.json.compact': compact,
        'com.registry.portmap': portmap,
        'com.text.not_match': not_match,

        'com.workers.garbage_collector': garbage_collector
    }