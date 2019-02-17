def IPToInteger(ip):
	'''
	Concert IP address to integer.
	Source: Bruno Adele, Stack Overflow
	'''
	o = map(int, ip.split('.'))
    	res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
    	return res

def IntegerToIP(ipnum):
	'''
	Concert integer to IP address.
	Source: Bruno Adele, Stack Overflow
	'''
    	o1 = int(ipnum / 16777216) % 256
    	o2 = int(ipnum / 65536) % 256
    	o3 = int(ipnum / 256) % 256
    	o4 = int(ipnum) % 256
    	return '%(o1)s.%(o2)s.%(o3)s.%(o4)s' % locals()
