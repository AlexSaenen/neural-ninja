from kernet.task import Task
from engine.moduleManager import ModuleManager

class RemoveNet(Task):

    def __init__(self, net):
        self._net = net
        super().__init__()

    def execute(self):
        ModuleManager.instance.get('NeuNet').removeNet(self._net)
