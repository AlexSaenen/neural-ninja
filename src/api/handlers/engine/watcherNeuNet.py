from api.handlers.actionHandler import ActionHandler, handler
from api.handlers.engine._neuNetHandler import WatcherHandler
import os

class Load(WatcherHandler):

    @handler
    def handle(self):
        result = { 'error': None, 'answer': None }
        netName = self._wrapper.netName
        watcher = super().handle()
        if watcher is None:
            result['error'] = self.error
        else:
            try:
                watcher.load()
                if not watcher.isLoaded:
                    result['error'] = "Network {} failed to load".format(netName)
                else:
                    result['answer'] = 'Network {} successfully loaded'.format(netName)
            except RuntimeError as error:
                result['error'] = str(error)
        self.callback(result)

class Unload(WatcherHandler):

    @handler
    def handle(self):
        result = { 'error': None, 'answer': None }
        netName = self._wrapper.netName
        watcher = super().handle()
        if watcher is None:
            result['error'] = self.error
        else:
            try:
                watcher.unload()
                result['answer'] = 'Network {} successfully unloaded'.format(netName)
            except RuntimeError as error:
                result['error'] = str(error)
        self.callback(result)

class Delete(WatcherHandler):

    @handler
    def handle(self):
        result = { 'error': None, 'answer': None }
        netName = self._wrapper.netName
        watcher = super().handle()
        if watcher is None:
            result['error'] = self.error
        else:
            try:
                watcher.unload()
                os.remove('/app/src/neunets/{}.py'.format(watcher))
                result['answer'] = 'Network {} successfully deleted'.format(netName)
            except RuntimeError as error:
                result['error'] = str(error)
        self.callback(result)

class GetDetails(WatcherHandler):

    @handler
    def handle(self):
        result = { 'error': None, 'answer': None }
        netName = self._wrapper.netName
        watcher = super().handle()
        if watcher is None:
            result['error'] = self.error
        else:
            if not watcher.isLoaded:
                result['error'] = 'Network {} is not loaded'.format(netName)
            else:
                result['answer'] = watcher.getConfig()
        self.callback(result)
