class StackBuilder(object):

    def __init__(self, name):
        self._name = name

    def build(self):
        raise NotImplementedError("Class %s doesn't implement build()" % (self.__class__.__name__))

    def getName(self):
        return self._name

    def __str__(self):
        return self._name
