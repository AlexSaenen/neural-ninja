from engine.module import Module
from kernet.queue import Queue

class RequestsToHandle(Module, Queue):

    def __init__(self):
        Module.__init__(self, self.__class__.__name__)
        Queue.__init__(self)

    def load(self):
        self._logger.info("Loaded and ready to handle API requests")

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        self.clear()
