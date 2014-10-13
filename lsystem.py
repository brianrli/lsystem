"""
Axiom:

Mappings:

Iterations:

Alphabet
F: Move forward a step of length d.
+: turn left
-: turn right
&: pitch down
^: pitch up
\: roll left
/: roll right
|: turn around
"""
import string
from pyparsing import *
import pymel.core as pm

f = pm.newFile(f=True)

#key variables
map_input = \
'''F:F+F-F-F+F'''
axiom = "-F"
iterations = 3
dist = 5
degr = 90
mappings = {}
alphabet = "Ff+-&^\/|[]"
for letter in alphabet:
	mappings[letter] = letter


#parse map
map = Word(alphabet)
instruction = Word(alphabet)
mapExpr = map.setResultsName("key")+":"+instruction.setResultsName("value")
split_map_input = string.split(map_input, '\n')
print(split_map_input)
for line in split_map_input:
	try:
		newMap = mapExpr.parseString(line)
		print(newMap.key)
		print(newMap.value)
		mappings[newMap.key] = newMap.value
	except:
		print("Bad Map Definition")
		raise SystemExit(0)


print(mappings)

newaxiom = ""
#process LSystem
for i in range(iterations):
	for letter in axiom:
		newaxiom+=mappings[letter]
	axiom = newaxiom

print("***RESULT***\n"+axiom+"\n************")

"""
Draw LSystem

Supported Commands:
F --> move forward by distance d
+ --> turn left by angle ang
"""

curpos = {
	'x':0,
	'y':0,
	'ang':0
}

ang = 0
degr = 0
first_itr = True
# axiom = "F-FFFF-F"
for command in axiom:
	
	if command is 'F':
		print ("{} {}".format("F command triggered", ang))
		current = pm.polyCube(height=5)[0]
		if not first_itr:
			current.setMatrix(previous.getMatrix(worldSpace=True))
			pm.parent(current,previous)
		else:
			first_itr = False
		
		# w
		if degr != 0:
			print("triggered 1")
			pm.move(0,dist/2,0,current,os=True)
			pm.rotate(current,0,0,degr,os=True)
			pm.move(0,dist/2,0,current,os=True,relative=True)
		if degr == 0:
			print("triggered 2")
			pm.move(0,dist,0,current,os=True,relative=True)
		degr = 0
		previous = current

	elif command is '-':
		degr = -90
		ang-=degr
		print ("{} {}".format("- command triggered", ang))

	elif command is '+':
		degr = 90
		ang+=degr
		print ("{} {}".format("+ command triggered", ang))






