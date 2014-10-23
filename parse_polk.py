import re
import sys

COLUMNS = ['last_name', 'first_name', 'middle_name', 'occupation', 'occupation_place', 'address_category', 'address_number', 'address_street', 'address_cross_1', 'address_cross_2']
# indexes into list of columns that should be copied for wife
WIFE_COLUMNS = set([0, 5, 6, 7, 8, 9])

def format_err(lno, typ):
	return '%d %s' % (lno, typ)

def parse(lines):
	ret = []
	err = []
	
	ret.append(','.join(COLUMNS))

	for lno, line in enumerate(lines):
		last_name = ''
		first_name = ''
		middle_name = ''
		occupation = ''
		occupation_place = ''
		address_category = ''
		address_number = ''
		address_street = ''
		address_cross_1 = ''
		address_cross_2 = ''

#		print lno
		if line.strip() == '':
			continue

		# remove spurious first char(s)
		line = re.sub(r'^([-(\'!|j]|([iI] ))', '', line)
		
		# remove spurious end char(s)
		line = re.sub(r'%$', '', line)
		
		# split by commas
		comma_fields = [f.strip() for f in line.split(',')]
		occupation_and_place = ''
		if len(comma_fields) == 3:
			names, occupation_and_place, address = comma_fields
		elif len(comma_fields) == 2:
			names, address = comma_fields
		else:
			err.append(format_err(lno, 'COMMA_FIELDS_NUM'))
			continue

		if occupation_and_place:
			splt = occupation_and_place.split(' ')
			bi = len(splt)
			# we'll assume the the words that are capitalized are the place,
			# and those before it are the occupation title
			# TODO: could use abbreviation list here
			# TODO: could fix common errors here ('elk' instead of 'clk')
			for i in range(1, len(splt)):
				fc = splt[i][0]
				if fc == fc.upper():
					bi = i
					break
			occupation = ' '.join(splt[:bi])
			occupation_place = ' '.join(splt[bi:])
		
		# doctor
		m = re.match(r'(.*?) dr\b(.*)', names, re.IGNORECASE)
		if m:
			occupation = 'dr'
			names = m.group(1) + m.group(2)

		wife_name = ''
		wife_middle_name = ''

		# widow
		m = re.match(r'(.*?) \((wid .*?)\)(.*)', names, re.IGNORECASE)
		if m:
			# just ignore the wid thing. The guy isn't living any more, don't add him.
			names = m.group(1) + m.group(3)
	
		# wife
		m = re.match(r'(.*?) \((.*?)\)(.*)', names)
		if m:
			split_wife_name = m.group(2).split(' ', 1)
			wife_name = split_wife_name[0]
			if len(split_wife_name) > 1:
				wife_middle_name = split_wife_name[1]
			names = m.group(1) + m.group(3)

		# remainder of names
		split_names = names.split(' ', 2)
		if len(split_names) > 1:
			last_name, first_name = split_names[:2]
			if len(split_names) > 2:
				middle_name = split_names[2]
		elif len(split_names) == 1:
			last_name = split_names[0]

		# cross-streets address
		m = re.match(r'(.*?) (.*?) and (.*)', address, re.IGNORECASE)
		if m:
			address_category, address_cross_1, address_cross_2 = m.group(1), m.group(2), m.group(3)
		else:
			address_fields = address.split(' ', 2)
			if len(address_fields) == 2:
				address_number, address_street = address_fields
			elif len(address_fields) > 2:
				address_category, address_number, address_street = address_fields

		# fix some common OCR errors
		address_number = re.sub(r'(\d+)%', r'\1 1/2', address_number)

		# fill in CSV line
		v = locals()
		column_vals = [v[column] for column in COLUMNS]
		ret_line = ','.join(column_vals)
		ret.append(ret_line)
	
		# fill in another CSV line for wife if present. She deserves it.
		if wife_name:
			wife_column_vals = []
			for ci in range(len(COLUMNS)):
				wife_column_vals.append(column_vals[ci] if ci in WIFE_COLUMNS else '')
				
			wife_column_vals[1] = wife_name
			if wife_middle_name:
				wife_column_vals[2] = wife_middle_name
			ret_line = ','.join(wife_column_vals)
			ret.append(ret_line)

	# TODO: do an alphabetical-order check here
	return (ret, err)

def read_file(filename):
	with open(filename) as f:
		lines = f.readlines()
	return [line[:-1] for line in lines]

def write_file(filename, lines):
	with open(filename, 'w') as f:
		f.writelines((line + '\n' for line in lines))

def parse_file(filename):
	return parse(read_file(filename))

if __name__ == '__main__':
	fn = sys.argv[1]
	ret, err = parse_file(fn + '.txt')
	write_file(fn + '.csv', ret)
	write_file(fn + '.err', err)
