import re
import sys
import argparse

# looks like an address
address = re.compile(r'[RrHh]?([1-9lI][0-9oOl]* +.{1,12} +(AV|Av|av|ST|St|st|RD|Rd|rd|DR|Dr|dr))\b')
# stuff we want to strip out
junk = re.compile(r'[*<>.]')
spaces = re.compile(r'\s+')


class Format1(object):
    def parse(self, lines):
        hits = []

        # try 1-3 lines together until we get a match for the pattern
        lineno = 0
        while lineno < len(lines):
            concat_lines = ''
            for i in range(2):
                if lineno + i >= len(lines):
                    break
                concat_lines += ' ' + lines[lineno + i]
                m = address.search(concat_lines)
                if m:
                    hits.append(m.group(1))
                    lineno += i
                    break
            lineno += 1

        # fix up common errors
        fixed_hits = []
        for hit in hits:
            fixed_hit = junk.sub('', hit)
            fixed_hit = spaces.sub(' ', fixed_hit)
            end_of_initial_number = fixed_hit.find(' ')
            initial_number = fixed_hit[:end_of_initial_number]
            initial_number = initial_number.replace('I', '1').replace('l', '1').replace('o', '0').replace('O', '0')
            fixed_hit = initial_number + fixed_hit[end_of_initial_number:]
            fixed_hits.append(fixed_hit)

        return fixed_hits


class Format2(Format1):
    # formats 1 and 2 are pretty similar
    pass


if __name__ == '__main__':
    lines = []
    arg_parser = argparse.ArgumentParser(description='Parse OCR data from phonebooks')
    arg_parser.add_argument('format', type=int, help='number of format to parse')
    arg_parser.add_argument('file', type=str, help='file to parse', nargs='+')

    parsed_args = arg_parser.parse_args(sys.argv[1:])

    for file in parsed_args.file:
        with open(file) as f:
            lines += [l.strip() for l in f.readlines()]

    parser = Format1()
    for hit in parser.parse(lines):
        print hit
