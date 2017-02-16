from kernet.logger import Logger
from kernet.pathTools import Path
import importlib

class ClassLoader(object):

    def __init__(self, path, instantiate=True):
        self._path = path
        self._instantiate = instantiate
        self._logger = Logger(self.__class__.__name__)

    def loadClass(self, className):
        _fileName = Path.convert(className, toClass=False)
        self._logger.info("Loading module {} from {}".format(className, Path.fusion(self._path, _fileName)))
        try:
            _module = self.loadFile(_fileName)
            return (ClassLoader.instantiateClass(_module, className) if self._instantiate else ClassLoader.getClass(_module, className))
        except ImportError:
            self._logger.error("Couldn't load the module {} at {}".format(className, Path.fusion(_filePath, _fileName)))
            return None

    def loadFile(self, fileName):
        _filePath = Path.fusion(self._path, fileName)
        return importlib.import_module(_filePath)

    def loadSource(self, fileName, moduleName):
        _filePath = Path.fusion(self._path, fileName, '/')
        fileLoader = importlib.machinery.SourceFileLoader(moduleName, _filePath)
        return fileLoader.get_source(moduleName)

    @staticmethod
    def reload(module):
        return importlib.reload(module)

    @staticmethod
    def getClass(module, className=None):
        if className is None:
            _moduleName = Path.extractModuleName(module.__name__)
            className = Path.convert(_moduleName, toClass=True)
        return getattr(module, className)

    @staticmethod
    def instantiateClass(module, className=None, params=None):
        _class = ClassLoader.getClass(module, className)
        return (_class(params) if params is not None else _class())
