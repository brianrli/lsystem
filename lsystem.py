"""
LSystems by
Brian Li

Procedural Sakura Trees using Lindenmayer Systems.
"""
import string
import re
import math
from pyparsing import *
import parser as pr
from pymel import *
import pymel.core as pm
import ternary as tn
import pymel.core.datatypes as dt

f = pm.newFile(f=True)

#Class Lsystem, handles generation of Lsystems
class Lsystem:

	#initialize all variables
	def __init__(self,axiom,map_input,iterations, ang, dist,vars):
		print("Lsystem Init")
		self.axiom = axiom
		self.map_input = map_input
		self.depth = iterations
		self.ang = ang
		self.dist = dist
		self.variables = vars 
		self.flower_index = 0

		self.ternaryflag = False
		self.tropism = dt.Vector(0,0,0)
		self.e = 0

		self.branchShader = pm.shadingNode('lambert',asShader=True,name="branchText")
		self.branchShader.setColor([1, 1, 1, 1.0])
		self.leafShader = pm.shadingNode('lambert',asShader=True,name="leafText")
		self.leafShader.setColor([0.72, .32, 0.19, 1.0])

	#process construction parameters and create Sakura Tree
	def create(self):
		print("Create Invoked")
		print(self.axiom)
		proc_axiom = pr.parse_input(self.map_input, self.axiom, self.depth, self.variables)
		print(self.dist)
		print(proc_axiom)
		self.draw_axiom(proc_axiom, self.ang, self.dist)

	#draw the tree given by an axiom
	def draw_axiom(self,axiom,ang,dist):
		stack = []

		zdegr = 0
		ydegr = 0
		xdegr = 0
		width = 0.5
		dist = 0
		world = False
		previous = None
		pdist = 0 #previous distance

		first_itr = True

		for c in axiom:
			
			command = c[0]
			argument = c[1]

			# draw flower
			if command is 'L':
				if argument is 'def':
					argument = self.dist
				current = self.make_flower(self.flower_index)
				self.flower_index += 1
				if previous is not None:
					current.setMatrix(previous.getMatrix(worldSpace=True))
					pm.parent(current,previous)
				pm.scale(15,15,15)
				if xdegr != 0 or zdegr != 0 or ydegr != 0:
					# print(pdist)
					current.translateY.set(pdist)
					# pm.move(0,pdist,0,current,os=True)
					# pm.rotate(current,xdegr,ydegr,zdegr,os=True,relative=True)
					print(width)
					# pm.move(0,width,0,current,os=True,relative=True)
				else:
					pm.move(0,dist+argument/2,0,current,os=True,relative=True)

				zdegr = 0
				ydegr = 0
				xdegr = 0
				dist = 0
				world = False
				previous = current

			if command is 'F':
				print ("{} {} {} {}".format("F command triggered", world, xdegr+ydegr+zdegr,width))
				if argument is 'def':
					argument = self.dist

				if command is 'F':
					current = self.make_branch(argument,width)[0]
				elif command is 'L': 
					current = self.make_flower(self.flower_index)
					# pm.scale(3,3,3)
					self.flower_index += 1
				
				if previous is not None:
					current.setMatrix(previous.getMatrix(worldSpace=True))
					pm.parent(current,previous)
				if command is 'L':
					pm.scale(8,8,8)

				
				#apply rotates and transforms				
				if xdegr != 0 or zdegr != 0 or self.ternaryflag:
					pm.move(0,pdist,0,current,os=True)
					# print(tn.process(current))
					
					if previous is not None and command is 'F' and self.ternaryflag:
						tn.apply_tropism(current,self.e,self.tropism)

					pm.rotate(current,xdegr,ydegr,zdegr,os=True,relative=True)
					if command is 'F':
						pm.move(0,dist+argument/2,0,current,os=True,relative=True)
					if command is 'L':
						pm.move(0,width,0,current,os=True,relative=True)

				else:
					if command is 'F':
						pm.move(0,pdist+dist+argument/2,0,current,os=True,relative=True)
					if command is 'L':
						pm.move(0,dist+argument/2,0,current,os=True,relative=True)

				zdegr = 0
				ydegr = 0
				xdegr = 0
				dist = 0
				world = False
				
				if command is 'F':
					pdist = argument/2

				# print(xdegr)
				previous = current

			elif command is 'f':
				if argument is 'def':
					dist = 5
				else:
					dist = argument

			elif command is '-':
				if argument is 'def':
					argument = ang
				zdegr += -argument
				print ("{} {}".format("- command triggered", zdegr))

			elif command is '+':
				if argument is 'def':
					argument = ang
				zdegr += argument
				print ("{} {}".format("+ command triggered", zdegr))

			elif command is '&':
				if argument is 'def':
					argument = ang
				print("& command triggered")
				xdegr += -argument
				print ("{} {}".format("+ command triggered", xdegr))

			elif command is '^':
				if argument is 'def':
					argument = ang
				xdegr += argument

			elif command == "\\":
				print("\\ command triggered")
				ydegr += -argument

			elif command is '/':
				if argument is 'def':
					argument = ang
				ydegr += argument

			elif command is '[':
				print("[ triggered")
				stack.append([previous,xdegr,ydegr,zdegr,width,dist,world])
				# print(stack)

			elif command is ']':
				print("] triggered")
				# print(stack)
				prev_state = stack.pop()
				previous = prev_state[0]
				xdegr = prev_state[1]
				ydegr = prev_state[2]
				zdegr = prev_state[3]
				width = prev_state[4]
				dist = prev_state[5]
				world = prev_state[6]
				# print(stack)

			#decrement width
			elif command is '!':
				print("! triggered")
				if argument is 'def':
					width*=0.9
				else:
					width = argument

			#rotate Y and until Z-axis is horizontal (WIP)
			elif command is '$':
				pass
				# print("$ triggered")
				# world = True

	#references from flower.mb
	def make_flower(self,flower_index):
		pm.system.importFile("/Users/brianli/Desktop/Fall2014/lsystem/flower.mb",namespace="flower"+str(flower_index))
		i = pm.nodetypes.Transform("flower"+str(flower_index)+":Flower")
		pm.select(i,hi=False)
		# pm.hyperShade(assign=self.flowerShader)
		return i

	#make branch
	def make_branch(self,h,w):
		print(w)
		i = pm.polyCylinder(height=h,radius=w)
		pm.select(i[0])
		pm.hyperShade(assign=self.branchShader)
		print("Constructed {} {} {}".format(i[0],h,w))
		return i

	#make leaf
	def make_leaf(self):
		i = pm.polyCube(w=.5,d=1.5,h=4,sw=3,sh=3)
		pm.select(i[0].vtx[12:19])
		pm.scale(0.1,0.1,1,r=True)
		pm.select(i[0].vtx[0:3],i[0].vtx[28:31])
		pm.scale(0.1,0.1,1,r=True)
		pm.select(i[0].vtx[4],i[0].vtx[7:8],i[0].vtx[11],i[0].vtx[20],i[0].vtx[23:24],i[0].vtx[27]) 
		pm.scale(0.8,0.8,0.8)
		pm.select(i[0])
		pm.hyperShade(assign=Lsystem.leafShader)
		return i

