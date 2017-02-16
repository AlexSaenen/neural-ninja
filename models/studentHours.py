from engine.neural.neuNetRegressor import NeuNetRegressor
from engine.neural.operator import Operator
import engine.neural.neuNet as baseNet
import tensorflow as tf
import copy

config = copy.copy(baseNet.config)
config['usageThreshold'] = 0.93
config['inputSelector'] = 'studentHoursTrainingInput'

COLUMNS = [ 'hours' ]

class StudentHours(NeuNetRegressor):

    def __init__(self, atomicLock):
        self._config = config
        self._columns = COLUMNS
        super().__init__(atomicLock)

    def _declareNetwork(self):
        hours = tf.contrib.layers.real_valued_column('hours')

        wide_columns = [ hours ]

        self.network = tf.contrib.learn.LinearRegressor(
            model_dir=self._backupDir,
            feature_columns=wide_columns,
            optimizer=tf.train.RMSPropOptimizer(learning_rate=0.01)
        )
