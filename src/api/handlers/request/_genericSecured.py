from tornado.web import asynchronous
from api.handlers.request._generic import GenericRequestHandler
from kernet.logger import Logger
import json

class GenericSecuredRequestHandler(GenericRequestHandler):

    def _verifyAPIKey(self):
        apiKey = None
        if 'body' in dir(self) and self.body is not None and 'skynetApiKey' in self.body:
            apiKey = self.body['skynetApiKey']
        else:
            apiKey = self.get_body_argument('skynetApiKey', default=None)

        if apiKey != 'skynetSuperSecretApiKey':
            raise RuntimeError("{} : Error, wrong access to the API without the correct key".format(self.request.uri))

    def _handleRequest(self, **routeParams):
        try:
            self._verifyAPIKey()
            GenericRequestHandler._handleRequest(self, **routeParams)
        except RuntimeError as error:
            Logger(self.__class__.__name__).error(error)
            self.write(str(error))
            self.finish()

    @asynchronous
    def get(self, **routeParams):
        self._handleRequest(**routeParams)

    @asynchronous
    def post(self, **routeParams):
        self._getBodyPayload()
        self._handleRequest(**routeParams)
