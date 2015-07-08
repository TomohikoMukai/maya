# -*- coding: utf-8 -*
import math
import maya.api.OpenMaya as OpenMaya

nodeName = 'mlEulerToExpmap'

expmapName = ('expmap', 'em', u'Expmap')
expmapElementName = (('expmapX', 'emx', 'Expmap X'),
                     ('expmapY', 'emy', 'Expmap Y'),
                     ('expmapZ', 'emz', 'Expmap Z'))
rotateName  = ('rotate', 'ir', u'回転')
eulerAngleName  = (('rotateX', 'rx', u'回転 X'),
                   ('rotateY', 'ry', u'回転 Y'),
                   ('rotateZ', 'rz', u'回転 Z'))
rotateOrderName  = ('rotateOrder', 'ro', u'回転順序')

def maya_useNewAPI():
    pass

class mlEulerToExpmap(OpenMaya.MPxNode):
    """euler to expmap"""    
    rotate = OpenMaya.MObject()
    eulerAngles = []
    expmap = OpenMaya.MObject()
    expmapElement = []
    
    def __init__(self):
        OpenMaya.MPxNode.__init__(self) 

    @staticmethod
    def creator():
        return mlEulerToExpmap()

    @staticmethod
    def initialize():
        # output expmap
        cAttr = OpenMaya.MFnCompoundAttribute()
        mlEulerToExpmap.expmap = cAttr.create(expmapName[0], expmapName[1])
        cAttr.setNiceNameOverride(expmapName[2])
        mlEulerToExpmap.expmapElement = []
        for i in xrange(0, 3):
            nAttr = OpenMaya.MFnNumericAttribute()
            mlEulerToExpmap.expmapElement = mlEulerToExpmap.expmapElement + \
                [nAttr.create(expmapElementName[i][0],
                                expmapElementName[i][1],
                                OpenMaya.MFnNumericData.kDouble,
                                0.0)]
            nAttr.setNiceNameOverride(expmapElementName[i][2])
            nAttr.keyable = False
            nAttr.writable = False
            cAttr.addChild(mlEulerToExpmap.expmapElement[i])
        mlEulerToExpmap.addAttribute(mlEulerToExpmap.expmap)
        
        # input Euler angles
        cAttr = OpenMaya.MFnCompoundAttribute()
        mlEulerToExpmap.rotate = cAttr.create(rotateName[0], rotateName[1])
        cAttr.setNiceNameOverride(rotateName[2])
        mlEulerToExpmap.eulerAngles = []
        for i in xrange(0, 3):
            uAttr = OpenMaya.MFnUnitAttribute()
            mlEulerToExpmap.eulerAngles = mlEulerToExpmap.eulerAngles + \
                [uAttr.create(eulerAngleName[i][0],
                                eulerAngleName[i][1],
                                OpenMaya.MFnUnitAttribute.kAngle,
                                0.0)]
            uAttr.setNiceNameOverride(eulerAngleName[i][2])
            uAttr.keyable = True
            uAttr.readable = False
            cAttr.addChild(mlEulerToExpmap.eulerAngles[i])
        mlEulerToExpmap.addAttribute(mlEulerToExpmap.rotate)
        mlEulerToExpmap.attributeAffects(mlEulerToExpmap.rotate, mlEulerToExpmap.expmap)

        # input rotation order
        nAttr = OpenMaya.MFnNumericAttribute()
        mlEulerToExpmap.rotateOrder = nAttr.create(rotateOrderName[0],
                                                    rotateOrderName[1],
                                                    OpenMaya.MFnNumericData.kInt,
                                                    0)
        nAttr.setNiceNameOverride(rotateOrderName[2])
        nAttr.readable = False
        mlEulerToExpmap.addAttribute(mlEulerToExpmap.rotateOrder)
        mlEulerToExpmap.attributeAffects(mlEulerToExpmap.rotateOrder, mlEulerToExpmap.expmap)

    def compute(self, plug, dataBlock):
        if plug is not self.expmap and plug not in self.expmapElement:
            return

        r = [0, 0, 0]
        for i in xrange(0, 3):
            rHandle = dataBlock.inputValue(mlEulerToExpmap.eulerAngles[i])
            r[i] = rHandle.asDouble()
        roHandle = dataBlock.inputValue(mlEulerToExpmap.rotateOrder)
        rotateOrder = roHandle.asInt()
        eulerRotation = OpenMaya.MEulerRotation(r[0], r[1], r[2], rotateOrder)
        q = eulerRotation.asQuaternion()
        if q.w < 0:
            q = -q
        if math.fabs(q.w) > 1.0 - 1.0e-6:
            a = 0.0
            isina = 0.0
        else:
            a = math.acos(q.w)
            isina = a / math.sin(a)
        ln = (q.x * isina, q.y * isina, q.z * isina)
        for i in xrange(0, 3):
            outputHandle = dataBlock.outputValue(mlEulerToExpmap.expmapElement[i])
            outputHandle.setDouble(ln[i])
        dataBlock.setClean(plug)