def apply_tropism(obj,tropism,e):
	pass


#for testing purposes
def main():
	variables = {}
	#key variables

	#test input1
	map_input = \
'''F(w):F(w)F(w)
X(w):F(w)[+X(w)][-X(w)]F(w)X(w)'''
	axiom = "X(10)"

	#test input 2
	variables = {
		'r1':0.9,
		'r2':0.9,
		'a0':45,
		'a2':45,
		'd':137.5,
		'wr':0.707,
	}
	map_input = \
'''A(l,w):!(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)
B(l,w):!(w)F(l)[-(a2)$C(l*r2,w*wr)]C(l*r1,w*wr)
C(l,w):!(w)F(l)[+(a2)$B(l*r2,w*wr)]B(l*r1,w*wr)'''
# 	map_input = \
# '''A(l,w):!(w)F(l)[&(a0)B(l*r2,w*wr)]/(d)A(l*r1,w*wr)
# B(l,w):!(w)F(l)[-(a2)C(l*r2,w*wr)]C(l*r1,w*wr)
# C(l,w):!(w)F(l)[+(a2)B(l*r2,w*wr)]B(l*r1,w*wr)'''
	axiom = "A(10,0.5)"

	#test input 3
	variables ={
		'd1':94.74,
		'd2':132.63,
		'a':18.95,
		'lr':1.109,
		'vr':1.732
	}
	axiom = "!(1)F(200)/(45)A"
	map_input =\
'''A:!(vr)F(50)[&(a)F(50)A]/(d1)[&(a)F(50)A]/d2[&(a)F(50)A]
F(l):F(l*lr)
!(w):!(w*vr)'''
	
	iterations = 4
	dist = 5
	ang = 25.7
	
	print("Commence Lsystem Construction")
	test = Lsystem(axiom, map_input, iterations, ang, dist,variables)
	test.create()
# main()


