import re
# pattern = "[FXf+-&^\\/|\[\]]\(.*\)"
# result = re.match(pattern,"F(a1)")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_args(in_string):
	instructions = []
	m = re.findall("([\[\]XABC!FXf\+\-&/])(\(.*?\))?",in_string)
	for pair in m:
		item = []
		item.append(pair[0])
		if pair[1] is '':
			item.append("def")
		else:
			item.append(re.match("\((.*?)\)", pair[1]).group(1))
		instructions.append(item)
	return instructions

def parse_input(in_string,axiom,depth,variables):
	alphabet = "AXBC!FXf+-&^\/|[]"
	mappings = {}
	for letter in alphabet:
		mappings[letter] = [letter,0]
	# print(mappings)

	r = re.split("\n", in_string)
	print(r)
	for projection in r:
		# print("projection: "+projection)
		m = re.match("([!ABCFX\-f\+&/])(\((.*?)\))?:(.*)", projection)
		try:
			mappings[m.group(1)]=[m.group(4),m.group(3)]
		except:
			print(projection)
			raise SystemExit(0)

	# print(m.groups())
	# print(mappings)
	axiom_list = parse_args(axiom)
	# print(axiom_list)

	for i in range(depth):
		newaxiom = []
		for item in axiom_list:
			replacement=mappings[item[0]][0]
			local_map = mappings[item[0]][1]

			# print(variables)
			# print(item[1])

			if item[1] is not 'def':
				variables[local_map] = float(item[1])

			# print(local_map)
			# mappings[local_map]=item[1]

			replacement_pairs = parse_args(replacement)
			# print(replacement_pairs)

			for pair in replacement_pairs:
				new_string = ""
				# print("pair is "+pair[1])
				m = re.split("[\%\*\+-]", pair[1])
				o = re.findall("[\%\*\+-]",pair[1])

				if m[0] is not 'def':
					for i in range(len(m)):
						if is_number(m[i]) is not True:
							new_string+="variables[\'"+m[i]+"\']"
						else:
							new_string+=m[i]
						if i < len(o):
								new_string += o[i]
					try:
						new_expression = eval(new_string)
					except:
						print("Invalid Syntax")
						print(new_string)
						raise SystemExit(0)
				else:
					new_expression = 'def'

				newaxiom.append([pair[0],new_expression])

			variables.pop(local_map, None)
			# print(variables)
		axiom_list = newaxiom

	return axiom_list

def main():
	strng = r"F(a)f(a)+(a)&(a)/(a)"
	strng2 = r"Ff+&/"
	variables = {
		'r1':0.9,
		'r2':0.6,
		'a0':45,
		'a2':45,
		'd':137.5,
		'wr':0.707,
		'w':69
	}
	r1=0.9
	r2=0.6
	a0=45
	a2=45
	d=137.5
	wr=0.707

	# map_input = \
	# '''A(w):!(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)
	# B(w):!(w)F(l)[-(a2)$C(l*r2,w*wr)]C(l*r1,w*wr)
	# C(w):!(w)F(l)[+(a2)$B(l*r2,w*wr)]B(l*r1,w*wr)'''
	# map_input2 = \
	# '''A(w):B(w)A(w*wr+w)
	# B(w):!(w)
	# C(w):!(w)'''
	# map_input3 = \
	# '''F(w):F(w)F(w)\\/&(w)F(w)'''
	# axiom = "F(10)"

	map_input = \
'''F:FF
X:F[+X][-X]FX'''
	axiom = "X"

	final = parse_input(map_input,axiom,1,variables)
	print(final)
	# for item in final:
	# 	print(item[0])
	# print(parse_args(strng2))
# main()