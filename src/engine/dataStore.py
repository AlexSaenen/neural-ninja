from kernet.queue import Queue
from kernet.stack import threadsafe

class DataStore(Queue):

    def __init__(self, route=None):
        super().__init__()
        self.route = route

    @threadsafe
    def size(self):
        return sum(len(packet) for packet in self._queue)
