from kernet.stackBuilder import StackBuilder
from engine.moduleManager import ModuleManager
from engine.tasks.newNet import NewNet
from engine.tasks.removeNet import RemoveNet
from engine.tasks.reloadNet import ReloadNet

class NeuNetBuilder(StackBuilder):

    def __init__(self, builderType):
        self._type = builderType
        taskByBuilderType = {'new': NewNet, 'remove': RemoveNet, 'reload': ReloadNet}
        if self._type not in taskByBuilderType:
            raise RuntimeError('The builderType {0} is not a valid NeuNetBuilder type'.format(self._type))
        self._taskConstructor = taskByBuilderType[self._type]
        super().__init__(self.__class__.__name__ + self._type)

    def build(self):
        realtimeNets = ModuleManager.instance.get('NeuNet').load(self._type)
        return [self._taskConstructor(net) for net in realtimeNets] if realtimeNets is not None else []
