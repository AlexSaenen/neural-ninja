from kernet.task import Task
from engine.moduleManager import ModuleManager

class ReloadNet(Task):

    def __init__(self, net):
        self._net = net
        super().__init__()

    def execute(self):
        if self._net.isRunning:
            self._net.stopNetwork()
        if self._net.isLoaded:
            self._net.unload(isReloading=True)
        self._net.load()
        if self._net.isLoaded and self._net.getConfig('autoRun'):
            self._net.startNetwork()
