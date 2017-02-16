from kernet.stackBuilder import StackBuilder
from engine.moduleManager import ModuleManager
from engine.tasks.trainNet import TrainNet

class TrainBuilder(StackBuilder):

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def build(self):
        neuNetModule = ModuleManager.instance.get('NeuNet')
        watchers = neuNetModule.getWatchers()
        tasks = []
        for watcher in watchers:
            watcher.acquireLock()
            if watcher.isRunning and watcher.getNetworkInstance().store.size() > 0:
                tasks.append(TrainNet(watcher))
            watcher.releaseLock()
        return tasks
