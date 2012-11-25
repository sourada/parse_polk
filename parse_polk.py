tests = ['Acheson Wm B (Mamie), carp, r 1231 Duff',
'Adamson James Dr (Golda), r 603 Burnett',
'Adams Elmer (Ida), barber, r 1211 Burnett']

for test in tests:
	comma_fields = test.split(',')
	occupation = None
	if len(comma_fields) == 3:
		(names, occupation, address) = comma_fields
	elif len(comma_fields) == 2:
		(names, address) = comma_fields
	name_fields = names.split(' ')
	last_name = name_fields[0]
	first_name = name_fields[1]
	is_doctor = False
	wife_name = None
	for name in name_fields[2:]:
		if name == 'Dr':
			is_doctor = True
		elif name.startswith('('):
			wife_name = name[1:-1]
	address_fields = address.split(' ')
	address_category = address_fields[0]
	address_number = address_fields[1]
	address_street = address_fields[2]
	
	for fn in ['last_name', 'first_name', 'wife_name']:
		print '%s: \'%s\'' % (fn, globals()[fn])
