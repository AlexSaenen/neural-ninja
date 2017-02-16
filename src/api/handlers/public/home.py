from api.handlers.actionHandler import ActionHandler, handler

class Home(ActionHandler):

    @handler
    def handle(self):
        self.render('../views/home.html')
