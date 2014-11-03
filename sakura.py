import maya.cmds as cmds
import re
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

#--todo--
#read/write/load files

skFileExtension = 'sk'

class SK_OptionsWindow(AR_OptionsWindow):
	def __init__(self):
		AR_OptionsWindow.__init__(self)
		self.title = 'Sakura Generator'
		self.actionName = 'Create'
		print("Window Init")
		self.sakuraTree = Lsystem("", "", 0, 0, 0, {})
		print(self.sakuraTree.branchShader)
		self.fileFilter = 'Sakura (*.%s)'%skFileExtension

	def loadFile(self,*args):
		filePath = ''
		filePath = cmds.fileDialog2(
			ff=self.fileFilter, fileMode=1
			)
		if filePath is None or len(filePath) < 1: return
		if isinstance(filePath, list): filePath = filePath[0]
		try:
			f = open(filePath, 'r')
		except:
			cmds.confirmDialog(
				t='Error', b=['OK'],
				m='Unable to open file: %s'%filePath
			)
			raise
		try:
			fileInput = re.split(";",str(f.read()))
			cmds.textFieldGrp(self.axiom,e=True,text=fileInput[0])
			cmds.intFieldGrp(self.depth,e=True,value1=int(fileInput[1]))
			cmds.floatFieldGrp(self.dist,e=True,value1=float(fileInput[2]))
			cmds.floatFieldGrp(self.ang,e=True,value1=float(fileInput[3]))
			cmds.scrollField(self.projections,e=True,text=fileInput[4])
			cmds.scrollField(self.variables,e=True,text=fileInput[5])
		except:
		   	cmds.error("Error reading from SK file.")
		f.close()	      
		print 'Template Loaded Successfully'

	def saveFile(self,*args):
		cmds.showWindow()
		filePath = ''
		# try:
		filePath = cmds.fileDialog2(
			ff=self.fileFilter, fileMode=0
		)
		if filePath is None or len(filePath) < 1: return
		if isinstance(filePath, list): filePath = filePath[0]
		try: 
			f = open(filePath, 'w')
		except:
			cmds.confirmDialog(
				t='Error', b=['OK'],
				m='Unable to write file: %s'%filePath
			)
			raise

		try:
			self.storeArguments()
			f.write(str(self.sakuraTree.axiom)+";")
			f.write(str(self.sakuraTree.depth)+";")
			f.write(str(self.sakuraTree.dist)+";")
			f.write(str(self.sakuraTree.ang)+";")
			f.write(str(self.sakuraTree.map_input)+";")
			f.write(str(cmds.scrollField(
							self.variables,q=True,
							text=True
							))+";")
		except:
			cmds.error("Error Writing to File")
		print 'Sakura template saved to '+filePath

	def displayOptions(self):
		#Depth, Default Distance, Default Angle, Axiom
		self.constructGrp = cmds.frameLayout(
			label='Construction Parameters',
			collapsable=True
			)
		cmds.formLayout(
			self.optionsForm,e=True,
			attachForm=(
				[self.constructGrp,'right',0],
				[self.constructGrp,'top',0],
				[self.constructGrp,'left',0]
				),
			attachPosition = (
				[self.constructGrp,'left',1,0],
				[self.constructGrp,'right',1,100]
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
			label='Projection Settings',
			collapsable=True
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
			label='Variable Settings',
			collapsable=True
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
		self.variables = cmds.scrollField(editable=True)

		cmds.setParent(self.optionsForm)
		self.fileGrp = cmds.frameLayout(
			label='File Commands',
			collapsable=True
			)
		cmds.formLayout(
			self.optionsForm,e=True,
			attachControl=(
				[self.fileGrp,'top',0,self.variableGrp]
				),
			attachForm=(
				[self.fileGrp,'left',0],
				[self.fileGrp,'right',0]
				)
			)
		self.fileCol = cmds.columnLayout( adjustableColumn=True )
		self.loadFile = cmds.button( label='Load Template', c=self.loadFile)
		self.saveFile = cmds.button( label='Save Template', c=self.saveFile)

	def storeArguments(self):
		try:
			self.sakuraTree.axiom = cmds.textFieldGrp(
				self.axiom,q=True,
				text=True
				)
		except:
			cmds.error("Invalid Axiom")

		try:
			self.sakuraTree.depth = cmds.intFieldGrp(
				self.depth,q=True,
				value1=True
				)
		except:
			cmds.error("Invalid Depth")

		try:
			self.sakuraTree.dist = cmds.floatFieldGrp(
				self.dist,q=True,
				value1=True
				)
		except:
			cmds.error("Invalid Default Distance")
		
		try:
			self.sakuraTree.ang = cmds.floatFieldGrp(
				self.ang,q=True,
				value1=True
				)
		except:
			cmds.error("Invalid Default Angle")
			
		try:
			self.sakuraTree.map_input = cmds.scrollField(
				self.projections,q=True,
				text=True
				)
		except:
			cmds.error("Invalid Projections")
		
		try:
			self.sakuraTree.variables = create_dict(cmds.scrollField(
				self.variables,q=True,
				text=True
				))
		except:
			cmds.error("Invalid Variables")

	def applyBtnCmd(self,*args):
		self.storeArguments()
		self.sakuraTree.create()
		print("Sakura Created")
SK_OptionsWindow.showUI()

