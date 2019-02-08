import json
from collections import defaultdict
from aiohttp import web

from ..utils.common import Executor

class GarbageCollector:

    def __init__(self, stacker, docker):
        self.stacker = stacker
        self.docker = docker
        self.executor = Executor()

    def _get_label(self, info, label) -> str:
        labels = {l[0]: l[1] for l in map(lambda x: x.split("="), info['Labels'].split(','))}
        return labels[label]

    async def get_projects_with_volumes(self) -> dict:
        projects_volumes = defaultdict(lambda: [])
        cmd = "docker volume ls --filter='label=com.docker.compose.project' --format='{{json .}}' | grep " + self.stacker.stack_name()
        out, err, code = await self.executor.cmd(cmd)

        if not out:
            return {}

        for line in out.strip().split(b'\n'):
            info = json.loads(line)
            project_name = self._get_label(info, 'com.docker.compose.project')
            projects_volumes[project_name].append(info['Name'])

        return projects_volumes

    async def get_projects_containers(self) -> dict:
        """
        Get all containers (running and stopped)
        :return:
        """
        ids = defaultdict(lambda: [])
        for container in await self.docker.ps(all=True, filters='{"label": {"com.docker.compose.project":true}}'):
            if container['Labels']['com.docker.compose.project'].startswith(self.stacker.stack_name()):
                ids[container['Labels']['com.docker.compose.project']].append(container['Id'])
        return ids

    async def cleanup_containers(self):
        projects_with_containers = await self.get_projects_containers()
        names_existing = []
        async for stack in self.stacker.registry.list():
            names_existing.append(self.stacker.stack_name(stack.uid, stack.id))

        containers_cleaned = []
        for proj_name, containers in projects_with_containers.items():
            if proj_name not in names_existing:
                containers_cleaned += containers
                await self._rm_containers(*containers)
        return containers_cleaned

    async def cleanup_volumes(self):
        projects_with_volumes = await self.get_projects_with_volumes()
        names_existing = []
        async for stack in self.stacker.registry.list():
            names_existing.append(self.stacker.stack_name(stack.uid, stack.id))

        volumes_cleaned = []
        for proj_name, volumes in projects_with_volumes.items():
            if proj_name not in names_existing:
                volumes_cleaned += volumes
                await self._rm_volumes(*volumes)
        return volumes_cleaned

    async def _rm_containers(self, *args):
        for arg in args:
            await self.executor.cmd("docker rm -fv %s" % arg, raise_on_error=True)

    async def _rm_volumes(self, *args):
        for arg in args:
            await self.executor.cmd("docker volume rm %s" % arg, raise_on_error=True)

    async def prune_volumes(self):
        return await self.executor.cmd("docker volume prune -f", raise_on_error=True)

    async def prune_images(self):
        return await self.executor.cmd("docker image prune -f", raise_on_error=True)



async def garbage_collector(app: web.Application):
    gc = GarbageCollector(app['stacker'], app['docker'])

    app['logger'].info("Cleaning up orphaned containers")
    cc = await gc.cleanup_containers()
    if cc:
        app['logger'].info("Cleaned up %s" % ", ".join(cc))

    app['logger'].info("Cleaning up orphaned volumes")
    cv = await gc.cleanup_volumes()
    if cv:
        app['logger'].info("Cleaned up %s" % ", ".join(cv))

    app['logger'].info("Removing intermediate volumes and containers")
    await gc.prune_images()
    #await gc.prune_volumes()

    app['logger'].info("Cleaning up complete")


