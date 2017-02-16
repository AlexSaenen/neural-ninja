from models.dataNormalisation import DataNormalisation

class ExtractData(variant):
	def __init__(self,string):
		self.variantsList = (oca2, v_1, v_2, v_x1, v_x2, v_x3, v_x4, v_x5, v_x6, v_x7, v_x7, v_x8, v_x9)
		super().__init__(string)

	def _extractData(self, variant, intStartingPoint, intStopingPoint):
		self.variantList('oca2') = (open(/models/dnaEyeColor/variants/oca2.py))
		self.variantList('v_1')  = (open(/models/dnaEyeColor/variants/variant1.py))
		self.variantList('v_2')  = (open(/models/dnaEyeColor/variants/variant2.py))
		self.variantList('v_x1') = (open(/models/dnaEyeColor/variants/variantx1.py))
		self.variantList('v_x2') = (open(/models/dnaEyeColor/variants/variantx2.py))
		self.variantList('v_x3') = (open(/models/dnaEyeColor/variants/variantx3.py))
		self.variantList('v_x4') = (open(/models/dnaEyeColor/variants/variantx4.py))
		self.variantList('v_x5') = (open(/models/dnaEyeColor/variants/variantx5.py))
		self.variantList('v_x6') = (open(/models/dnaEyeColor/variants/variantx6.py))
		self.variantList('v_x7') = (open(/models/dnaEyeColor/variants/variantx7.py))
		self.variantList('v_x8') = (open(/models/dnaEyeColor/variants/variantx8.py))
		self.variantList('v_x9') = (open(/models/dnaEyeColor/variants/variantx9.py))
		return self.variantList(variant(intStartingPoint:intStopingPoint))

	def startSeq(self, string):		
		self.variantsList.oca2.starting_point = 0
		self.v_1.starting_point = 111
		self.v_2.starting_point = 111
		self.v_x1.starting_point = 1359
		self.v_x2.starting_point = 139
		self.v_x3.starting_point = 1357
		self.v_x4.starting_point = 1358
		self.v_x5.starting_point = 1356
		self.v_x6.starting_point = 1358
		self.v_x7.starting_point = 1358
		self.v_x8.starting_point = 1361
		self.v_x9.starting_point = 1361
		return [el[variantsList]].starting_point if el in string

	def stopSeq(self,string):
	##	_oca2Len = (27719008 - 28099342)
		self.oca2.ending_point = LENDATASET
		self.v_1.ending_point = 2627
		self.v_2.ending_point = 2555
		self.v_x1.ending_point = 3941
		self.v_x2.ending_point = 2697
		self.v_x3.ending_point = 3897
		self.v_x4.ending_point = 3868
		self.v_x5.ending_point = 3824
		self.v_x6.ending_point = 3802
		self.v_x7.ending_point = 3733
		self.v_x8.ending_point = 3391
		self.v_x9.ending_point = 3232
		return [el[variantsList]],ending_point if el in string
