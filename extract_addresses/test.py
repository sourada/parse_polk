from os import path
import unittest
from main import parse

def read_test_file(name):
    with open(path.join('test_data', name)) as f:
        inp = [l.strip() for l in f.readlines()]
    expected = []
    try:
        with open(path.join('test_data', name + '_expected')) as f:
            expected = [l.strip() for l in f.readlines()]
    except:
        pass
    return inp, expected

class ExtractAddressTest(unittest.TestCase):
    def test_format_1(self):
        inp, expected = read_test_file('format_1')
        self.assertEqual(parse(inp), expected)
