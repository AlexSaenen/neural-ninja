from engine.neural.neuNet import NeuNet
from engine.neural.decorators import feedmethod, trained, accurate
from engine.dataStore import DataStore
from engine.moduleManager import ModuleManager
from kernet.pathTools import Path
from kernet.decorators import getter
import tensorflow as tf

class Operator(NeuNet):

    def __init__(self, atomicLock):
        self.store = self._instantiateDataStore()
        super().__init__(atomicLock)
        ModuleManager.instance.register(self)

    @classmethod
    def _stop(cls):
        _network = cls.instance
        _network.stop()
        ModuleManager.instance.unregister(cls.__name__)

    @getter
    def instance(cls):
        try:
            return ModuleManager.instance.getClass(cls.__name__)
        except RuntimeError:
            return None

    @classmethod
    def _instantiateDataStore(cls):
        return DataStore()
