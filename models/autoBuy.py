from engine.neural.neuNetClassifier import NeuNetClassifier
from engine.neural.operator import Operator
import engine.neural.neuNet as baseNet
import tensorflow as tf
import copy

config = copy.copy(baseNet.config)
config['usageThreshold'] = 0.93
config['inputSelector'] = 'autoBuyTrainingInput'

COLUMNS = [ 'days_sold_out', 'margin_ratio', 'places_left', 'sold_out_in',
    'stock_duration', 'tickets_bought', 'tickets_sold', 'turnover' ]

class AutoBuy(NeuNetClassifier):

    def __init__(self, atomicLock):
        self._config = config
        self._columns = COLUMNS
        super().__init__(atomicLock)

    def _declareNetwork(self):
        turnover = tf.contrib.layers.real_valued_column('turnover')
        tickets_bought = tf.contrib.layers.real_valued_column('tickets_bought')
        stock_duration = tf.contrib.layers.real_valued_column('stock_duration')
        margin_ratio = tf.contrib.layers.real_valued_column('margin_ratio')
        sold_out_in = tf.contrib.layers.real_valued_column('sold_out_in')
        days_sold_out = tf.contrib.layers.real_valued_column('days_sold_out')
        places_left = tf.contrib.layers.real_valued_column('places_left')
        tickets_sold = tf.contrib.layers.real_valued_column('tickets_sold')

        wide_columns = [
            turnover, tickets_bought, stock_duration, margin_ratio, sold_out_in,
            days_sold_out, places_left, tickets_sold
        ]

        deep_columns = [
          places_left,
          tickets_sold,
          tickets_bought,
          sold_out_in
        ]

        self.network = tf.contrib.learn.DNNLinearCombinedClassifier(
            model_dir=self._backupDir,
            linear_feature_columns=wide_columns,
            dnn_feature_columns=deep_columns,
            dnn_hidden_units=[100, 50])
