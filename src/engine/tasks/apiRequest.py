from kernet.asyncTask import AsyncTask

class APIRequest(AsyncTask):

    def __init__(self, handler, request, timeout=2):
        super().__init__(timeout)
        self._handler = handler
        self._req = request

    def run(self):
        self._handler.handle(self._req)
