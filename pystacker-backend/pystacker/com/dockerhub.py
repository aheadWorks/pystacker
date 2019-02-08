from ..utils.docker import get_tags


async def tags_for_repo(app, user, repo, match=None, rmatch=None):
    login = app['config']['docker']['hub_username']
    password = app['config']['docker']['hub_password']

    tags = [t for t in await get_tags(login, password, user, repo) if
            (not rmatch or rmatch not in t) and (not match or match in t)]

    tags.sort(reverse=True)
    app['logger'].info("Got {tags} tags for dockerhub repo {repo}".format(tags=len(tags), repo=repo))

    return {'options': tags, 'default': tags[0]}

