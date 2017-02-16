from kernet.logger import Logger

class FileWatcher(object):

    def __init__(self, fileName):
        self.isLoaded = False
        self.loadError = None
        self._logger = Logger(self.__class__.__name__)
        self._name = fileName

    def load(self):
        self.isLoaded = True
        self.loadError = None

    def unload(self):
        self.isLoaded = False
        self.loadError = None

    def onLoadError(self, error):
        self.loadError = error
        self._logger.error(error)
        raise RuntimeError(error)

    def __str__(self):
        return self._name
