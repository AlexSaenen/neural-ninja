from kernet.stackBuilder import StackBuilder
from engine.tasks.dataLoader import DataLoader
from engine.moduleManager import ModuleManager

class TrainingDataBuilder(StackBuilder):

    def __init__(self, loadThreshold=2):
        super().__init__(self.__class__.__name__)
        self._threshold = loadThreshold

    def build(self):
        neuNetModule = ModuleManager.instance.get('NeuNet')
        watchers = neuNetModule.getWatchers()
        tasks = []
        loop = (watcher for watcher in watchers if watcher.isRunning and watcher.getConfig('autoTrainable'))
        for watcher in loop:
            batchSize = watcher.getConfig('batchSize')
            if watcher.getNetworkInstance().store.size() < batchSize * self._threshold:
                tasks.append(DataLoader(watcher))
        return tasks
