from api.handlers.engine.networks import Upload
from api.handlers.engine.networks import GetAll
from api.handlers.routerHandler import RouterHandler
from api.handlers.request._genericSecured import GenericSecuredRequestHandler

class NetworksHandler(GenericSecuredRequestHandler):

    def initialize(self):
        router = RouterHandler()
        router.addHandler('getAll', GetAll())
        router.addHandler('upload', Upload())
        self.routers = [ router ]
