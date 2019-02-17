import sys

class ModulusList():

	def __init__(self):
		self.modulusList = []

	def extendList(self, newList):
		self.modulusList.extend(newList)

	def addToList(self, item):
		self.modulusList.append(item)

	def getListLength(self):
		return len(self.modulusList)

	def getListElement(self, index):
		return self.modulusList[index]

	def saveListToFile(self, fileName):
		saveFile = open(fileName, 'w')
		for record in self.modulusList:
			saveFile.write(str(record[0]) + '\n')
			saveFile.write(str(record[1]) + '\n')
			saveFile.write(str(record[2]) + '\n')
		saveFile.close()

	def loadKeys(self, fileName):
		loadFile = open(fileName, 'r')
		while True:
			host = loadFile.readline().rstrip()
			n = loadFile.readline().rstrip()
			e = loadFile.readline().rstrip()
			if not e: break
			self.modulusList.append((host, long(n), long(e)))
