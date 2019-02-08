import aiohttp

from contextlib import asynccontextmanager

HUB_API_URL = 'https://hub.docker.com/v2/'


@asynccontextmanager
async def hub_api(username, password):
    headers = {
        "Content-Type": "application/json"
    }
    auth_payload = {
        "username": username,
        "password": password
    }

    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.post(HUB_API_URL + 'users/login/', json=auth_payload, headers=headers) as r:
            token = (await r.json(content_type=None))['token']

    client = aiohttp.ClientSession(raise_for_status=True, headers={'Authorization': 'JWT %s' % token})
    try:
        yield client
    finally:
        await client.close()


async def get_tags(login, password, user, repo):
    url = HUB_API_URL + 'repositories/{}/{}/tags/?page_size=100'.format(user, repo)
    async with hub_api(login, password) as client:
        async with client.get(url) as r:
            tag_resp = await r.json()
            return [k['name'] for k in tag_resp['results']]


