from kernet.asyncTask import AsyncTask
from engine.moduleManager import ModuleManager

class APIHandler(AsyncTask):

    def __init__(self, timeout=2):
        super().__init__(timeout)

    def execute(self):
        requestsToHandle = ModuleManager.instance.get('RequestsToHandle')
        while requestsToHandle.size() > 0:
            request = requestsToHandle.pop()
            request.execute()
