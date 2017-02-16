from api.handlers.engine._neuNetHandler import WatcherHandler, InstanceInteraction
from api.handlers.actionHandler import handler

class Stop(InstanceInteraction):

    @handler
    def handle(self):
        super().handle()
        if self.error is None:
            try:
                self.watcher.stopNetwork()
                if self.watcher.isRunning:
                    self.error = "Network {} failed to stop".format(self._wrapper.netName)
            except RuntimeError as error:
                self.error = str(error)
            self.callback(self._convertOutput("Network {} successfully stopped".format(self._wrapper.netName)))
        else:
            self.callback(self._convertOutput(None))

class Start(WatcherHandler):

    @handler
    def handle(self):
        result = { 'error': None, 'answer': None }
        netName = self._wrapper.netName
        watcher = super().handle()
        if watcher is None:
            result['error'] = self.error
        else:
            try:
                watcher.startNetwork()
                if not watcher.isRunning:
                    result['error'] = "Network {} failed to start".format(netName)
                else:
                    result['answer'] = 'Network {} successfully started'.format(netName)
            except RuntimeError as error:
                result['error'] = str(error)
        self.callback(result)
