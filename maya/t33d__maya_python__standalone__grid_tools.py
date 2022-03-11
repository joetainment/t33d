"""
GridToolsUi - An example GUI tool for 
working with "powers of two" grid sizes in Maya

Originally Written by Joe Crawford

"""

import traceback
import pymel
import pymel.all as pm
import maya
import maya.cmds
import maya.cmds as cmds

class T33d_GridToolsFuncs(object):
    
    _Instance = None
    
    @classmethod
    def GetInstance(cls):
        return cls.__Instance    
    
    @classmethod
    def reset(cls, setManip=False):
        pymel.all.grid(reset=True)
        if setManip==True:
            ## Reset grid is spacing of 5 with 5 divisions,
            ## ends up being just 1.0
            cls.setManipToSpacing( 1.0 )

    @classmethod       
    def reset_via_numbers( cls, multiplier=1.0, spacing=1.0, wholeSize=4096, setManip=False):
        ##Reset, but remember, default grid size is wacky, based on 5.0
        pymel.all.grid(reset=True)
        ## now change it to be power of two friendly 1.0*multiplier
        ## also set divisions to one and size
        pymel.all.grid( 
            size = wholeSize * multiplier,
            spacing = spacing * multiplier,
            divisions = 1
        )
        if setManip==True:
            cls.setManipToSpacing( spacing*multiplier )
       

    @classmethod        
    def getWholeSize(cls):
        """
        This function gets the size of the *entire* grid,
        not the spacing between grid lines.
        """
        return pymel.all.grid( query=True, size=True )

    @classmethod
    def setWholeSize( cls, wholeSize):
        """
        This function sets the size of the *entire* grid,
        not the spacing between grid lines.
        """
        pymel.all.grid( size=wholeSize )

    @classmethod        
    def getSpacing( cls, log=False):
        sp = pymel.all.grid( query=True, spacing=True )
        if log:
            print( "Grid spacing value is: " + str(sp) )
        return sp

    @classmethod        
    def getDivisions( cls, log=False):
        sp = pymel.all.grid( query=True, divisions=True )
        if sp < 1:  ## Just in case maya ever gives us a number lower than the logically smallest
            sp = 1
        if log:
            print( "Grid spacing value is: " + str(sp) )
        return sp

    @classmethod
    def setSpacing( cls, spacing, setManip=False, log=False):
        if log:
            print( "Grid spacing value is: " + str(sp) )        
        pymel.all.grid( spacing=spacing )
        if setManip:
            cls.setManipToSpacing(spacing)

    @classmethod
    def setManipToSpacing( cls,spacing ):
        pymel.all.manipMoveContext( 'Move', e=True, snapRelative=True, snapValue=spacing )

    @classmethod
    def grow( cls, setManip=False, log=False):
        spacing = cls.getSpacing( log=log)
        new_spacing = spacing * 2
        cls.setSpacing( new_spacing, setManip=setManip )
        if log:
            cls.showMsg( "Grid size: "  + str(cls.getSpacing())  )
            
    @classmethod
    def showMsg(cls, msg):
        pm.inViewMessage( smg=msg, fade = True, fadeStayTime=300, fadeOutTime=1 )  # amg=msg, smg=msg, 
        #if log==True:
        #    pymel.all.warning(    "Grid spacing value is: " + str(  cls.getSpacing() )    )        

    @classmethod         
    def shrink( cls, setManip=False, log=False):
        spacing = cls.getSpacing( log=log)
        new_spacing = spacing * 0.5
        cls.setSpacing( new_spacing, setManip=setManip, )
        if log:
            cls.showMsg( "Grid size: "  + str(cls.getSpacing())  )
            
    @classmethod            
    def putSelectedVertsOnGrid(cls):
        cls.snapVertsToGrid()  ## basically just an alias of the function name

    @classmethod            
    def snapVertsToGrid(cls):
        originalSelection = pymel.all.ls( selection=True, flatten=True )
        pymel.all.mel.eval('ConvertSelectionToVertices;')
        selVerts = pymel.all.ls( selection=True, flatten=True )
        #objectSelection = pymel.all.ls(selection=True, shapes=True )
        
        #selObjs = originalSelection[:]  ## copy the list
        #selVerts = pymel.all.polyListComponentConversion(
        #    fromFace=True, fromVertex=True, fromEdge=True,
        #    fromVertexFace=True,
        #    toVertex=True )
        #    
        #selVerts = 
            
            
            
        spacing = cls.getSpacing()
        divisions = cls.getDivisions()
        
        spacingOfDivisions = spacing / float(divisions)
        
        for item in selVerts:
            if isinstance( item, pymel.all.MeshVertex ):
                for v in item:
                    pW = v.getPosition(space='world')
                    p = pW.homogenize()  ## Turn it into simply coords
                    #print( type(p.x)  )                
                    def onGrid(n, s):
                        return (  spacingOfDivisions * float(   round( n/float(s) )  )   )
                    p.x = onGrid( p.x, spacingOfDivisions )
                    p.y = onGrid( p.y, spacingOfDivisions )
                    p.z = onGrid( p.z, spacingOfDivisions )
                    #print( p.x, p.y, p.z )                               
                    v.setPosition( p.homogenize(), space='world' )
                    #print p.x,p.y,p.z
                    #print( help(p)  )
                    #break
        pymel.all.select( originalSelection )
        



    @classmethod                   
    def getGridSnappableSpacing(cls):
        snappableSpacing = pm.grid(query=True, spacing=True)/pm.grid(query=True, divisions=True)
        return snappableSpacing


    @classmethod           
    def putSelectedObjsOnGrid(cls):
        ss = cls.getGridSnappableSpacing()
        cls.putSelectedObjsOnSnappableSpacing(ss)

        
    @classmethod           
    def putSelectedObjsOnSnappableSpacing(cls,snappableSpacing):
        oSel = pm.ls(selection=True)
        objs = oSel[:]
        for obj in objs:
            cls.putObjOnSnappableSpacing(obj, snappableSpacing  )
        pm.select(oSel)


    @classmethod           
    def putObjsOnSnappableSpacing( cls, objs, snappableSpacing ):
        oSel = pm.ls(selection=True)
        for obj in objs:
            cls.putObjOnSnappableSpacing( obj, snappableSpacing )
        usedObj = obj
        

    @classmethod           
    def putObjOnSnappableSpacing( cls, obj, snappableSpacing ):
        oSel = pm.ls(selection=True)
        destinationObj = obj
        usedObj = obj
        
        
        pm.select( destinationObj )
        t = pm.xform(query=True, rotatePivot=True, worldSpace=True )
        vt = pm.core.datatypes.Vector( t[0], t[1], t[2] )
        vt = cls.onSnappableSpacingVec(vt, snappableSpacing)
        
        
        pm.select( usedObj )
        pm.move( vt, worldSpace=True, absolute=True, worldSpaceDistance=True)
        
        ## We compensate by getting the *object being moved*'s
        ## pivot
        t2 = pm.xform(query=True, rotatePivot=True, worldSpace=True )
        vt2 = pm.core.datatypes.Vector( t2[0], t2[1], t2[2] )
        
        ## vExtra is the additional amount compensated
        vExtra = vt - vt2
        
        vDest = vt+vExtra
        
        vFinal = vDest
        
        pm.move( vFinal, worldSpace=True, absolute=True, worldSpaceDistance=True)
        
        pm.select(oSel)

    @classmethod           
    def onSnappableSpacing(cls, n, snappableSpacing):
        return (  snappableSpacing * float(   round( n/float(snappableSpacing) )  )   )

    @classmethod           
    def onSnappableSpacingVec( cls, v, snappableSpacing):
        ## Only points need to use homogen
        ## this is simply a vector...
        #vh = v.homogenize()
        x = cls.onSnappableSpacing( v.x, snappableSpacing )
        y = cls.onSnappableSpacing( v.y, snappableSpacing )
        z = cls.onSnappableSpacing( v.z, snappableSpacing )    
        return pm.core.datatypes.Vector( x,y,z )


