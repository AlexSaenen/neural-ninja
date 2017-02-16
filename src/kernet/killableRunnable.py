from kernet.runnable import Runnable
from collections import namedtuple
import sys

class KillableRunnable(Runnable):

    def __init__(self, **params):
        params = namedtuple('params', params.keys())(*params.values())
        self._killMe = params.killWatcher
        super().__init__(params.name)

    def kill(self, **killInfo):
        killInfo['who'] = sys._getframe().f_back.f_code.co_name
        killDisplay = namedtuple('killInfo', killInfo.keys())(*killInfo.values())
        unexpectedly = "unexpectedly " if killDisplay.wasUnexpected else ""
        message = "{0} was {1}killed by {2} because {3}".format(self._name, unexpectedly, killDisplay.who, killDisplay.why)
        self._logger.warn(message)
        self._killMe(**killInfo)

    def die(self):
        self.shutdown()
        self._logger.warn("{0} died".format(self._name))
