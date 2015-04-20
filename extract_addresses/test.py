from os import path
import unittest
from main import Format1, Format2


def read_test_file(name):
    with open(path.join('test_data', name + '.txt')) as f:
        inp = [l.strip() for l in f.readlines()]
    expected = []
    try:
        with open(path.join('test_data', name + '_expected.txt')) as f:
            expected = [l.strip() for l in f.readlines()]
    except:
        pass
    return inp, expected


class ExtractAddressTest(unittest.TestCase):
    def test_format_1(self):
        inp, expected = read_test_file('format_1')
        parser = Format1()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_2(self):
        inp, expected = read_test_file('format_2')
        parser = Format2()
        self.assertEqual(parser.parse(inp), expected)

#    def test_format_3(self):
#        inp, expected = read_test_file('format_3')
#        self.assertEqual(parse(inp), expected)
