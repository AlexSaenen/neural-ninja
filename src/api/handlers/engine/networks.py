from api.handlers.actionHandler import ActionHandler, handler
from engine.moduleManager import ModuleManager

class Upload(ActionHandler):

    @handler
    def handle(self):
        requestFile = self._wrapper.request.files
        if 'networkFile' not in requestFile:
            self.callback({ 'error': 'Invalid form, no \'networkFile\' found' })
            return
        fileinfo = requestFile['networkFile'][0]
        try:
            fileEntry = open('./neunets/{}'.format(fileinfo['filename']), 'xb')
            fileEntry.write(fileinfo['body'])
            fileEntry.flush()
            fileEntry.close()
            self.callback({
                'error': None,
                'answer': 'Network uploaded successfully'
            })
        except Exception as error:
            self.callback({ 'error': str(error) })

class GetAll(ActionHandler):

    @handler
    def handle(self):
        watchers = ModuleManager.instance.get('NeuNet').getWatchers()
        self.callback({
            'error': None,
            'networks': [ str(net) for net in watchers ]
        })
