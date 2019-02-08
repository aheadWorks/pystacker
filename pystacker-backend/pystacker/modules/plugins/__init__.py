import re



class Plugin:

    property_re = re.compile(r"[a-z0-9_]+")

    def register(self, path, plugin):
        """
        Add child plugin to node
        :param path:
        :param plugin:
        :return:
        """
        if not self.property_re.match(path):
            raise ValueError("Invalid child plugin name: %s" % path)
        if hasattr(self, path):
            raise ValueError("Child plugin with name already registered: %s" % path)

        _children = getattr(self, 'CHILDREN', [])
        _children.append(plugin)
        setattr(self, 'CHILDREN', _children)
        setattr(self, path, plugin)





class PluginManager(Plugin):

    def add(self, path, plugin):
        pass



class PluginConsumer():
    """
    Root plugins storage
    """
    plugins = PluginManager()





class PluginsRoot(Plugin):

    def __init__(self, *plugins):
        self.p = plugins

    def __getattr__(self, item):
        pass

    def init(self):
        # Init plugins. Start from less dots in root, finish with longest routes
        pass


import logging


class LoggerPlugin:

    NAME = 'log'

    def __init__(self):

        self.logger = logging.getLogger('pystacker')
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    def __getattr__(self, item):
        # Proxy all to logger
        return getattr(self.logger, item)

    def mount(self):
        self.plugins.register('log', self)


class LogAdvanced(PluginConsumer):

    NAME = 'log.advanced'

    def hi(self):
        print('hi')

    def mount(self):
        self.plugins.register(self)
