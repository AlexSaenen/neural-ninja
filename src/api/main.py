from kernet.runnable import Runnable
from collections import namedtuple
from api.handlers.request.networks import NetworksHandler
from api.handlers.request.neunet import NeuNetHandler
from api.handlers.request.home import HomeHandler
from api.handlers.request.netKit import NetKitHandler
import tornado, os
from tornado import httpserver
from tornado.ioloop import IOLoop

WebApplication = tornado.web.Application
StaticFileHandler = tornado.web.StaticFileHandler
HTTPServer = httpserver.HTTPServer

class Server(Runnable, WebApplication):

    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port
        Runnable.__init__(self, self.__class__.__name__)
        WebApplication.__init__(self, default_host=self._host,
            template_path=os.path.join(os.path.dirname(__file__), "views")
        )

        self._httpModule = HTTPServer(self, xheaders=True)

    def boot(self):
        Runnable.boot(self)
        WebApplication.add_handlers(self, r'{}'.format(self._host), [
            (r'/networks/(?P<action>[A-Za-z]+)', NetworksHandler),
            (r'/network/(?P<action>[A-Za-z]+)', NetKitHandler),
            (r'/network/(?P<netName>[A-Za-z]+)/(?P<action>[A-Za-z]+)', NeuNetHandler),
            (r'/(?P<action>[A-Za-z]+)?', HomeHandler),
            (r'/assets/(.*)', StaticFileHandler, {'path': '/app/src/api/assets/'})
        ])

    def run(self):
        Runnable.run(self)
        self._httpModule.bind(port=8080)
        self._httpModule.start(num_processes=1)
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            self._logger.warn("Server was killed, shutting down")

    def shutdown(self):
        Runnable.shutdown(self)
        IOLoop.current().stop()
