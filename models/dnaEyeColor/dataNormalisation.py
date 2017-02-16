from models.extractData import ExtractData
from models.dnaPreProcess import DNAPreProcess

LENDATASET = 3999
## must be divisible by 3

class DataNormalisation(ExtractData):
	def __init__(self, variant):
		self._variant = variant
		super().__init__(variant)

	def _dataNormalisation(self, variant):
		self._lenDataSet = LENDATASET
		self._startVar = startSeq(variant)
		self. _stopVar = stopSaq(variant)
		return ([extractData('oca2', 0, self._startVar)] + [extractData(self.variant, self._startVar, smallest(self._stopVar, self._lenDataSet))] + [extractData('oca2', smallest(self._stopVar, self._lenDataSet), self._lenDataSet)])

	def smallest(self, maxLenVar, maxLenDataSet):
		if maxLenVar < maxLenDataSet:
			return maxLenVar
		return maxLenDataSet
