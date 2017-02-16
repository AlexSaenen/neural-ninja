import tensorflow as tf
from threading import Lock

class Feeder(object):

    def _getData(self, foodElement, k):
        inputSelector = self._config['inputSelector']
        mealInput = foodElement[inputSelector]
        return (mealInput[k] if type(mealInput) is list else mealInput)

    def _transformMeal(self, meal):
        columns = self._columns
        columnLength = range(len(columns))

        _input = dict({ columns[k]: tf.constant([self._getData(el, k) for el in meal]) for k in columnLength })
        _labels = tf.constant([el['label'] for el in meal if 'label' in el])
        return _input, _labels
