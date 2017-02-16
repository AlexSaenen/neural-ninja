from threading import Lock

class Task(object):
    flow = "synchronous"

    def __init__(self):
        self._name = self.__class__.__name__
        self._taskingLock = Lock()
        with self._taskingLock:
            self.isTasking = False

    def execute(self):
        with self._taskingLock:
            self.isTasking = True

    def __str__(self):
        return self._name
