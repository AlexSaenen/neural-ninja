from api.handlers.actionHandler import ActionHandler, handler
from engine.moduleManager import ModuleManager

class Status(ActionHandler):

    @handler
    def handle(self):
        watchers = ModuleManager.instance.get('NeuNet').getWatchers()
        self.render('../views/status.html', watchers=watchers)
