from kernet.folderScanner import FolderScanner
from kernet.logger import Logger
from itertools import groupby
from operator import itemgetter

class FolderWatcher(object):

    def __init__(self, folder):
        self._registeredFiles = []
        self._logger = Logger(self.__class__.__name__)
        self._scanner = FolderScanner(folder)
        self._latestUpdatesNeeded = None

    def getUpdates(self):
        return self._latestUpdatesNeeded

    def getUpdatesByType(self):
        updates = self._latestUpdatesNeeded
        if updates is None:
            return {'new': [], 'remove': [], 'reload': []}
        updates.sort(key = itemgetter(1))
        groupedUpdates = groupby(updates, itemgetter(1))
        return [{'type':updateType, 'updates':[el[0] for el in update]} for updateType, update in groupedUpdates]

    def update(self):
        try:
            self._scanner.scan()
            if self._scanner.folderNeedsUpdate:
                self._latestUpdatesNeeded = self._scanner.analyseScan(self._registeredFiles)
        except OSError as error:
            self._logger.error("Error occurred when trying to access folder {0} : {1}".format(self._scanner._path, error))

    def outdate(self):
        del self._registeredFiles[:]
        self._scanner.clear()

    def getRegisteredFiles(self):
        return self._registeredFiles

    def registerFile(self, newFile):
        self._registeredFiles.append(newFile)

    def unregisterFile(self, fileToRemove):
        if fileToRemove in self._registeredFiles:
            self._registeredFiles.remove(fileToRemove)