class T33d_GridToolsUi(object):
    
    _Instance = None
    
    @classmethod
    def GetInstance(cls):
        return cls.__Instance
    
    def __init__(self):
        self.annotationAboutInteraction = (
            "The settings should also auto apply when you change them,\n "+
            "but due to a Maya bug, you may occasionally have to apply manually,\n "+
            "with the button."
        )
        self.gtFuncs = T33d_GridToolsFuncs
        
        initialMultiplier = 1.0
        
        initialSpacing =(
            (    pm.grid( query=True, spacing=True ) / pm.grid( query=True, divisions=True )    )
            /
            initialMultiplier
        )
        initialWholeSize = pm.grid( query=True, size=True ) / initialMultiplier
        self.widgets = {}
        parentWidget = self.widgets['parentWidget'] = pm.Window(
                title=" Grid Tools Ui", width=100,height=200
            )
            
        ## Make a shortcut for function that addWidgets
        aw = self.addWidget
        
        with parentWidget:
          with aw( 'col', pm.ColumnLayout() ):
            aw('mayaOptionsButton',pm.Button(label="Maya Grid Options...",
                    command= lambda x: pm.mel.eval("GridOptions;")
                )
            )
            aw('resetButton', pm.Button(label="Reset (To Maya Defaults)",
                command= lambda x: self.resetToMayaDefault()  ) )
            #aw('resetText', pm.Text(label='  '))
            aw('reset2Button', pm.Button(
                    label="Apply These Settings",
                    annotation=self.annotationAboutInteraction,
                    command= lambda x: self.gtFuncs.reset_via_numbers(
                        multiplier=self.getMultiplierFromUi(),
                        spacing=self.getSpacingFromUi(),
                        wholeSize=self.getWholeSizeFromUi(),
                        setManip=True,
                    )
                )
            )
            
            
            ## note the "with" doesn't work with rows,
            ## so we manually specify parents
            priorParent=self.widgets['col']
            
            row1 = self.widgets["row1"] = pm.rowLayout( numberOfColumns=2 )
            aw( 'rowText1', pm.Text('Multiplier:', parent=row1)  )
            aw( 'multiplierFloatField', pm.floatField(value=initialMultiplier, parent=row1,
                    annotation="This will mutiply with both spacing and whole size \n " +
                        "to determine the final amount used. \n \n"+
                        self.annotationAboutInteraction,
                    changeCommand= lambda x: self.onChangedField(),
                    enterCommand= lambda x: self.onChangedField(),
                )
            )
            pm.setParent( priorParent )  
            
            row2 = self.widgets["row2"] = pm.rowLayout( numberOfColumns=2 )
            aw( 'rowText2', pm.Text('Spacing:', parent=row2)  )
            aw( 'spacingFloatField', pm.floatField(value=initialSpacing, parent=row2,
                    annotation="This will control grid point spacing,\n "+
                        "and will multiply with multiplier\n "+
                        "to determine the final amount used. \n \n"+
                        self.annotationAboutInteraction,
                    changeCommand= lambda x: self.onChangedField(),
                    enterCommand= lambda x: self.onChangedField(),
                )
            )
            pm.setParent( priorParent )  
            
            row3 = self.widgets["row3"] = pm.rowLayout( numberOfColumns=2 )            
            aw( 'rowText3', pm.Text('Whole:', parent=row3)  )
            aw( 'wholeSizeFloatField', pm.floatField(value=initialWholeSize, parent=row3,
                     annotation="This will control the extents of the whole grid,\n " +
                        "(width/height) and will multiply with multiplier \n "+
                        "to determine the final amount used. \n \n"+
                        "Note, Maya's grid width is like a radius, \n"+
                        "visible grid in Maya always looks twice as tall/wide, \n"+
                        "since the 'size' setting in Maya is distance from grid center, \n"+
                        "that's how Maya is intended to work. \n \n"+
                        self.annotationAboutInteraction,           
                    changeCommand= lambda x: self.onChangedField(),
                    enterCommand= lambda x: self.onChangedField(),
                )
            )
            pm.setParent( priorParent )
            
            row4 = self.widgets["row4"] = pm.rowLayout( numberOfColumns=2 )            
            aw( 'rowText4', pm.Text('Auto adjust discreet move:', parent=row4)  )
            aw( 'setManipCheckBox', pm.CheckBox(value=True, label=' ', parent=row4) )
                ## the checkbox has a built in label, but that shows on wrong side
            pm.setParent( priorParent )  
            
               
               
            aw('spacerBlankText', pm.Text(label='  '))

            aw('snapButton', pm.Button(label="Snap Selected Objs To Grid",
                command= lambda x: self.gtFuncs.putSelectedObjsOnGrid()  ) )
            aw('snapButton', pm.Button(label="Snap Selected Verts To Grid",
                command= lambda x: self.gtFuncs.snapVertsToGrid()  ) )
            aw('snapText', pm.Text(label='  '))
            
            aw('growButton', pm.Button(label="Grow",
                command= lambda x: self.growWithWarning(log=True)  ) )
            aw('shrinkButton', pm.Button(label="Shrink",
                command= lambda x: self.shrinkWithWarning(log=True)  ) )
            
                
        # Show Window
        if type( parentWidget ) == pm.core.windows.window:
            win = parentWidget
            pm.showWindow(win)
            win.setWidth(200)
            win.setHeight(300)
        
    
    
    def resetToMayaDefault(self):
        self.gtFuncs.reset(setManip=True)
        ## Maya default size is 5 with 5 divisions, results in one
        ## since this tool doesn't use divisions
        spacing = pm.grid( query=True, spacing=True ) / pm.grid( query=True, divisions=True )
        wholeSize = pm.grid( query=True, size=True )
        
        f = self.widgets['spacingFloatField']
        f.setValue(  spacing )
        f = self.widgets['multiplierFloatField']
        f.setValue(  1.0 )
        f = self.widgets['wholeSizeFloatField']
        f.setValue(  wholeSize )

    
    def getMultiplierFromUi(self):
        return self.widgets['multiplierFloatField'].getValue()
    
    def getSpacingFromUi(self):
        return self.widgets['spacingFloatField'].getValue()
    
    def getWholeSizeFromUi(self):
        return self.widgets['wholeSizeFloatField'].getValue()
    
    def getSetManipFromUi(self):
        return self.widgets['setManipCheckBox'].getValue()
    
    def growWithWarning(self, log=False):
        ## This grow function will increase total size if required.
        self.applyUiNumbers()
        
        ## Double the value of the UI field
        f = self.widgets['spacingFloatField']
        f.setValue(  2.0 * f.getValue()  )
        ## Double the actual grid spacing
        self.gtFuncs.grow(setManip=True,log=log)

        ## Check to make sure the spacing isn't too big
        ## if the grid spacing is too large, adjust the whole grid size to accomadate
        spacingOfActualGrid = pm.grid( query=True, spacing=True ) / pm.grid( query=True, divisions=True )
        wholeSizeOfActualGrid = pm.grid( query=True, size=True )
        multiplier=self.getMultiplierFromUi()
        w = self.widgets['wholeSizeFloatField']
        
        if spacingOfActualGrid>wholeSizeOfActualGrid:
            spacing = self.getSpacingFromUi()
            newWholeSizeNoMultiplier = spacing
            newWholeSizeWithMultiplier = newWholeSizeNoMultiplier * self.getMultiplierFromUi()
            pm.grid(    size=newWholeSizeWithMultiplier    )
            w.setValue( newWholeSizeNoMultiplier )
            
            
    def shrinkWithWarning(self, log=False):
        self.applyUiNumbers()
        ## Half the UI fields        
        f = self.widgets['spacingFloatField']
        f.setValue(  0.5 * f.getValue()  )    
        
        self.gtFuncs.shrink(setManip=True,log=log)
            
        ## Half the actual Maya size
        
    def onChangedField(self):
        self.applyUiNumbers()
        
    
    def applyUiNumbers(self):
            self.gtFuncs.reset_via_numbers(
                        multiplier=self.getMultiplierFromUi(),
                        spacing=self.getSpacingFromUi(),
                        wholeSize=self.getWholeSizeFromUi(),
                        setManip=self.getSetManipFromUi(),
            )

    
    def addWidget(self, name, widget):
        self.widgets[ name ] = widget
        return widget
 

