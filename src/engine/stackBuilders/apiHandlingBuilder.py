from kernet.stackBuilder import StackBuilder
from engine.tasks.apiHandler import APIHandler
from engine.moduleManager import ModuleManager

class APIHandlingBuilder(StackBuilder):

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def build(self):
        requestsToHandle = ModuleManager.instance.get('RequestsToHandle')
        return APIHandler() if requestsToHandle.size() > 0 else []
