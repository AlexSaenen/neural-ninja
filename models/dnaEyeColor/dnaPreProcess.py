from engine.task.dataLoader import DataLoader
import modules.dataGenerator as string
import engine.neural.decorators as _decorators
import tensorflow as ts  

class DNAPreProcess(DataNormalisation):
	def __init__(self, string):
		super.__init__(string)

	def _dataPreProcess(self, normedData):
		lenSeq = LENDATASET
		for [el[string]] in range(lenSeq)
			try:
				arrayOfChar.append(_convertToArray[el[string]])
			except ValueError as error:
				self.logger.error(error)
		self._decorators.feed(arrayOfChar)

	def _convertToArray(self, letter):
		transpileMap = ['a', 'c', 't', 'g']
		if letter.lower() in transpileMap:
			return (letter.lower())
		raise ValueError('Input data format error : letter: \" {} \"'.format(letter))