## Register runTimeCommands so the user can make hotkeys for them 
T33d_GridTools_CmdPrefix=__name__
if T33d_GridTools_CmdPrefix == '__main__':
  #runtomeCmdNamePrefix = 
  T33d_GridTools_CmdPrefix = "T33d_GridToolsFuncs"
else:
  T33d_GridTools_CmdPrefix = T33d_GridTools_CmdPrefix + '.T33d_GridToolsFuncs'
runTimeCommands = {
    'T33d_GridTools_Grow' :
        T33d_GridTools_CmdPrefix+".grow(log=True)",
    'T33d_GridTools_Shrink' :
        T33d_GridTools_CmdPrefix+".shrink(log=True)",
    'T33d_GridTools_SnapObjsToGrid' :
        T33d_GridTools_CmdPrefix+".putSelectedObjsOnGrid()",
    'T33d_GridTools_SnapVertsToGrid' :
        T33d_GridTools_CmdPrefix+".snapVertsToGrid()",
  }
for k, v in runTimeCommands.items():
    if pm.runTimeCommand( k, q=1, exists=1 ):
        pm.runTimeCommand( k, e=1, command=v )
    else:
        pm.runTimeCommand( k, command=v )


def main():
    t33d_GridToolsUi = T33d_GridToolsUi()
    
if __name__=="__main__":
    main()

    
    
