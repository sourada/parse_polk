from os import path
import unittest
from main import *


def strip_test_lines(inp):
    return [l.strip() for l in inp.split('\n')][1:-1]

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


class ParsePolkTest(unittest.TestCase):
    def test_format_1(self):
        inp, expected = read_test_file('format_1')
        parser = Format1and2()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_2(self):
        inp, expected = read_test_file('format_2')
        parser = Format1and2()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_3_happy_with_middle(self):
        inp = strip_test_lines("""
Kalton Robert R r 715 Lynn.................985-W
 Kampen Fuller N r 1521 Kellogg............2236-W
 Kautz John Lt r 518 Hayward..............2493-W
 Keasey Charles S r 1217 Clark...............2457-J
        """)
        expected = strip_test_lines("""
Kalton,Robert,R,,r,715,Lynn,,985-W
Kampen,Fuller,N,,r,1521,Kellogg,,2236-W
Kautz,John,Lt,,r,518,Hayward,,2493-W
Keasey,Charles,S,,r,1217,Clark,,2457-J
        """)
        parser = Format3()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_3_happy_without_middle(self):
        inp = strip_test_lines("""
Karns Worth r 2817 Oakland................2494-J
 Kelley Dorothy r 3133 Story................3114-J
 Kerekes Frank r 1123 Burnett.................1123
        """)
        expected = strip_test_lines("""
Karns,Worth,,,r,2817,Oakland,,2494-J
Kelley,Dorothy,,,r,3133,Story,,3114-J
Kerekes,Frank,,,r,1123,Burnett,,1123
        """)
        parser = Format3()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_3_farm(self):
        inp = strip_test_lines("""
 Kaitenheuser George W farm................65-F16
Kelley A farm.............................23-F12
Kingsbury Frank farm.,.....................65-F12
        """)
        expected = strip_test_lines("""
Kaitenheuser,George,W,,,,,farm,65-F16
Kelley,A,,,,,,farm,23-F12
Kingsbury,Frank,,,,,,farm,65-F12
        """)
        parser = Format3()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_3_non_r(self):
        inp = strip_test_lines("""
Kappa Delta 2102 Sunset dr...................581
Kappa Sigma Fraternity 237 Ash...............1948
        """)
        expected = strip_test_lines("""
Kappa Delta,,,,,2102,Sunset dr,,581
Kappa Sigma Fraternity,,,,,237,Ash,,1948
        """)
        parser = Format3()
#        print '\n'.join(parser.parse(inp))
        self.assertEqual(parser.parse(inp), expected)

    def test_format_3_weird_dots(self):
        inp = strip_test_lines("""
Kingsbury Frank farm.,.....................65-F12
        """)
        expected = strip_test_lines("""
Kingsbury,Frank,,,,,,farm,65-F12
        """)
        parser = Format3()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_3_profession(self):
        inp = strip_test_lines("""
Beam F N dentist 322% Main.................85
        """)
        expected = strip_test_lines("""
Beam,F,N,dentist,,322 1/2,Main,,85
        """)
        parser = Format3()
        self.assertEqual(parser.parse(inp), expected)

    def test_format_3_half(self):
        inp = strip_test_lines("""
 Hohberger Halland D r 217% S Hazel.......... 17 1'
Carter L P Ins 312V2 Main..................138
        """)
        expected = strip_test_lines("""
Hohberger,Halland,D,,r,217 1/2,S Hazel,,17 1'
Carter L P,,,,,312 1/2,Main,,138
        """)
        parser = Format3()
        self.assertEqual(parser.parse(inp), expected)


if __name__ == '__main__':
    unittest.main()