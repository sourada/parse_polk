import re
import sys
import argparse


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

        return [hits, err]

format_map = {3: Format3}
if __name__ == '__main__':
    lines = []
    arg_parser = argparse.ArgumentParser(description='Parse OCR data from phonebooks. Outputs output.csv and errors.txt')
    arg_parser.add_argument('format', type=int, help='number of format to parse')
    arg_parser.add_argument('file', type=str, help='file to parse', nargs='+')

    parsed_args = arg_parser.parse_args(sys.argv[1:])

    for file in parsed_args.file:
        with open(file) as f:
            lines += [l.strip() for l in f.readlines()]

    parser = format_map[parsed_args.format]()
    output, errors = parser.parse(lines)
    with open('output.csv', 'w') as out:
        out.writelines([line + '\n' for line in output])
    with open('errors.txt', 'w') as out:
        out.writelines([line + '\n' for line in errors])
