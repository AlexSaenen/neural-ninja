class DataPacket(object):

    def __init__(self, json=None):
        self._jsonObj = json

    def set(self, json):
        self._jsonObj = json

    def get(self):
        return self._jsonObj

    def __len__(self):
        return len(self._jsonObj)
