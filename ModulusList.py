import sys
from abc import ABCMeta, abstractmethod

class ModulusList:

	'''
	Maintains a list of (host, modulus, e) tuples.
	'''

	__metaclass__ = ABCMeta

	def __init__(self):
		self._modulusList = []

	@abstractmethod
	def add(self, host, modulus, e):
		pass

	@abstractmethod
	def length(self):
		pass

	@abstractmethod
	def __getitem__(self, index):
		pass

	@abstractmethod
	def saveListToFile(self, fileName):
		pass

	@abstractmethod
	def loadListFromFile(self, fileName):
		pass

class ModulusListImpl(ModulusList):

	def add(self, host, modulus, e):
		self._modulusList.append((host, modulus, e))

	def length(self):
		return len(self._modulusList)

	def __getitem__(self, index):
		return self._modulusList[index]

	def saveListToFile(self, fileName):
		saveFile = open(fileName, 'w')
		for record in self._modulusList:
			saveFile.write(str(record[0]) + '\n')
			saveFile.write(str(record[1]) + '\n')
			saveFile.write(str(record[2]) + '\n')
		saveFile.close()

	def loadListFromFile(self, fileName):
		loadFile = open(fileName, 'r')
		while True:
			host = loadFile.readline().rstrip()
			n = loadFile.readline().rstrip()
			e = loadFile.readline().rstrip()
			if not e: break
			self._modulusList.append((host, long(n), long(e)))
