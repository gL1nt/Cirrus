import unittest
import os
import sys

sys.path.append('../')

from ModulusList import ModulusListImpl

class ModulusListTests(unittest.TestCase):

	def test_index_should_work(self):
		sut = ModulusListImpl()
		sut.add('192.168.1.1', 345635467, 3)
		sut.add('192.168.1.2', 345635467, 3)
		sut.add('192.168.1.3', 345635467, 3)
		IPs = [sut[0][0], sut[1][0], sut[2][0]]
		self.assertTrue('192.168.1.1' in IPs)
		self.assertTrue('192.168.1.2' in IPs)
		self.assertTrue('192.168.1.3' in IPs)

	def test_getLength_should_work(self):
		sut = ModulusListImpl()
		sut.add('192.168.1.1', 345635467, 3)
		sut.add('192.168.1.2', 345635467, 3)
		sut.add('192.168.1.3', 345635467, 3)
		self.assertEqual(sut.length(), 3, "Shoud have three items.")

	def test_save_then_load_should_retreive_all_saved_data(self):
		sut1 = ModulusListImpl()
		sut2 = ModulusListImpl()
		sut1.add('192.168.1.1', 345635467, 3)
		sut1.add('192.168.1.2', 345635467, 3)
		sut1.add('192.168.1.3', 345635467, 3)
		sut1.saveListToFile("test.txt")
		sut2.loadListFromFile("test.txt")
		os.remove("test.txt")
		self.assertEqual(sut2.length(), 3, "Shoud have three items.")
		IPs = [sut2[0][0], sut2[1][0], sut2[2][0]]
		self.assertTrue('192.168.1.1' in IPs)
		self.assertTrue('192.168.1.2' in IPs)
		self.assertTrue('192.168.1.3' in IPs)

	def test_add_other(self):
		list1 = ModulusListImpl()
		list2 = ModulusListImpl()
		list1.add('192.168.1.1', 345635467, 3)
		list1.add('192.168.1.2', 345635467, 3)
		list1.add('192.168.1.3', 345635467, 3)
		list2.add('192.168.1.4', 345635467, 3)
		list2.add('192.168.1.5', 345635467, 3)
		list2.add('192.168.1.6', 345635467, 3)
		list1.addModulusList(list2)
		self.assertEqual(list1.length(), 6, "Shoud have six items.")
		IPs = [list1[0][0], list1[1][0], list1[2][0], list1[3][0], list1[4][0], list1[5][0]]
		self.assertTrue('192.168.1.1' in IPs)
		self.assertTrue('192.168.1.2' in IPs)
		self.assertTrue('192.168.1.3' in IPs)
		self.assertTrue('192.168.1.4' in IPs)
		self.assertTrue('192.168.1.5' in IPs)
		self.assertTrue('192.168.1.6' in IPs)

if __name__ == '__main__':
	unittest.main()
