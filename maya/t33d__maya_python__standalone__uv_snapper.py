"""
A tool for snapping UVs since snapping on individual axes 
doesn't work for some people in Maya 2022.

Part of the T33d scripts package.
"""
import maya.cmds as cmds


class T33dUvSnapper(object):
    def __init__(self):
        
        self.nameForUiWindow = "T33dUvSnapperWindow"
        self.targetLoc = None
        self.tmpCurrentLoc = None
        self.tmpPivotObj = None
        
        self.makeUi()

    def makeUi(self):
        if cmds.window( self.nameForUiWindow, exists=True):
            cmds.deleteUI( self.nameForUiWindow )
        
        self.win = cmds.window(
            self.nameForUiWindow,
            title="T33d Uv Snapper" )
            #assert self.nameForUiWindow == self.win
        self.layout = cmds.columnLayout( parent=self.win )
        self.setTargetBtn = cmds.button(
            label="Set Target",
            c=lambda x: self.setTarget()
        )
        self.snapToTargetInUBtn = cmds.button(
            label="Snap To Target In U",
            c=lambda x: self.snapToTargetInU()            
        )
        self.snapToTargetInUBtn = cmds.button(
            label="Snap To Target In V",
            c=lambda x: self.snapToTargetInV()          
        )
        self.snapToTargetInUBtn = cmds.button(
            label="Snap To Target In Both U and V",
            c=lambda x: self.snapToTargetInUAndV()            
        )
        cmds.showWindow( self.win )

    def getManipFromUvs(self):
        sel = cmds.ls( sl=True )
        uniqObjs = {}
        for e in sel:
            if ".map" in e:
                #uniqObjs[ e.split('.')[0] ] = True
                pivotObj = e.split('.')[0]
                self.tmpPivotObj = pivotObj
                break  ##  because,
                ## for some reason, we only want first in sel
                ## other don't have right uvPivot
                ## perhaps Maya's UI only tracks the uvPivot
                ## of the first selected uv/obj
                ## even when working with selections
                ## including uvs on multiple objects

        tLoc = None
        ## This loop wasn't needed due to single obj
        ## issue noted above
        #for o in uniqObjs: 
        #    print( o )
        #    ## locations will be list of tuples
        
        ## Instead, we just use pivotObj
        src = pivotObj + ".uvPivot"  #print( f"src: {src}" )
        locations = cmds.getAttr( src )  #print( locations )
        tLoc = locations[0]
        return tLoc
        
    def setTarget(self):
        self.targetLoc = self.getManipFromUvs()
        print( self.targetLoc )
        
    def calcDelta(self, cLoc, tLoc):
        """calcs delta (difference) from current to target"""
        return ( tLoc[0] - cLoc[0], tLoc[1] - cLoc[1] )
        
    def getDelta(self):
        """Gets delta in context of use, """
        """from current manip to stored."""
        """Requires target to have been set already."""
        if self.targetLoc is None:
            header = "\n\nWarning From T33d UV Snapper:\n    "
            msg =  "Target must be set before snapping to it."
            print( header + msg )
            raise Exception( msg )

        cLoc = self.getManipFromUvs()
        self.tmpCurrentLoc = cLoc
        tLoc = self.targetLoc
        delta = self.calcDelta( cLoc, tLoc )
        return delta

    def snapToTargetInU(self):
        delta = self.getDelta()
        deltaU = delta[0]
        cmds.polyEditUV( u=deltaU )
        self.postFixForPivot( deltaU, 0.0   )
                
    def snapToTargetInV(self):
        delta = self.getDelta()
        deltaV = delta[1]
        cmds.polyEditUV( v=deltaV )
        self.postFixForPivot( 0.0, deltaV )
        
    def snapToTargetInUAndV(self):
        delta = self.getDelta()
        deltaU, deltaV = delta[0], delta[1]
        cmds.polyEditUV( u=deltaU, v=deltaV )
        self.postFixForPivot( deltaU, deltaV )
        
    def postFixForPivot(self, deltaU, deltaV ):
        ## self.getDelta stored a tmp cLoc on self
        cLoc = self.tmpCurrentLoc 
        destLoc = (  cLoc[0] + deltaU,  cLoc[1] + deltaV  )
        cmds.setAttr(
            self.tmpPivotObj + ".uvPivot",
            destLoc[0], destLoc[1]
        )
        
        
        #cLoc = cmds.getAttr
        #startUvObjName = str(J.startUv).split( '.' )[0]
        #startUvp = J.pm.getAttr( startUvObjName +".uvPivot" )

app = T33dUvSnapper()