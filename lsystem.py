"""
LSystems by
Brian Li

A basic (my first) maya scripting project.
"""
import string
from pyparsing import *
from pymel import *
import pymel.core as pm

def parse_input(axiom,map_input,iterations):
	mappings = {}
	alphabet = "FXf+-&^\/|[]"
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
	return newaxiom


def draw_axiom(axiom,ang,dist):
	stack = []

	zdegr = 0
	ydegr = 0
	xdegr = 0

	first_itr = True
	# axiom = "F-FFFF-F"
	for command in axiom:
		
		print(command)
		if command is 'F':
			print ("{} {}".format("F command triggered", xdegr))
			current = pm.polyCube(height=5)[0]
			if not first_itr:
				current.setMatrix(previous.getMatrix(worldSpace=True))
				pm.parent(current,previous)
			else:
				first_itr = False
			
			print("{} {}".format("x degree ", xdegr))
			
			if xdegr != 0 or ydegr != 0 or zdegr != 0:
				print("triggered 1")
				pm.move(0,dist/2,0,current,os=True)
				pm.rotate(current,xdegr,ydegr,zdegr,os=True)
				pm.move(0,dist/2,0,current,os=True,relative=True)
			else:
				print("triggered 2")
				pm.move(0,dist,0,current,os=True,relative=True)
			zdegr = 0
			ydegr = 0
			xdegr = 0
			print(xdegr)
			previous = current

		elif command is '-':
			zdegr += -ang
			print ("{} {}".format("- command triggered", ang))

		elif command is '+':
			zdegr += ang
			print ("{} {}".format("+ command triggered", ang))

		elif command is '&':
			print("& command triggered")
			xdegr += -ang
			print(xdegr)

		elif command is '^':
			xdegr += ang

		elif command == "\\":
			print("\\ command triggered")
			ydegr += -ang

		elif command is '/':
			ydegr += ang

		elif command is '[':
			print("[ triggered")
			stack.append([previous,xdegr,ydegr,zdegr])
			print(stack)

		elif command is ']':
			print("] triggered")
			print(stack)
			prev_state = stack.pop()
			previous = prev_state[0]
			xdegr = prev_state[1]
			ydegr = prev_state[2]
			zdegr = prev_state[3]
			print(stack)

def main():
	f = pm.newFile(f=True)

	#key variables
	map_input = \
	'''F:FF
	X:F[+X][-X]FX'''
	axiom = "X"
	
	iterations = 4
	dist = 5
	ang = 25.7
	
	axiom = parse_input(axiom,map_input,iterations)
	draw_axiom(axiom, ang, dist)
	print(axiom)

main()


