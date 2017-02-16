from engine.neural.operator import Operator
from engine.neural.modelHandler import ModelHandler

class NeuNetClassifier(Operator, ModelHandler):
    networkType = "classifier"

    def __init__(self, atomicLock):
        ModelHandler.__init__(self, self._config['progressive'])
        Operator.__init__(self, atomicLock)

    def _getAccuracy(self, meal):
        accuracyInfo = self.network.evaluate(input_fn=lambda: self._transformMeal(meal), steps=100)
        return accuracyInfo['accuracy']
