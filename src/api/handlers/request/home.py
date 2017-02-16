from api.handlers.public.home import Home
from api.handlers.public.status import Status
from api.handlers.routerHandler import RouterHandler
from api.handlers.request._generic import GenericRequestHandler
from tornado.web import asynchronous

class HomeHandler(GenericRequestHandler):

    def initialize(self):
        homeRouter = RouterHandler()
        statusRouter = RouterHandler()
        homeRouter.addHandler(None, Home())
        statusRouter.addHandler('status', Status())
        self.routers = [ homeRouter, statusRouter ]
