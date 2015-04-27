import re
import sys
import argparse

class Format1and2(object):
    @staticmethod
    def parse(lines):
        # looks like an address
        address = re.compile(r'[RrHh]?([1-9lI][0-9oOl]* +.{1,12} +(AV|Av|av|ST|St|st|RD|Rd|rd|DR|Dr|dr))\b')
        # stuff we want to strip out
        junk = re.compile(r'[*<>.]')
        spaces = re.compile(r'\s+')

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


class Format3(object):
    @staticmethod
    def parse(lines):
        dot = r'[.,\-\xe2]'
        dots = dot + r'(?:' + dot + r')+'
        front_bit = r'^(.*?)'
        r_designation = r'?:\s+(?:(r)\s*)'
        street_address = r'(?:(\d+(?:%|V2)?)\s+(.*?))'
        farm = '(farm)'
        back_bit = r'\s*(.*)$'
        address = re.compile(front_bit + r'(' + r_designation + r'?' + street_address + r'|' + farm + r')' + dots + back_bit)
        half = re.compile(r'%|V2')

        err = []
        hits = []

        for line in lines:
            address_match = address.match(line)

            if not address_match:
                err.append(line)
                continue

            groups = [e if e else '' for e in address_match.groups()]

            name_profession = re.split(r'\s+', groups[0])
            names = []
            profession_words = []
            for s in name_profession:
                if s.lower() == s:
                    profession_words.append(s)
                else:
                    names.append(s)

            if len(names) > 3:
                names[3] = ' '.join(names[3:])
                names = names[:3]
            elif len(names) == 1:
                names.extend(['', ''])
            elif len(names) == 2:
                names.append('')

            cols = names

            cols.append(' '.join(profession_words))
            cols.extend(groups[1:])

            if cols[4] != 'r' and cols[3] == '' and cols[7] != 'farm':
                 cols[0] = ' '.join(cols[0:3]).strip()
                 cols[1] = cols[2] = ''

            cols[5] = half.sub(' 1/2', cols[5])

            hits.append(','.join(cols))

        return hits

format_map = {1: Format1and2, 2: Format1and2, 3: Format3}
if __name__ == '__main__':
    lines = []
    arg_parser = argparse.ArgumentParser(description='Parse OCR data from phonebooks')
    arg_parser.add_argument('format', type=int, help='number of format to parse')
    arg_parser.add_argument('file', type=str, help='file to parse', nargs='+')

    parsed_args = arg_parser.parse_args(sys.argv[1:])

    for file in parsed_args.file:
        with open(file) as f:
            lines += [l.strip() for l in f.readlines()]

    parser = format_map[parsed_args.format]()
    for hit in parser.parse(lines):
        print hit
