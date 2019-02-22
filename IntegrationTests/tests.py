import unittest
import os
import BaseHTTPServer, SimpleHTTPServer
import ssl
import sys

sys.path.append('../')

from RSATools import *

class CrackerTests(unittest.TestCase):

	def test_1(self):
		pass

def Setup():
	WritePemFromPrimes("1.pem", 11, 19)
	WritePemFromPrimes("2.pem", 11, 23)
	WritePemFromPrimes("3.pem", 17, 29)
	WritePemFromPrimes("4.pem", 13, 31)
	WritePemFromPrimes("5.pem", 13, 37)
	for i in range(0, 5):
		httpd = BaseHTTPServer.HTTPServer(('localhost', 4443+i), SimpleHTTPServer.SimpleHTTPRequestHandler)
		certFileName=str(i+1)+".pem"
		httpd.socket = ssl.wrap_socket (httpd.socket, certfile=certFileName, server_side=True)
		httpd.serve_forever()

def Cleanup():
	for i in range(0,5):
		os.remove(str(i) + ".pem")

def WritePemFromPrimes(name, p, q):
	builder = RSA(p, q)
	pem = builder.to_pem()
	output = open(name, "w")
	output.write(pem)
	output.close()

if __name__ == '__main__':
	Setup()
	unittest.main()
	Cleanup()
