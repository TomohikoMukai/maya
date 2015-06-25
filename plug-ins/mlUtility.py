# -*- coding: utf-8 -*
import sys
import math
import maya.api.OpenMaya as OpenMaya
import mkilab.utility.mlEulerToExpmap as mlEulerToExpmap
import mkilab.utility.mlExpmapToEuler as mlExpmapToEuler

mlEulerToExpmapId = OpenMaya.MTypeId(0x00000)
mlExpmapToEulerId = OpenMaya.MTypeId(0x00001)

def maya_useNewAPI():
    pass

def initializePlugin(plugin):
    fnPlugin = OpenMaya.MFnPlugin(plugin, vendor = 'MukaiLab', version = '0.1')
    try:
        fnPlugin.registerNode(mlEulerToExpmap.nodeName,
                              mlEulerToExpmapId,
                              mlEulerToExpmap.mlEulerToExpmap.creator,
                              mlEulerToExpmap.mlEulerToExpmap.initialize,
                              OpenMaya.MPxNode.kDependNode,
                              'utility/general')
    except:
        sys.stderr.write('Failed to register node: %s' % mlEulerToExpmap.nodeName)
        raise
    try:
        fnPlugin.registerNode(mlExpmapToEuler.nodeName,
                              mlExpmapToEulerId,
                              mlExpmapToEuler.mlExpmapToEuler.creator,
                              mlExpmapToEuler.mlExpmapToEuler.initialize,
                              OpenMaya.MPxNode.kDependNode,
                              'utility/general')
    except:
        sys.stderr.write('Failed to register node: %s' % mlExpmapToEuler.nodeName)
        raise

def uninitializePlugin(plugin):
    fnPlugin = OpenMaya.MFnPlugin(plugin)
    try:
        fnPlugin.deregisterNode(mlEulerToExpmapId)
    except:
        sys.stderr.write('Failed to deregister node: %s' % mlEulerToExpmap.nodeName)
        raise
    try:
        fnPlugin.deregisterNode(mlExpmapToEulerId)
    except:
        sys.stderr.write('Failed to deregister node: %s' % mlExpmapToEuler.nodeName)
        raise
