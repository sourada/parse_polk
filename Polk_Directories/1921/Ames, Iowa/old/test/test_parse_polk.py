import unittest
from os import path
from parse_polk import parse_file, read_file, write_file

TEST_DIR = './'

class TestParsePolk(unittest.TestCase):
	def test_form_one(self):
		self.do_test('form_one')
	
	def test_form_two(self):
		self.do_test('form_two')

	def test_form_three(self):
		self.do_test('form_three')

	def test_no_wife(self):
		self.do_test('no_wife')

	def test_occ_place(self):
		self.do_test('occ_place')

	def test_occ_two_words(self):
		self.do_test('occ_two_words')

	def test_wife_middle_name(self):
		self.do_test('wife_middle_name')

	def test_proprietor(self):
		self.do_test('proprietor')

	def test_no_addr_category(self):
		self.do_test('no_addr_category')

	def test_addr_with_and(self):
		self.do_test('addr_with_and')

	def test_widow(self):
		self.do_test('widow')

	# TODO: we aren't doing the right thing here. How do we distinguish this case?
	def test_business(self):
		self.do_test('business')

	def test_spurious_first_char(self):
		self.do_test('spurious_first_char')

	def test_percent_signs(self):
		self.do_test('percent_signs')

	def do_test(self, fn_base):
		real_ret, real_err = parse_file(TEST_DIR + fn_base + '_in.txt')

		expected_ret_path = TEST_DIR + fn_base + '_out.txt'
		expected_ret = None
		if path.exists(expected_ret_path):
			expected_ret = read_file(expected_ret_path)
		if expected_ret is None or expected_ret != real_ret:
			bad_ret_path = TEST_DIR + 'TEST_' + fn_base + '_out.txt'
			write_file(bad_ret_path, real_ret)
			print 'wrote ' + bad_ret_path

		expected_err_path = TEST_DIR + fn_base + '_err.txt'
		expected_err = None
		if path.exists(expected_err_path):
			expected_err = read_file(expected_err_path)
		if expected_err is None or expected_err != real_err:
			bad_err_path = TEST_DIR + 'TEST_' + fn_base + '_err.txt'
			write_file(bad_err_path, real_err)
			print 'wrote ' + bad_err_path

		if expected_ret is not None:
			self.assertEqual(expected_ret, real_ret)
		else:
			self.fail('missing ' + expected_ret_path + ' file')

		if expected_err is not None:
			self.assertEqual(expected_err, real_err)
		else:
			self.fail('missing ' + expected_err_path + ' file')

if __name__ == '__main__':
	unittest.main()

