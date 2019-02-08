import json


async def compact(value, context):
    try:
        obj = json.loads(value)
        str = json.dumps(obj).replace(': ', ':')
        return {'value': str}
    except (json.JSONDecodeError, TypeError):
        return {'value': None}
