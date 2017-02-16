from engine.tasks.dataLoader import DataLoader
from engine.module import Module
from engine.moduleManager import ModuleManager

class TrainingDataStore(Module):

    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.autoLoadable = True
        self._stacks = []

    def load(self):
        tasks = [DataLoader(stack.route) for stack in self._stacks]
        ModuleManager.instance.getClass('Engine').stack().pushTask(tasks)

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        (stack.clear() for stack in self._stacks)

    def getAll(self):
        return self._stacks
