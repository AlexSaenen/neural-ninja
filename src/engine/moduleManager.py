from kernet.logger import Logger
from kernet.classLoader import ClassLoader
from kernet.decorators import getter

class ModuleManager(object):
    _manager = None

    def __init__(self, path="engine.modules"):
        self._modules = []
        self._logger = Logger(self.__class__.__name__)
        self._instances = {}
        self._loader = ClassLoader(path=path)

    def _load(self, className):
        _loadedModule = self._loader.loadClass(className)
        if _loadedModule is not None:
            if _loadedModule.autoLoadable:
                _loadedModule.load()
            self._modules.append(_loadedModule)

    def get(self, moduleName):
        namedModules = [str(module) for module in self._modules]
        if moduleName not in namedModules:
            self._load(moduleName)
        return next((module for module in self._modules if str(module) == moduleName), None)

    def shutdown(self):
        (module.unload() for module in self._modules)

    def register(self, instance):
        self._instances[instance.__class__.__name__] = instance

    def unregister(self, className):
        if className in self._instances:
            del self._instances[className]

    def getClass(self, className):
        if className not in self._instances:
            raise RuntimeError('Class {0} did not register an instance'.format(className))
        return self._instances[className]

    @getter
    def instance(cls):
        if cls._manager is None:
            cls._manager = ModuleManager()
        return cls._manager
