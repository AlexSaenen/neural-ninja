from kernet.logger import Logger
from threading import Lock

def threadsafe(fn):
    def _locked(self, args=None):
        with self._lock:
            return fn(self, args) if args is not None else fn(self)
    return _locked

class Stack(object):

    def __init__(self):
        self._lock = Lock()
        self._tasks = []
        self._queuedTasks = []
        self._logger = Logger(self.__class__.__name__)
        self._builders = []

    def _namedBuilders(self):
        return [str(builder) for builder in self._builders]

    @threadsafe
    def _getTasks(self):
        return self._tasks

    @threadsafe
    def pushBuilder(self, builder):
        namedBuilders = self._namedBuilders()
        if str(builder) in namedBuilders:
            self._logger.error("The builder {0} already exists as a builder for this stack".format(builder))
        else:
            self._builders.append(builder)

    @threadsafe
    def popBuilder(self, builderName):
        namedBuilders = self._namedBuilders()
        try:
            idx = namedBuilders.index(builderName)
            self._builders.pop(idx)
        except ValueError:
            self._logger.error("Couldn't find a builder named {0}".format(builderName))

    @threadsafe
    def rebuildStack(self):
        del self._tasks[:]
        self._tasks.extend(self._queuedTasks)
        del self._queuedTasks[:]
        for builder in self._builders:
            newTasks = builder.build()
            if newTasks is not None:
                self._tasks.extend(newTasks) if type(newTasks) is list else self._tasks.append(newTasks)

    def runStack(self):
        asyncTasks = []
        tasks = self._getTasks()
        for task in tasks:
            if task.flow == "asynchronous":
                asyncTasks.append(task)
            task.execute()

        for asyncTask in asyncTasks:
            asyncTask.wait()

    @threadsafe
    def pushTask(self, task):
        self._queuedTasks.extend(task) if type(task) is list else self._queuedTasks.append(task)
