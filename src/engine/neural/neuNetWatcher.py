from kernet.fileWatcher import FileWatcher
from kernet.folderScanner import FolderScanner
from kernet.classLoader import ClassLoader
from threading import Lock
from kernet.stack import threadsafe
from engine.neural.decorators import loaded, running, stopped
from kernet.decorators import getter

class NeuNetWatcher(FileWatcher):

    def __init__(self, fileName):
        self.isRunning = False
        self.hash = None
        self.file = None
        self.netClass = None
        self._lock = Lock()
        self._loader = ClassLoader(path='neunets')
        super().__init__(fileName)

    @threadsafe
    def load(self, autoStart=False):
        if self.isRunning:
            self._shutdown()
        try:
            self.hash = FolderScanner._md5hash('neunets', '{0}.py'.format(self._name))
            self.file = self._loader.loadFile(self._name) if self.file is None else self._loader.reload(self.file)
            self.netClass = ClassLoader.getClass(self.file)
            super().load()
            if autoStart:
                self._run()
        except ImportError as error:
            errorMessage = "Couldn't load the network neunets.{0} : {1}".format(self._name, error)
            super().onLoadError(errorMessage)

    def _shutdown(self):
        self.netClass._stop()
        self.isRunning = False

    def _run(self):
        ClassLoader.instantiateClass(module=self.file, params=self._lock)
        self.isRunning = True

    def getNetworkInstance(self):
        return (self.netClass.instance if self.netClass is not None else None)

    def getConfig(self, key=None):
        if self.file is None:
            return None
        return (self.file.config[key] if key is not None else self.file.config)

    @loaded
    def unload(self, isReloading):
        if self.isRunning:
            self._shutdown()
        if not isReloading:
            self.file = None
            self.netClass = None
        super().unload()

    @stopped
    def startNetwork(self):
        self._run()

    @running
    def stopNetwork(self):
        self._shutdown()

    def acquireLock(self):
        self._lock.acquire()

    def releaseLock(self):
        self._lock.release()
