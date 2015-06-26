# -*- coding: utf-8 -*
import math
import maya.api.OpenMaya as OpenMaya

nodeName = 'mlExpmapToEuler'

rotateName = ('rotate', 'r', u'回転')
eulerAngleName = (('rotateX', 'rx', u'回転 X'),
                  ('rotateY', 'ry', u'回転 Y'),
                  ('rotateZ', 'rz', u'回転 Z'))
expmapName = ('expmap', 'em', u'expmap')
expmapElementName = (('expmapX', 'emx', 'X'),
                     ('expmapY', 'emy', 'Y'),
                     ('expmapZ', 'emz', 'Z'))
rotateOrderName  = ('rotateOrder', 'ro', u'回転順序')

def maya_useNewAPI():
    pass

class mlExpmapToEuler(OpenMaya.MPxNode):
    """expmap to euler"""
    rotate = OpenMaya.MObject()
    eulerAngles = []
    expmap = OpenMaya.MObject()
    expmapElement = []
    rotateOrder = OpenMaya.MObject()

    @staticmethod
    def creator():
        return mlExpmapToEuler()

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)

    @staticmethod    
    def initialize():
        # output euler rotation
        cAttr = OpenMaya.MFnCompoundAttribute()
        mlExpmapToEuler.rotate = cAttr.create(rotateName[0], rotateName[1])
        cAttr.keyable = False
        cAttr.writable = False
        cAttr.channelBox = True
        cAttr.setNiceNameOverride(rotateName[2])
        #cAttr.keyable = True
        cAttr.writable = False
        for i in range(0, 3):
            uAttr = OpenMaya.MFnUnitAttribute()
            mlExpmapToEuler.eulerAngles = mlExpmapToEuler.eulerAngles + \
                [uAttr.create(eulerAngleName[i][0], eulerAngleName[i][1], OpenMaya.MFnUnitAttribute.kAngle, 0.0)]
            uAttr.setNiceNameOverride(eulerAngleName[i][2])
            cAttr.addChild(mlExpmapToEuler.eulerAngles[-1])
        mlExpmapToEuler.addAttribute(mlExpmapToEuler.rotate);

        # input expmap
        cAttr = OpenMaya.MFnCompoundAttribute()
        mlExpmapToEuler.expmap = cAttr.create(expmapName[0], expmapName[1])
        cAttr.keyable = True
        cAttr.readable = False
        cAttr.setNiceNameOverride(expmapName[2])
        for i in range(0, 3):
            nAttr = OpenMaya.MFnNumericAttribute()
            mlExpmapToEuler.expmapElement = mlExpmapToEuler.expmapElement + \
                [nAttr.create(expmapElementName[i][0], expmapElementName[i][1], OpenMaya.MFnNumericData.kDouble, 0.0)]
            nAttr.setNiceNameOverride(expmapElementName[i][2])
            uAttr.keyable = True
            uAttr.readable = False
            cAttr.addChild(mlExpmapToEuler.expmapElement[i])
        mlExpmapToEuler.addAttribute(mlExpmapToEuler.expmap)
        mlExpmapToEuler.attributeAffects(mlExpmapToEuler.expmap, mlExpmapToEuler.rotate)

        # rotation order
        nAttr = OpenMaya.MFnNumericAttribute()
        mlExpmapToEuler.rotateOrder = nAttr.create('rotateOrder', 'ro', OpenMaya.MFnNumericData.kInt, 0)
        nAttr.setNiceNameOverride(rotateOrderName[2])
        nAttr.readable = False
        mlExpmapToEuler.addAttribute(mlExpmapToEuler.rotateOrder);
        mlExpmapToEuler.attributeAffects(mlExpmapToEuler.rotateOrder, mlExpmapToEuler.rotate)

    def compute(self, plug, dataBlock):
        if rotateName[0] in plug.name():
            rv = [0.0, 0.0, 0.0]
            for i in xrange(0, 3):
                inputHandle = dataBlock.inputValue(mlExpmapToEuler.expmapElement[i])
                rv[i] = inputHandle.asDouble()
            orderHandle = dataBlock.inputValue(mlExpmapToEuler.rotateOrder)
            exHandle = dataBlock.outputValue(mlExpmapToEuler.eulerAngles[0])
            eyHandle = dataBlock.outputValue(mlExpmapToEuler.eulerAngles[1])
            ezHandle = dataBlock.outputValue(mlExpmapToEuler.eulerAngles[2])
            mag = math.sqrt(rv[0] * rv[0] + rv[1] * rv[1] + rv[2] * rv[2])
            if math.fabs(mag) < 1.0e-6:
                sina = 0
            else:
                sina = math.sin(mag) / mag
            quat = OpenMaya.MQuaternion(rv[0] * sina,
                                        rv[1] * sina,
                                        rv[2] * sina,
                                        math.cos(mag))
            order = orderHandle.asInt()
            euler = OpenMaya.MEulerRotation(0, 0, 0, order)
            euler *= quat
            exHandle.setDouble(euler.x)
            eyHandle.setDouble(euler.y)
            ezHandle.setDouble(euler.z)
            dataBlock.setClean(plug)
