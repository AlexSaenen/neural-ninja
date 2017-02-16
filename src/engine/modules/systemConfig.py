from engine.module import Module
from engine.moduleManager import ModuleManager
import importlib

class SystemConfig(Module):

    def __init__(self, path="engine.config"):
        super().__init__(self.__class__.__name__)
        self.autoLoadable = True
        self._path = path
        self._config = {}

    def load(self):
        try:
            self._config = importlib.import_module(self._path).config
        except ImportError as error:
            self._logger.error("Couldn't load the config file at {0}".format(self._path))

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        self._config.clear()

    def set(self, key, value, override=True):
        if key in self._config and not override:
            raise RuntimeError("Cannot set {0}, it already exists and override is False".format(key))
        self._config[key] = value

    def get(self, key):
        if key not in self._config:
            return None
        return self._config[key]
