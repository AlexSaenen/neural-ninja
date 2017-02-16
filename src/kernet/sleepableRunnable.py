from kernet.killableRunnable import KillableRunnable

def ifawake(fn):
    def _awake(self):
        if self.isAwake:
            return fn(self)
    return _awake

def ifsleeping(fn):
    def _sleep(self):
        if not self.isAwake:
            return fn(self)
    return _sleep

class SleepableRunnable(KillableRunnable):

    def __init__(self, **params):
        self.isAwake = False
        super().__init__(**params)

    @ifawake
    def sleep(self):
        self._logger.info('{0} is going to sleep'.format(self._name))
        self.isAwake = False

    @ifsleeping
    def wake(self):
        self._logger.info('{0} is awake'.format(self._name))
        self.isAwake = True
