from threading import Thread, Event
from kernet.sleepableRunnable import SleepableRunnable

class ThreadyRunnable(Thread, SleepableRunnable):
    runnableFlow = "asynchronous"

    def __init__(self, **params):
        self.mustDie = Event()
        Thread.__init__(self, target=self, name=self.__class__.__name__)
        SleepableRunnable.__init__(self, **params)

    def start(self):
        SleepableRunnable.run(self)
        Thread.start(self)

    def run(self, args=None):
        raise NotImplementedError("Class %s doesn't implement run()" % (self.__class__.__name__))

    def shutdown(self):
        SleepableRunnable.shutdown(self)
        if not self.mustDie.isSet():
            self.mustDie.set()
        if self.isAlive():
            self.join()
