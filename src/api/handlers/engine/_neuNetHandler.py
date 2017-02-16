from api.handlers.actionHandler import ActionHandler
from engine.moduleManager import ModuleManager

class WatcherHandler(ActionHandler):

    def handle(self):
        watcher = ModuleManager.instance.get('NeuNet').getWatcher(self._wrapper.netName)
        if watcher is None:
            self.error = 'Network {} is not in the engine repository, {} cannot be executed'.format(self._wrapper.netName, self._wrapper.action)
        return watcher

class InstanceInteraction(WatcherHandler):

    def handle(self):
        self.error = None
        self.watcher = super().handle()
        if self.error or self.watcher is None:
            return None

        self.neuNetInstance = self.watcher.getNetworkInstance() if self.watcher.isLoaded else None
        errorMessage = 'Network {} is not running, {} cannot be executed'.format(self._wrapper.netName, self._wrapper.action)
        self.error = errorMessage if self.neuNetInstance is None or not self.watcher.isRunning else None

    def _convertOutput(self, output):
        if type(output) is dict and 'error' in output:
            return output
        return {
            'error': self.error,
            'answer': (output.tolist() if output.__class__.__name__ == 'ndarray' else (str(output) if output is not None else None))
        }
