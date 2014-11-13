"""
Code from:
http://forums.cgsociety.org/archive/index.php/t-1124527.html

Written by users BigRoyNL and Palohman
"""
from pymel.all import *
import pymel.core as pm
import pymel.core.datatypes as dt
import maya.cmds as mc
import maya.OpenMaya as om

def getLocalVecToWorldSpaceAPI(obj, vec=om.MVector.yAxis):

	#get selection list
	selList = om.MSelectionList()

	#add object to selection list
	selList.add(obj)

	#get path 
	nodeDagPath = om.MDagPath()

	#get path to object
	selList.getDagPath(0, nodeDagPath)

	transform = om.MFnTransform(nodeDagPath)
	quatWS = om.MQuaternion()
	transform.getRotation( quatWS, om.MSpace.kWorld) 
	transformMX = transform.transformation()
	transformMX.setRotationQuaternion( quatWS.x, quatWS.y, quatWS.z, quatWS.w)
	matrix = transformMX.asMatrix()

	vec = (vec * matrix).normal()
	return dt.Vector(vec.x,vec.y,vec.z)

def apply_tropism(obj, e, tropism, vec=om.MVector.yAxis):
	#get selection list
	selList = om.MSelectionList()

	#add object to selection list
	selList.add(obj)

	#get path 
	nodeDagPath = om.MDagPath()

	#get path to object
	selList.getDagPath(0, nodeDagPath)
	transform = om.MFnTransform(nodeDagPath)
	quatWS = om.MQuaternion()
	transform.getRotation( quatWS, om.MSpace.kWorld) 
	transformMX = transform.transformation()
	transformMX.setRotationQuaternion( quatWS.x, quatWS.y, quatWS.z, quatWS.w)
	matrix = transformMX.asMatrix()

	e=0.2
	
	tropism = tropism.normal()
	tropism = (tropism*e)+getLocalVecToWorldSpaceAPI(obj)
	tropism = (tropism*dt.Matrix(matrix).inverse()).normal()

	quat = dt.Vector(0,1,0).rotateTo(tropism)
	obj.rotateBy(quat,space='preTransform')

	# print(quat.asEulerRotation())
	# print(tropism)

