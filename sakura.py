import maya.cmds as cmds
from lsystem import Lsystem
from optwin import AR_OptionsWindow
from parser import create_dict

#---strings---
#variables
#axiom
#map_input

#---variables---
#iteration depth
#default dist
#default ang

#--optional--
#progress bar

class SK_OptionsWindow(AR_OptionsWindow):
	def __init__(self):
		AR_OptionsWindow.__init__(self)
		self.title = 'Sakura Generator'
		self.actionName = 'Create'
		self.sakuraTree = Lsystem("", "", 0, 0, 0, {})

	def displayOptions(self):
		
		#Depth, Default Distance, Default Angle, Axiom
		self.constructGrp = cmds.frameLayout(
			label='Construction Parameters'
			)
		cmds.formLayout(
			self.optionsForm,e=True,
			attachForm=(
				[self.constructGrp,'top',0],
				[self.constructGrp,'left',0],
				[self.constructGrp,'right',0]
				)
			)
		self.constructCol = cmds.columnLayout(adj=True)
		self.depth = cmds.intFieldGrp(
			label='Depth: ',
			numberOfFields=1,
			value1=1
			)
		self.dist = cmds.floatFieldGrp(
			label='Default Distance: ',
			numberOfFields=1,
			value1=5
			)
		self.ang = cmds.floatFieldGrp(
			label='Default Angle: ',
			numberOfFields=1,
			value1=90
			)
		self.axiom = cmds.textFieldGrp(
			label='Axiom: '
		)

		cmds.setParent(self.optionsForm)
		self.projectionGrp = cmds.frameLayout(
			label='Projections'
			)
		cmds.formLayout(
			self.optionsForm,e=True,
			attachControl=(
				[self.projectionGrp,'top',0,self.constructGrp]
				),
			attachForm=(
				[self.projectionGrp,'left',0],
				[self.projectionGrp,'right',0]
				)
			)
		self.projectionCol = cmds.columnLayout(columnAttach=('left',0),adj=True)
		self.projections = cmds.scrollField(editable=True)

		cmds.setParent(self.optionsForm)
		self.variableGrp = cmds.frameLayout(
			label='Variables'
			)
		cmds.formLayout(
			self.optionsForm,e=True,
			attachControl=(
				[self.variableGrp,'top',0,self.projectionGrp]
				),
			attachForm=(
				[self.variableGrp,'left',0],
				[self.variableGrp,'right',0]
				)
			)
		self.variableCol = cmds.columnLayout(adj=True)
		self.variables = cmds.scrollField( editable=True)


	def applyBtnCmd(self,*args):
		self.sakuraTree.axiom = cmds.textFieldGrp(
			self.axiom,q=True,
			text=True
			)
		self.sakuraTree.depth = cmds.intFieldGrp(
			self.depth,q=True,
			value1=True
			)
		self.sakuraTree.dist = cmds.floatFieldGrp(
			self.dist,q=True,
			value1=True
			)
		self.sakuraTree.ang = cmds.floatFieldGrp(
			self.ang,q=True,
			value1=True
			)
		self.sakuraTree.map_input = cmds.scrollField(
			self.projections,q=True,
			text=True
			)
		self.sakuraTree.variables = create_dict(cmds.scrollField(
			self.variables,q=True,
			text=True
			))

		# print(self.sakuraTree.axiom)
		# print(self.sakuraTree.depth)
		# print(self.sakuraTree.map_input)
		# self.objIndAsCmd={
		# 	1:cmds.polyCube,
		# 	2:cmds.polyCone,
		# 	3:cmds.polyCylinder,
		# 	4:cmds.polySphere
		# }
		# objIndex =cmds.radioButtonGrp(
		# 	self.objType,q=True,
		# 	select=True
		# 	)
		# newobject=self.objIndAsCmd[objIndex]()
		self.sakuraTree.create()
SK_OptionsWindow.showUI()

