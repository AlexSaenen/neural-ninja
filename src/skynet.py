from kernet.runnable import Runnable
from engine.main import Engine
from kernet.decorators import getter
from api.main import Server
from collections import namedtuple
import time, os, threading

class Skynet(Runnable):
    _skynet = None

    def __init__(self):
        super().__init__(self.__class__.__name__)
        try:
            host = 'skynet.maestro-technology.com' if 'ENVIRONMENT' in os.environ and os.environ['ENVIRONMENT'] == 'production' else 'localhost'
            self._engine = Engine(killWatcher=self._reportKilled)
            self._api = Server(host=host, port=8080)
        except Exception as instantiateError:
            self._logger.error('instantiateError : {0}'.format(instantiateError))

    def boot(self):
        try:
            super().boot()
            self._engine.boot()
            self._api.boot()
        except Exception as bootError:
            self._logger.error('bootError : {0}'.format(bootError))

    def run(self):
        try:
            super().run()
            self._engine.start()
            self._api.run()
        except Exception as runError:
            self._logger.error('runError : {0}'.format(runError))

    def _reportKilled(self, **killInfo):
        if threading.current_thread() == threading.main_thread():
            killInfo = namedtuple('killInfo', killInfo.keys())(*killInfo.values())
            self.shutdown(gentle=not killInfo.wasUnexpected)
        else:
            self._api.shutdown()
            self._engine.mustDie.set()

    def shutdown(self, gentle=True):
        super().shutdown()
        if self._api.isRunning:
            self._api.shutdown()

        if self._engine.isRunning:
            self._engine.shutdown() if gentle else self._engine.die()

    @getter
    def instance(cls):
        if cls._skynet is None:
            cls._skynet = Skynet()
        return cls._skynet
