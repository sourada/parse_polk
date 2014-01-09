import re
import sys

# looks like an address
address = re.compile(r'[RrHh]?([1-9lI][0-9oOl]* +.{1,12} +(AV|Av|av|ST|St|st|RD|Rd|rd|DR|Dr|dr))\b')
# stuff we want to strip out
junk = re.compile(r'[*<>.]')
spaces = re.compile(r'\s+')

def parse(lines):
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

if __name__ == '__main__':
    lines = []
    for file in sys.argv[1:]:
        with open(file) as f:
            lines += [l.strip() for l in f.readlines()]

    for hit in parse(lines):
        print hit
