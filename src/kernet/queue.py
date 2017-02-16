from kernet.stack import threadsafe
from threading import Lock

class Queue(object):

    def __init__(self, queue=None):
        self._lock = Lock()
        self._queue = (queue if queue else list())

    @threadsafe
    def pop(self):
        return (self._queue.pop() if self._queue else None)

    @threadsafe
    def push(self, element):
        self._queue.append(element)

    @threadsafe
    def clear(self):
        del self._queue[:]

    @threadsafe
    def size(self):
        return len(self._queue)

    @threadsafe
    def flip(self):
        self._queue.reverse()
