from tornado.web import RequestHandler, asynchronous
from collections import namedtuple
from kernet.logger import Logger
import json

class GenericRequestHandler(RequestHandler):

    def _getBodyPayload(self):
        decodedBody = self.request.body.decode('utf-8')
        contentType = self.request.headers.get('Content-Type')
        if decodedBody is not None and contentType in [None, 'application/json']:
            self.body = json.loads(decodedBody)

    def _pickRouter(self):
        return next((router for router in self.routers if router.servesRoute(self.action)), None)

    def _handleRequest(self, **routeParams):
        routeParams = namedtuple('routeParams', routeParams.keys())(*routeParams.values())
        for name in routeParams._fields:
            setattr(self, name, getattr(routeParams, name))
        activeRouter = self._pickRouter()
        Logger(self.__class__.__name__).info("Handling request {}".format(self.request.uri))
        activeRouter.handle(self.action, self)

    def __str__(self):
        return self.__class__.__name__

    @asynchronous
    def get(self, **routeParams):
        self._handleRequest(**routeParams)

    @asynchronous
    def post(self, **routeParams):
        self._getBodyPayload()
        self._handleRequest(**routeParams)
