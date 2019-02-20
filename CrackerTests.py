import unittest
import os
from Cracker import CrackerImpl
from ModulusList import ModulusListImpl

class CrackerTests(unittest.TestCase):

	def test_cracker_should_work_with_one_value(self):
		theList = ModulusListImpl()
		theList.add('127.0.0.1', 24, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertFalse(os.path.isfile('127.0.0.1.key'))

	def test_cracker_should_work_with_no_common_factors(self):
		theList = ModulusListImpl()
		theList.add('192.168.1.1', 3, 3)
		theList.add('192.168.1.2', 5, 3)
		theList.add('192.168.1.3', 11, 3)
		theList.add('192.168.1.4', 13, 3)
		theList.add('192.168.1.5', 17, 3)
		theList.add('192.168.1.6', 23, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertFalse(os.path.isfile('192.168.1.1.key'))
		self.assertFalse(os.path.isfile('192.168.1.2.key'))
		self.assertFalse(os.path.isfile('192.168.1.3.key'))
		self.assertFalse(os.path.isfile('192.168.1.4.key'))
		self.assertFalse(os.path.isfile('192.168.1.5.key'))
		self.assertFalse(os.path.isfile('192.168.1.6.key'))

	def test_cracker_should_work_with_two_values_with_common_factor(self):
		theList = ModulusListImpl()
		theList.add('192.168.1.1', 2*3, 3)
		theList.add('192.168.1.2', 5*3, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertTrue(os.path.isfile('192.168.1.1.key'))
		self.assertTrue(os.path.isfile('192.168.1.2.key'))
		os.remove('192.168.1.1.key')
		os.remove('192.168.1.2.key')

	def test_cracker_should_work_with_three_values_with_three_common_factors(self):
		theList = ModulusListImpl()
		theList.add('192.168.1.1', 2*3, 3)
		theList.add('192.168.1.2', 5*3, 3)
		theList.add('192.168.1.3', 7*3, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertTrue(os.path.isfile('192.168.1.1.key'))
		self.assertTrue(os.path.isfile('192.168.1.2.key'))
		self.assertTrue(os.path.isfile('192.168.1.3.key'))
		os.remove('192.168.1.1.key')
		os.remove('192.168.1.2.key')
		os.remove('192.168.1.3.key')

	def test_cracker_should_work_with_three_values_with_two_common_factors_1(self):
		theList = ModulusListImpl()
		theList.add('192.168.1.1', 2*3, 3)
		theList.add('192.168.1.2', 2*5, 3)
		theList.add('192.168.1.3', 7*11, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertTrue(os.path.isfile('192.168.1.1.key'))
		self.assertTrue(os.path.isfile('192.168.1.2.key'))
		self.assertFalse(os.path.isfile('192.168.1.3.key'))
		os.remove('192.168.1.1.key')
		os.remove('192.168.1.2.key')

	def test_cracker_should_work_with_three_values_with_two_common_factors_2(self):
		theList = ModulusListImpl()
		theList.add('192.168.1.1', 2*3, 3)
		theList.add('192.168.1.2', 7*5, 3)
		theList.add('192.168.1.3', 2*11, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertTrue(os.path.isfile('192.168.1.1.key'))
		self.assertFalse(os.path.isfile('192.168.1.2.key'))
		self.assertTrue(os.path.isfile('192.168.1.3.key'))
		os.remove('192.168.1.1.key')
		os.remove('192.168.1.3.key')

	def test_cracker_should_work_with_three_values_with_two_common_factors_3(self):
		theList = ModulusListImpl()
		theList.add('192.168.1.1', 7*3, 3)
		theList.add('192.168.1.2', 2*5, 3)
		theList.add('192.168.1.3', 2*11, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertFalse(os.path.isfile('192.168.1.1.key'))
		self.assertTrue(os.path.isfile('192.168.1.2.key'))
		self.assertTrue(os.path.isfile('192.168.1.3.key'))
		os.remove('192.168.1.2.key')
		os.remove('192.168.1.3.key')

	def test_cracker_should_work_with_multiple_common_factors(self):
		theList = ModulusListImpl()
		theList.add('192.168.1.1', 2*3, 3)
		theList.add('192.168.1.2', 2*5, 3)
		theList.add('192.168.1.3', 7*11, 3)
		theList.add('192.168.1.4', 2*13, 3)
		theList.add('192.168.1.5', 7*17, 3)
		theList.add('192.168.1.6', 23, 3)
		sut = CrackerImpl(theList)
		sut.CrackAndWriteCertificates()
		self.assertTrue(os.path.isfile('192.168.1.1.key'))
		self.assertTrue(os.path.isfile('192.168.1.2.key'))
		self.assertTrue(os.path.isfile('192.168.1.3.key'))
		self.assertTrue(os.path.isfile('192.168.1.4.key'))
		self.assertTrue(os.path.isfile('192.168.1.5.key'))
		self.assertFalse(os.path.isfile('192.168.1.6.key'))
		os.remove('192.168.1.1.key')
		os.remove('192.168.1.2.key')
		os.remove('192.168.1.3.key')
		os.remove('192.168.1.4.key')
		os.remove('192.168.1.5.key')

if __name__ == '__main__':
	unittest.main()
