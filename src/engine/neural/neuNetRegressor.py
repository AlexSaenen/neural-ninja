from engine.neural.operator import Operator
from engine.neural.modelHandler import ModelHandler
import numpy as np

class NeuNetRegressor(Operator, ModelHandler):
    networkType = "regression"

    def __init__(self, atomicLock):
        ModelHandler.__init__(self, self._config['progressive'])
        Operator.__init__(self, atomicLock)

    def _diff(self, pred, label):
        absoluteSub = np.absolute(np.subtract(pred, label))
        average = np.mean(np.add(pred, label))
        return (absoluteSub / average)

    def _getAccuracy(self, meal):
        predictions = self.network.predict(input_fn=lambda: self._transformMeal(meal), as_iterable=False)
        correct_predictions = [el['label'] for el in meal]
        differences = [self._diff(pred, label) for (pred, label) in zip(predictions, correct_predictions)]
        accuracy = 1 - np.mean(differences)
        return accuracy
