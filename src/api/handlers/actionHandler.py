import tornado
from tornado.ioloop import IOLoop

def body(fn):
    def _body(self):
        if 'body' in dir(self._wrapper):
            return fn(self)
        else:
            self.callback({
                "error": 'Network {} requires a body, {} cannot be executed'.format(self._wrapper.netName, self._wrapper.action)
            })
            return None
    return _body


def handler(fn):
    def _handler(self, wrapper):
        self._wrapper = wrapper
        fn(self)
    return _handler

class ActionHandler(object):

    def handle(self, request):
        raise NotImplementedError("Class %s doesn't implement handle()" % (self.__class__.__name__))

    def callback(self, result=None):
        IOLoop.instance().add_callback(self._callback, result)

    def render(self, htmlPath, **settings):
        IOLoop.instance().add_callback(self._render, htmlPath, **settings)

    def _callback(self, result=None):
        if result is not None:
            self._wrapper.write(result)
        self._wrapper.finish()

    def _render(self, htmlPath, **settings):
        self._wrapper.render(htmlPath, **settings)

    def __str__(self):
        return self.__class__.__name__
