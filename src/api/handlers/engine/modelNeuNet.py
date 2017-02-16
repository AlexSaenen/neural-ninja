from api.handlers.engine._neuNetHandler import InstanceInteraction
from api.handlers.actionHandler import ActionHandler, handler, body

class Train(InstanceInteraction):

    @handler
    @body
    def handle(self):
        super().handle()
        self.callback(self._convertOutput(None))
        if self.error is None:
            self.neuNetInstance.train(self._wrapper.body)

class Predict(InstanceInteraction):

    @handler
    @body
    def handle(self):
        super().handle()
        if self.error is None:
            result = self.neuNetInstance.predict(self._wrapper.body)
            self.callback(self._convertOutput(result))
        else:
            self.callback(self._convertOutput(None))

class Accuracy(InstanceInteraction):

    @handler
    def handle(self):
        super().handle()
        if self.error is None:
            food = self._wrapper.body if 'body' in dir(self._wrapper) else None
            result = self.neuNetInstance.accuracy(food)
            self.callback(self._convertOutput(result))
        else:
            self.callback(self._convertOutput(None))

class Usable(InstanceInteraction):

    @handler
    def handle(self):
        super().handle()
        if self.error is None:
            accuracy = self.neuNetInstance.accuracy()
            usageThreshold = self.neuNetInstance._config['usageThreshold']
            usable = (accuracy > usageThreshold if 'float' in type(accuracy).__name__ else False)
            self.callback(self._convertOutput(usable))
        else:
            self.callback(self._convertOutput(None))
