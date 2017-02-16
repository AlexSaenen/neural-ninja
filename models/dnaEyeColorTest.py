from engine.neural.neuNetClassifier import NeuNetClassifier
from engine.neural.operator import Operator
from models.dnaEyeColor.dnaPreProcess import DNAPreProcess
from models.dnaEyeColor.createMeal import CreateMeal
import engine.neural.neuNet as baseNet
import tensorflow as tf
import copy

config = copy.copy(baseNet)
config['usageThreashold'] = 0.5
config['inputSelector'] = 'dnaEyeColorTrainingInput'

class DNAEyeColor(NeuNetClassifier):
	def __init__(self, atomickLock):
		self._config = config
		super().__init__(atomickLock)

	def _declareNetwork(self):
		self.network = tf.contrib.learn.DNNClassifier(
			model_dir=_backupDir,
			optimizer=tf.train.RMSPropOptimizer(learning_rate=0.01),
			hidden_units=[100, 50, 50]
			)
	def _transformMeal(self):
		meal = self._creatDataTraining()
		inputSelector = self._config['inputSelector']

		_input = [el[inputSelector] for el in meal]
		_labels = tf.constant([el['label'] for el in meal if 'label' in el])
		return _input, _labels