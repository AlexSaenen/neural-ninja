from api.handlers.engine.netKit import Create
from api.handlers.routerHandler import RouterHandler
from api.handlers.request._genericSecured import GenericSecuredRequestHandler

class NetKitHandler(GenericSecuredRequestHandler):

    def initialize(self):
        router = RouterHandler()
        router.addHandler('create', Create())
        self.routers = [ router ]
