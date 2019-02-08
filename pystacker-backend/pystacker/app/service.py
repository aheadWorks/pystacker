from ..utils.common import run_cmd
from ..modules.docker import AsyncDocker

class Service:

    def __init__(self, name: str, stack):
        self.name = name
        self.node = stack.config['services'][name]
        self.ports = self.init_ports()
        self.stack = stack

    def init_ports(self):
        if 'ports' not in self.node:
            return []
        return [p.split(':') for p in self.node['ports']]

    @property
    def image(self):
        if 'image' not in self.node:
            return False
        return self.node['image']




