from kernet.queue import Queue

def stream(fn):
    def _stream(self, args=None):
        if self._stream:
            return (fn(self, args) if args else fn(self))
        else:
            return None
    return _stream

class Serializer(object):

    def __init__(self):
        self._stream = None

    def openStream(self, path):
        if self._stream and self._stream.isopen():
            self.closeStream()
        self._stream = open(path, 'x')

    @stream
    def _writeLine(self, line):
        self._stream.write('{}\n'.format(line))

    @stream
    def _writeBlob(self, blob):
        for line in blob:
            self._stream.write('{}\n'.format(line))

    @stream
    def newLine(self):
        self._stream.write('\n')

    @stream
    def serialize(self, blob):
        self._writeBlob(blob) if isinstance(blob, list) else self._writeLine(blob)

    @stream
    def closeStream(self):
        self._stream.close()
