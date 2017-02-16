from kernet.logger import Logger

def ifnotbooted(fn):
    def _booted(self):
        if not self.hasBooted:
            return fn(self)
    return _booted

def ifstopped(fn):
    def _stopped(self):
        if not self.isRunning:
            return fn(self)
    return _stopped

def ifrunning(fn):
    def _running(self):
        if self.isRunning:
            return fn(self)
    return _running

class Runnable(object):
    runnableFlow = "synchronous"

    def __init__(self, name):
        self._name = name
        self._logger = Logger(name)
        self.hasBooted = False
        self.isRunning = False
        self._logger.info('{0} instantiated'.format(self._name))

    @ifnotbooted
    def boot(self):
        self._logger.info('{0} is booting up'.format(self._name))
        self.hasBooted = True

    @ifstopped
    def run(self):
        self._logger.info('{0} is running'.format(self._name))
        self.isRunning = True

    @ifrunning
    def shutdown(self):
        self._logger.info('{0} is shutting down'.format(self._name))
        self.isRunning = False
