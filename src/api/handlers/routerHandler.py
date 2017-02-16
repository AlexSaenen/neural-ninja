from api.subRouter import SubRouter
from engine.tasks.apiRequest import APIRequest
from engine.moduleManager import ModuleManager

class RouterHandler(SubRouter):

    def handle(self, route, request):
        handler = self.getHandler(route)
        apiRequestToHandle = APIRequest(handler, request)
        requestsToHandle = ModuleManager.instance.get('RequestsToHandle')
        requestsToHandle.push(apiRequestToHandle)
