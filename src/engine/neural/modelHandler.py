from engine.neural.feeder import Feeder
from engine.neural.decorators import hungry, feedmethod, trained, accurate
from kernet.pathTools import Path
import tensorflow as tf

class ModelHandler(Feeder):

    def __init__(self, progressive):
        self._progressive = progressive
        self._backupDir = Path.fusion('/app/modelBackups', self.__class__.__name__, separator='/')
        self._lastKnownAccuracy = 0
        super().__init__()

    def _getAccuracy(self, meal):
        raise NotImplementedError("Class %s doesn't implement _getAccuracy()" % (self.__class__.__name__))

    @hungry
    @feedmethod
    @trained
    @accurate
    def predict(self, meal):
        return self.network.predict(input_fn=lambda: self._transformMeal(meal), as_iterable=False)

    @feedmethod
    @trained
    def accuracy(self, meal):
        if meal is None or 'label' not in meal:
            return self._lastKnownAccuracy
        return self._getAccuracy(meal)

    @hungry
    @feedmethod
    def train(self, meal):
        trainHelper = self.network.partial_fit if self._progressive else self.network.fit
        trainHelper(input_fn=lambda: self._transformMeal(meal), steps=200)
        self._lastKnownAccuracy = self._getAccuracy(meal)
