from api.handlers.actionHandler import ActionHandler, handler
from netKit.creator import Creator

class Create(ActionHandler):

    @handler
    def handle(self):
        if 'body' not in dir(self._wrapper):
            self.callback({ 'error': 'NetKit needs a body, avoid to send data as a Form'})
            return

        body = self._wrapper.body
        networkCreator = Creator()
        try:
            networkCreator.configure(body)
            networkCreator.run()
            self.callback({
                'error': None,
                'answer': 'NetKit specs uploaded successfully'
            })
        except RuntimeError as error:
            self.callback({ 'error': 'NetKit failed creation: {}'.format(error) })
