"""
LSystems by
Brian Li

A basic (my first) maya scripting project.
"""
import string
import re
from pyparsing import *
from pymel import *
import pymel.core as pm

f = pm.newFile(f=True)
class Lsystem:

	branchShader = pm.shadingNode('lambert',asShader=True)
	branchShader.setColor([0, .9, 0, 1.0])
	leafShader = pm.shadingNode('phong',asShader=True)
	leafShader.setColor([0.72, .32, 0.19, 1.0])

	def __init__(self,axiom,map_input,iterations, ang, dist):
		proc_axiom = self.parse_input(axiom,map_input,iterations)
		self.draw_axiom(proc_axiom, ang, dist)
		print(proc_axiom)

	def parse_input(self,axiom,map_input,iterations):
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

	def parse_args(self,in_string):
		instructions = []
		m = re.findall("([FXf\+&/])(\(.*?\))?",in_string)
		for pair in m:
			item = []
			item.append(pair[0])
			if pair[1] is '':
				item.append(pair[0]+"def")
			else:
				item.append(re.match("\((.*?)\)", pair[1]).group(1))
			instructions.append(item)
		return instructions

	def draw_axiom(self,axiom,ang,dist):

		axiom = "LLLL"
		stack = []

		zdegr = 0
		ydegr = 0
		xdegr = 0

		first_itr = True
		flower_index = 0

		# axiom = "F-FFFF-F"
		for command in axiom:
			
			print(command)
			if command is 'F' or command is 'L':
				print ("{} {}".format("F command triggered", xdegr))

				if command is 'F':
					current = self.make_branch()[0]
				elif command is 'L':
					current = self.make_flower(flower_index)
					flower_index += 1
					# current = make_leaf()[0]
				
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

	def make_flower(self,flower_index):
		pm.system.importFile("/Users/brianli/Desktop/Fall2014/lsystem/flower.mb",namespace="flower"+str(flower_index))
		i = pm.nodetypes.Transform("flower"+str(flower_index)+":Flower")
		return i

	def make_branch(self):
		i = pm.polyCube(height=5)
		pm.select(i[0])
		pm.hyperShade(assign=branchShader)
		return i

	def make_leaf(self):
		i = pm.polyCube(w=.5,d=1.5,h=4,sw=3,sh=3)
		pm.select(i[0].vtx[12:19])
		pm.scale(0.1,0.1,1,r=True)
		pm.select(i[0].vtx[0:3],i[0].vtx[28:31])
		pm.scale(0.1,0.1,1,r=True)
		pm.select(i[0].vtx[4],i[0].vtx[7:8],i[0].vtx[11],i[0].vtx[20],i[0].vtx[23:24],i[0].vtx[27]) 
		pm.scale(0.8,0.8,0.8)
		pm.select(i[0])
		pm.hyperShade(assign=leafShader)
		return i

def main():
	
	
	#key variables
	map_input = \
	'''F:FF
	X:F[+X][-X]FX'''
	axiom = "X"
	
	iterations = 3
	dist = 5
	ang = 25.7

	Lsystem(axiom, map_input, iterations, ang, dist)
	
# 	axiom = parse_input(axiom,map_input,iterations)
# 	draw_axiom(axiom, ang, dist)
# 	print(axiom)

main()


