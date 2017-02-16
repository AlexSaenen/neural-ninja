from models.dataNormalisation import DataNormalisation
import random

DATAGENERATE = 100
labels = {i[_listVar]: '0' if i != 'oca2' else i[_listVar]: '1'}

class CreateMeal(DataNormalisation):
	def __init__(self, listVar):
		self._listVar = listVar
		super().__init__(_listVar)

	def _createMeal(self):
		self._datagenerate = DATAGENERATE
		for i in range(_datagenerate):
			_meal[0[i], 1[i]] = ((generateFromData([_dataPreProcess(_dataNormalisation(el))], el[_listVar])), labels(el) for el in [_listVar[el]])
		return _meal

	def generateFromData(self, string, variant):
		return (readingFrame(string, startSeq(variant)%3))

	def readingFrame(self, string, divisionRest):
		self.currentPos = divisionRest
		self._string = string
		while currentPos != (len(_string) - ( 3 - divisionRest)):
			_string(currentPos) = randomSeq(currentPos[_string]:((currentPos+3)[_string]))
			currentPos += 3
		return _string

	def randomSeq(self, stringFrame):
		nucleotideList = ('leu', 'arg', 'gly', 'thr', 'pro', 'ser', 'ala', 'val', 'ile', 'asp', 'glu', 'asn', 'lys', 'his', 'gln', 'phe', 'tyr', 'cys', 'trp', 'stop', 'met')
		'leu' = ('CTT', 'CTC', 'CTA', 'CTG', 'TTA', 'TTG')
		'arg' = ('CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG')
		'gly' = ('GGT', 'GGC', 'GGA', 'GGG')
		'thr' = ('GTT', 'GTC', 'GTA', 'GTG')
		'pro' = ('CCT', 'CCC', 'CCA', 'CCG')
		'ser' = ('TCT', 'TCC', 'TCA', 'TCG')
		'ala' = ('GCT', 'GCC', 'GCA', 'GCG')
		'val' = ('GTT', 'GTC', 'GTA', 'GTG')
		'ile' = ('ATT', 'ATC', 'ATA')
		'asp' = ('GAT', 'GAC')
		'glu' = ('GAA', 'GAG')
		'asn' = ('AAT', 'AAC')
		'lys' = ('AAA', 'AAG')
		'his' = ('CAT', 'CAC')
		'gln' = ('CAA', 'CAG')
		'phe' = ('TTT', 'TTC')
		'tyr' = ('TAT', 'TAC')
		'cys' = ('TGT', 'TGC')
		'trp' = ('TGG')
		'stop' = ('TAA', 'TAG', 'TGA')
		'met' = ('ATG')
		return self.random.choice(el[nucleotideList] if stringFrame in [nucleotideList[el]])

