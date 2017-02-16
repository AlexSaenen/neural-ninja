from kernet.task import Task
from kernet.logger import Logger
from threading import Thread, Event

class AsyncTask(Thread, Task):
    flow = "asynchronous"

    def __init__(self, timeout=1):
        self.mustDie = Event()
        self._timeout = timeout
        self._logger = Logger(self.__class__.__name__)
        Thread.__init__(self, target=self, name=self.__class__.__name__)
        Task.__init__(self)

    def execute(self):
        Task.execute(self)
        Thread.start(self)

    def run(self, args=None):
        raise NotImplementedError("Class %s doesn't implement run()" % (self.__class__.__name__))

    def shutdown(self):
        if not self.mustDie.isSet():
            self.mustDie.set()
        self.wait()

    def wait(self):
        if self.isAlive():
            self.join()
