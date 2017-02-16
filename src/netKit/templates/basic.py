from engine.neural.neuNet${networkType} import NeuNet${networkType}
from engine.neural.operator import Operator
import engine.neural.neuNet as baseNet
import tensorflow as tf
import copy

config = copy.copy(baseNet.config)
config['usageThreshold'] = ${usageThreshold}
config['inputSelector'] = '${inputSelector}'

COLUMNS = ${columns}

class ${networkName}(NeuNet${networkType}):

    def __init__(self, atomicLock):
        self._config = config
        self._columns = COLUMNS
        super().__init__(atomicLock)

    def _declareNetwork(self):
${features}

        featureColumns = ${columnsWithoutApostrophe}

        self.network = tf.contrib.learn.${networkDepth}${networkType}(
            model_dir=self._backupDir,
            feature_columns=featureColumns,
            optimizer=tf.train.${optimizer}(learning_rate=${learningRate})
${neuronLayers})
