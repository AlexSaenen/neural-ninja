from kernet.logger import Logger

class Module(object):

    def __init__(self, name):
        self._name = name
        self._logger = Logger(name)
        self.autoLoadable = True

    def __str__(self):
        return self._name

    def reload(self):
        raise NotImplementedError("Class %s doesn't implement reload()" % (self.__class__.__name__))

    def load(self):
        raise NotImplementedError("Class %s doesn't implement load()" % (self.__class__.__name__))

    def unload(self):
        raise NotImplementedError("Class %s doesn't implement unload()" % (self.__class__.__name__))
