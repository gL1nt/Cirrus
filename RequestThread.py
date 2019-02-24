from abc import ABCMeta, abstractmethod
import threading
from IPTools import *
from ModulusList import *

class requestThread(threading.Thread):

	__metaclass__ = ABCMeta

	def __init__(self, threadID, name, counter, params):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.resultList = ModulusListImpl()
		self.params = params

	def getResultList(self):
		return self.resultList

	@abstractmethod
	def run(self):
		pass

class requestThreadIPRange(requestThread):
	
	def __doIPRange(self, start, end, count, timeout):
		'''
		Configure thread to start scanning at IP=start, scan every 'count'
		addresses and not scan past 'end'.
		'''
		curIP = IPToInteger(start)
		endIP = IPToInteger(end)
		while curIP <= endIP:
			strIP = IntegerToIP(curIP)
			modulus = 0
			e = 0
			try:
				params = getModulus(strIP, timeout)
				modulus = params[0]
				e = params[1]
			except:
				curIP = curIP + count
				continue
			if modulus != 0:
				self.resultList.add(strIP, modulus, e)	
			curIP = curIP + count

	def run(self):
		start = self.params[0]
		end = self.params[1]
		count = self.params[2]
		timeout = self.params[3]
		self.__doIPRange(start, end, count, timeout)

class requestThreadHostList(requestThread):

	def __doList(self, hostList, start, end, count, timeout):
		'''
		Configure thread to scan every 'count' elements of a list of hosts
		starting at 'start' index and not going past 'end' index.
		'''
		curIndex = start
		while curIndex <= end:
			modulus = 0
			e = 0
			try:
				params = getModulus(hostList[curIndex], timeout)
				modulus = params[0]
				e = params[1]
			except:
				curIndex = curIndex + count
				continue
			if modulus != 0:
				self.resultList.add(hostList[curIndex], modulus, e)
			curIndex = curIndex + count

	def run(self):
		hostList = self.params[0]
		start = self.params[1]
		end = self.params[2]
		count = self.params[3]
		timeout = self.params[3]
		self.__doList(hostList, start, end, count, timeout)
