import re
# pattern = "[FXf+-&^\\/|\[\]]\(.*\)"
# result = re.match(pattern,"F(a1)")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def create_dict(in_string):
	if not in_string:
		return {}

	variables = {}
	for pair in re.split("\n",in_string):
		keyval = re.split(":",pair)
		if keyval[0] is not '' and len(keyval) is 2:
				variables[keyval[0]]=float(keyval[1])

	# print(variables)
	return variables


# Given an input string, returns list of commands
# and arguments, as [command, arguments...]
def parse_args(in_string,tokens):
	in_string = str(in_string)
	instructions = []
	m = re.findall("([\[\]XLABC"+tokens+"$!^FXf\+\-&/])(\(.*?\))?",in_string)
	for pair in m:
		item = []
		item.append(pair[0])
		if pair[1] is '':
			item.append("def")
		else:
			arguments = re.match("\((.*?)\)", pair[1]).group(1)
			for ar in re.split(",",arguments):
				item.append(ar)
		instructions.append(item)
	return instructions

# Given an input string, returns list of commands
# and arguments do a given depth
def parse_input(in_string,axiom,depth,variables):

	if not axiom:
		return []

	alphabet = "AXLBC$!FXf+-&^\/|[]"
	tokens = ""
	mappings = {}
	for letter in alphabet:
		mappings[letter] = [letter,'def']

	if in_string:
		r = re.split("\n", in_string)
		for projection in r:
			token = re.split(":",projection)[0]
			if token not in alphabet and token not in tokens:
				tokens += token

			m = re.match("([!ABLC$F^X\-f\+&/"+tokens+"])(\((.*?)\))?:(.*)", projection)
			try:
				new_map = [m.group(4)]
				if m.group(3) is not None:
					new_map+=re.split(",",m.group(3))
				# mappings[m.group(1)]=[m.group(4),m.group(3)]
				mappings[m.group(1)]=new_map
			except:
				print("Problem with projection")
				print(projection)
				raise SystemExit(0)

	axiom_list = parse_args(axiom,tokens)
	for i in range(len(axiom_list)):
		for k in range(len(axiom_list[i][1:])):
			if is_number(axiom_list[i][k+1]):
				axiom_list[i][k+1]=float(axiom_list[i][k+1])

	for i in range(depth):
		newaxiom = []
		for item in axiom_list:

			#line to replace with
			command_name = item[0]
			replacement=mappings[command_name][0]
			#local variables
			local_map = mappings[command_name][1:]

			#identity, just copy
			if command_name is replacement:
				for i in range(len(item[1:])):
					if is_number(item[1:][0]):
						# item[1:][i] = float()
						item[i+1] = float(item[1:][i])
				newaxiom.append(item)
			else:
				#assign values of local variables to map
				counter = 0
				for ar in item[1:]:
					if ar is not 'def' and not is_number(local_map[counter]):
						try:
							variables[local_map[counter]] = float(ar)
							counter += 1
						except:
							print("Incorrect Number of Argments")
							print("Variables:{} Given:{}".format(local_map,item[1:]))
							raise SystemExit(0)
					# elif:
					# 	pass
					# 	# print("fails here")
					# 	# print(item)
					# 	# print(local_map)
					# 	# print(counter)
					# 	# print("a number {}".format(local_map[counter]))

				#recursively parse replacement
				replacement_pairs = parse_args(replacement,tokens)

				#for command and arguments in new pairs, parse
				for pair in replacement_pairs:
					new_expressions = []
					for ar in pair[1:]:
						new_string = ""
						try:
							m = re.split("[\%\*\+-]",ar)
						except:
							print("problem")
							raise SystemExit(0)
						o = re.findall("[\%\*\+-]",ar)

						if m[0] is not 'def':
							for i in range(len(m)):
								if is_number(m[i]) is not True:
									new_string+="variables[\'"+m[i]+"\']"
								else:
									new_string+=str(m[i])
								if i < len(o):
										new_string += o[i]
							try:
								new_expressions.append(eval(new_string))
							except:
								print(new_string)
								print("Invalid Syntax")
								raise SystemExit(0)
						else:
							new_expressions.append('def')

					#add new pair to the final list being constructed
					try:
						newaxiom.append([pair[0]]+new_expressions)
					except:
						print("Failed to generate new axiom")
						raise SystemExit(0)

				#delete from local variable list
				for i in local_map:
					variables.pop(i, None)

		axiom_list = newaxiom

	print("success!")
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

	map_input = \
'''A(l,w):!(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)
B(l,w):!(w)F(l)[-(a2)$C(l*r2,w*wr)]C(l*r1,w*wr)
C(l,w):!(w)F(l)[+(a2)$B(l*r2,w*wr)]B(l*r1,w*wr)'''
	# map_input2 = \
	# '''A(w):B(w)A(w*wr+w)
	# B(w):!(w)
	# C(w):!(w)'''
	map_input3 = \
	'''F(w):F(w)F(w)\\/&(w)F(w)'''
	axiom = "A(1,10)"
	# axiom = "A"

# 	map_input = \
# '''F:FF
# X:F[+X][-X]FX'''
# 	axiom = "X"
	axiom = "F(10)&(45)F(1)"

	variables ={
		'd1':94.74,
		'd2':132.63,
		'a':18.95,
		'lr':1.109,
		'vr':1.732
	}
	strvars =\
'''d1:94.74
d2:132.63
a:18.95
lr:1.109
vr:1.732
'''
	strvars = " "
	axiom = "!(1)F(200)/(45)A"
	map_input =\
'''A:!(vr)F(50)[&(a)F(50)A]/(d1)[&(a)F(50)A]/d2[&(a)F(50)A]
F(l):F(l*lr)
!(w):!(w*vr)'''

	strvars = " "
	axiom = "!(1)F(200)/(45)A(10,20)"
	map_input =\
'''A:[&FK!A]/////[&FK!A]///////[&FK!A]
F:S/////F
S:FK
K:[^^L]'''

	final = parse_input(map_input,axiom,0,None)
	# final = parse_input("", "", 0, {})
	# print(final)value, ...
	christmas = ""
	print(final)
	for item in final:
		christmas+=item[0]
	print(christmas)
	# print(parse_args(strng2))
	# print(create_dict(strvars))
# main()