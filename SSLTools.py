from Crypto.Util import asn1
import ssl
import socket
import OpenSSL

def getModulus(address, timeout):
	'''
	Gets SSL cert from 'address' and returns (n, e) as tuple of long. 
	Raises exception if cert contains no RSA key. 
	'''
	getAddress = address
	getPort = 443
	if ":" in address:
		getAddress = address.split(":")[0]
		getPort = int(address.split(":")[1])
	#cert = ssl.get_server_certificate((address, 443))
	cert = getSSLCertificate(getAddress, getPort, timeout = timeout)
	x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
	pub = x509.get_pubkey()
	if pub.type()!=OpenSSL.crypto.TYPE_RSA:
    		raise Exception('Not RSA key')
	pub_asn1=OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, pub)
	pub_der = asn1.DerSequence()
	pub_der.decode(pub_asn1)
	return (pub_der[1], pub_der[2])

def getSSLCertificate(addr, port, timeout=None):
	'''
	Connect to a server and get its SSL certificate.
	'''
	sock = socket.create_connection((addr,port), timeout=timeout)
	context = ssl.create_default_context()
	context.check_hostname = False
	context.verify_mode = ssl.CERT_NONE
	sslsock = context.wrap_socket(sock, server_hostname=addr)
	return sslsock.getpeercert(True)
