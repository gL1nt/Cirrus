import unittest
import os
import signal
import BaseHTTPServer, SimpleHTTPServer
import ssl
import sys

sys.path.append('../')

from RSATools import *

children = []

class CrackerTests(unittest.TestCase):

	def test_basic_read_from_host_list(self):
		hostList = open("../hosts.txt", "w")
		for i in range(0, 5):		
			hostList.write("localhost:" + str(4443+i) + "\n")
		hostList.close()
		os.system("python ../Cirrus.py -c -to 2 -l ../hosts.txt")
		self.assertTrue(os.path.isfile('localhost:4443.key'))
		self.assertTrue(os.path.isfile('localhost:4444.key'))
		self.assertFalse(os.path.isfile('localhost:4445.key'))
		self.assertTrue(os.path.isfile('localhost:4446.key'))
		self.assertTrue(os.path.isfile('localhost:4447.key'))
		os.remove('localhost:4443.key')
		os.remove('localhost:4444.key')
		os.remove('localhost:4446.key')
		os.remove('localhost:4447.key')
		os.remove('../hosts.txt')

def Setup():
	a = 282755483533707287054752184321121345766861480697448703443857012153264407439766013042402571
	b = 370332600450952648802345609908335058273399487356359263038584017827194636172568988257769601
	c = 463199005416013829210323411514132845972525641604435693287586851332821637442813833942427923
	d = 374413471625854958269706803072259202131399386829497836277471117216044734280924224462969371
	e = 664869143773196608462001772779382650311673568542237852546715913135688434614731717844868261
	f = 309133826845331278722882330592890120369379620942948199356542318795450228858357445635314757
	g = 976522637021306403150551933319006137720124048624544172072735055780411834104862667155922841
	h = 635752334942676003169313626814655695963315290125751655287486460091602385142405742365191277
	WriteKeyFromPrimes("1.pem", a , d)
	WriteKeyFromPrimes("2.pem", a , e)
	WriteKeyFromPrimes("3.pem", b, f)
	WriteKeyFromPrimes("4.pem", c, g)
	WriteKeyFromPrimes("5.pem", c, h)
	for i in range(0, 5):
		keyFileName=str(i+1)+".pem"
		certFileName=keyFileName+".crt"
		WriteCertsFromKey(keyFileName)
		newpid = os.fork()
		if newpid == 0:
			httpd = BaseHTTPServer.HTTPServer(('localhost', 4443+i), SimpleHTTPServer.SimpleHTTPRequestHandler)
			#httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=keyFileName, certfile=certFileName, server_side=True)
			httpd.serve_forever()
			os._exit(0)
		else:
			children.append(newpid)

def Cleanup():
	for i in range(0,5):
		os.remove(str(i+1) + ".pem")
		os.remove(str(i+1) + ".pem.crt")
	for pid in children:
		os.kill(pid, signal.SIGKILL)

def WriteKeyFromPrimes(name, p, q):
	builder = RSA(p, q)
	pem = builder.to_pem()
	output = open(name, "w")
	output.write(pem)
	output.close()

def WriteCertsFromKey(keyFileName):
	os.system("openssl req -key " + keyFileName + " -new -x509 -days 365 -out " + keyFileName + ".crt -subj '/CN=www.mydom.com/O=My Company Name LTD./C=US'")

if __name__ == '__main__':
	Setup()
	try:
		unittest.main()
	finally:
		Cleanup()
