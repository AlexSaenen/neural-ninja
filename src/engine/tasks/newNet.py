from kernet.task import Task
from engine.neural.neuNetWatcher import NeuNetWatcher
from engine.moduleManager import ModuleManager

class NewNet(Task):

    def __init__(self, net):
        self._net = net
        super().__init__()

    def execute(self):
        watcher = NeuNetWatcher(self._net)
        watcher.load()
        if watcher.isLoaded and watcher.getConfig('autoRun'):
            watcher.startNetwork()
        ModuleManager.instance.get('NeuNet').addWatcher(watcher)
