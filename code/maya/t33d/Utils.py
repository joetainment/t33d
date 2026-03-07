import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel


def msg( msg_ , typ="info", doPrint=True ):
    if typ=="error":
        om.error( msg_ )
    if typ=="warning":
        om.warning( msg_ )
    else:
        om.info( msg_ )
    ## Also print the msg
    if doPrint:
        print( msg_ )




