from engine.module import Module
from kernet.folderWatcher import FolderWatcher

class NeuNet(Module):

    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.autoLoadable = False
        self.overwatch = FolderWatcher('neunets')

    def load(self, requestedType):
        self.overwatch.update()
        updatesByType = self.overwatch.getUpdatesByType()
        return next((updateGroup['updates'] for updateGroup in updatesByType if updateGroup['type'] is requestedType), None)

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        self.overwatch.outdate()

    def addWatcher(self, watcher):
        self._logger.info("Adding net {} to the engine repository".format(watcher))
        self.overwatch.registerFile(watcher)

    def getWatcher(self, net):
        watchers = self.getWatchers()
        return next((el for el in watchers if str(el) == net), None)

    def getWatchers(self):
        return self.overwatch.getRegisteredFiles()

    def removeNet(self, net):
        self._logger.info("Removing net {} from the engine repository".format(net))
        watcher = self.getWatcher(net)
        self.overwatch.unregisterFile(watcher)
