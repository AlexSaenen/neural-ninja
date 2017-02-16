from kernet.threadyRunnable import ThreadyRunnable
from kernet.stack import Stack
from engine.moduleManager import ModuleManager
from engine.stackBuilders.neuNetBuilder import NeuNetBuilder
# from engine.stackBuilders.trainingDataBuilder import TrainingDataBuilder
# from engine.stackBuilders.trainBuilder import TrainBuilder
from engine.stackBuilders.apiHandlingBuilder import APIHandlingBuilder
from collections import namedtuple

class Engine(ThreadyRunnable):

    def __init__(self, **params):
        params = namedtuple('params', params.keys())(*params.values())
        super().__init__(name=self.__class__.__name__, killWatcher=params.killWatcher)
        self._stack = Stack()
        ModuleManager.instance.register(self)

    def boot(self):
        super().boot()
        self.wake()
        for builderType in ['new', 'remove', 'reload']:
            self._stack.pushBuilder(NeuNetBuilder(builderType))
        # self._stack.pushBuilder(TrainingDataBuilder())
        # self._stack.pushBuilder(TrainBuilder())
        self._stack.pushBuilder(APIHandlingBuilder())

    def run(self):
        while not self.mustDie.isSet():
            self._stack.rebuildStack()
            self._stack.runStack()

    def shutdown(self):
        super().shutdown()
        self.isAwake = False

    def stack(self):
        return self._stack
