import threading
import argparse
import sys
from IPTools import *
from ModulusList import ModulusList

def scanIPRange(fromIP, toIP, threads, timeout):
	'''
	Preform multi-threaded IP range scanning.
	'''
	threadArr = []
	for i in range(0, threads):
		threadIPStart = IntegerToIP(IPToInteger(fromIP) + i) 
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

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', action='store', dest='threads',default = 1, help='number of threads to scan with')
	parser.add_argument('-ip', dest='ipRange', default = [], nargs = '*', help = 'IP range to scan, specify with [from] [to]')
	parser.add_argument('-l', action='store', dest='listName', default = "", help='list of hosts to scan')
	parser.add_argument('-lk', action='store', dest='loadList', default = "", help='load list of saved keys from file')
	parser.add_argument('-sk', action='store', dest='saveList', default = "", help='save list of saved keys to file')
	parser.add_argument('-c', action='store_true', dest='crack', help='crack loaded RSA keys')
	parser.add_argument('-to', action='store', dest='timeout', default = 10, help='timeout in seconds before terminating connections')
	args = parser.parse_args()

	# load keys
	if args.loadList != "":
		loadKeys(args.loadList)

	# scan IP ranges
	if args.ipRange != []:
		print "[+] Scanning IP range..."
		try:
			fromIP = args.ipRange[0]
			toIP = args.ipRange[1]
			assert IPToInteger(fromIP) <= IPToInteger(toIP)
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
