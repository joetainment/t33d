#### Attribute Setter Utility and User Interface
##The script allows you to quickly edit attributes on many objects at once.
##You can use r( minNumber, maxNumber ) to generate random values.
## You can also write other code and math.
## The i variable will give you the current iteration, which starts at zero and increases by one for each object.
import maya.cmds as cmds
#import pymel.all as pm
import math, random, traceback

## Short help msg shown at top of window
BANNER=""" You can use python expressions.
Use "a" for the old attribute value,
and i for the object index.
So to double the values, you could use:    a * 2
To stack you could use:    a + i
To randomize from 20 to 30 could use:  random.uniform( 20.0, 30.0 )
"""

## We can wrap it all up as a class which is a common Python pattern.
class T33d_AttributeSetterUi(object):
    def __init__(self):
        self.win = 'T33d_AttributeSetterUi'
        if self.win in cmds.lsUI(windows=True):
            cmds.deleteUI( self.win )    
        self.win = cmds.window( self.win, title='T33d Attribute Setter' )
        print( "Created UI:", self.win )
        
        
        self.col = cmds.columnLayout( adjustableColumn=True, parent=self.win )
        self.text = cmds.text(BANNER, align="left")
        
        ## Text label that says "Attribute to change:"
        self.attrNameLabel = cmds.text(
            'Attribute to change:',
            align="left",
            parent=self.col
        )
        
        ## Text entry field, a place where the user will type in the attribute to change
        self.attrNameField = cmds.textField( parent=self.col   )

        ## Text label that says "New value for attribute:"
        self.attrValueLabel = cmds.text(
            'New value for attribute:',
            align="left",
            parent=self.col
        )
        
        ## Text entry field, a place where the user will type the new value to set the attribute to
        self.attrValueField = cmds.textField( parent=self.col )

        self.go = cmds.button(
          label="Set Attributes",
          align="left",
          parent=self.col,
          command=lambda x: self.setAttributes(  )
        )
        
        cmds.showWindow( self.win )

    def setAttributes(self):
        ## Get a list of all selected objects
        objs = cmds.ls(selection=True,flatten=True)
        
        ## Loop through the list, and try setting each object
        for i, obj in enumerate(objs):
            ## use a try block so that if it fails
            ## we just continue on to the next!
            try:
                ## Get the attribute based on the attribute name in the UI
                attrName = cmds.textField(
                    self.attrNameField,
                    q=True,
                    text=True
                )
                attrValueOld = cmds.getAttr( obj + '.' + attrName )
                a = attrValueOld
                ## Get the value from the UI
                attrValueNew = cmds.textField(
                    self.attrValueField,
                    q=True,
                    text=True
                )
                ## Eval it to convert convert the value from the UI
                ## into the target type, e.g. a floating point number
                attrValueNew = eval( attrValueNew )
                cmds.setAttr( obj + '.' + attrName,  attrValueNew  )
            except:
                print( traceback.format_exc()  )
                print(  'Failed for object: '  +  obj  )


if __name__=="__main__":
    T33d_AttributeSetterUi()
