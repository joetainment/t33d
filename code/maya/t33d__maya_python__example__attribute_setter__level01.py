#### Attribute Setter Utility and User Interface
##The script allows you to quickly edit attributes on many objects at once.
##You can use r( minNumber, maxNumber ) to generate random values.
## You can also write other code and math.
## The i variable will give you the current iteration, which starts at zero and increases by one for each object.
import maya.cmds as cmds
#import pymel.all as pm
import math, random, traceback

## Short help msg shown at top of window
##   It's common (standard) to have "constant" variables,
##   that we don't intend to change while running
##   all together at the top of the script in ALL CAPS
BANNER=""" You can use python expressions.
Use "a" for the old attribute value,
and i for the object index.
So to double the values, you could use:    a * 2
To stack you could use:    a + i
To randomize from 20 to 30 could use:  random.uniform( 20.0, 30.0 )
"""

## This simple version will just use a bunch of global variables
## It's actually a bad way to do it, so a better version later
## will avoid so many global vars.
## This simple way with globals is easy to understand
## for beginner students thoug.


## This is the function that will actually
## create and show the UI window
def attributeSetterUiCreate():
    ## we have to tell python which variables should be global,
    ## made available outside this function, normally they should
    ## all be at the top, but to make it easier to follow,
    ## we'll actually declare them later when we make them
    #global win
    #global col
    #global banner
    #global attrNameLabel
    #global attrNameField
    #global attrValueLabel
    #global attrValueField
    #global setAttrButton
    

    global win
    win = 'T33d_AttributeSetterUi'
    if win in cmds.lsUI(windows=True):
        cmds.deleteUI( win )    
    win = cmds.window( win, title='T33d Attribute Setter' )
    ## store our win in our dict in case we want it elsewhere
    print( "Created UI:", win )
    
    ## A ColumnLayout - This will stack UI widgets vertically
    ##   adjustableColumn=True  means the widgets can auto adjust
    ##   their width to the window size
    global col
    col = cmds.columnLayout( adjustableColumn=True, parent=win )

    ## A banner msg we will show with some help
    ##    cmds.text just creates a text label
    global banner
    banner = cmds.text(BANNER, align="left")
    
    ## Text label that says "Attribute to change:"
    global attrNameLabel
    attrNameLabel = cmds.text(
        'Attribute to change:',
        align="left",
        parent=col
    )
        
    ## Text entry field,
    ## a place where the user will type in the attribute to change
    global attrNameField
    attrNameField = cmds.textField( parent=col   )

    ## Text label that says "New value for attribute:"
    global attrValueLabel
    attrValueLabel = cmds.text(
        'New value for attribute:',
        align="left",
        parent=col
    )
    
    ## Text entry field,
    ##   a place where the user will type the new value
    ##   to set the attribute to
    global attrValueField
    attrValueField = cmds.textField( parent=col )

    ## Finally, a button the user can click on to actually run the code!
    ##    even tho it's not strictly necessary,
    ##    it's usually a good idea to use lambda as below
    ##    to specify what command to run
    ##    otherwise you can't write parens for the func call
    ##    or put args in the parens... but with lambda you can!
    global setAttrButton
    setAttrButton = cmds.button(
        label="Set Attributes",
        align="left",
        parent=col,
        command=lambda x: setAttributes(  )
    )
    cmds.showWindow( win )



def setAttributes():
    print( "run!" )
    ## remember to declare our globals from the other function!
    global attrNameLabel
    global attrNameField
    global attrValueLabel
    global attrValueField
    
    ## this function doesn't actually use the next few globals,
    ##   so they don't have to be included
    #global win
    #global col
    #global banner
    #global btn

    ## we'll get a list of all selected objects
    objs = cmds.ls(selection=True,flatten=True)
    

    ## Now we'll Loop through the list, and try setting each
    ## object's attributes as requested
    for i, obj in enumerate(objs):
        ## We use a try block so that if one fails,
        ##   we just keep going to the next
        try:
            ## Get the attribute based on the attribute name in the UI
            attrName = cmds.textField( attrNameField, q=True, text=True )
            attrValueOld = cmds.getAttr( obj + '.' + attrName )
            a = attrValueOld
            ## Get the value from the UI
            attrValueNew = cmds.textField( attrValueField, q=True, text=True )
            ## eval it to convert convert the value from the UI
            ## into the target type, e.g. a floating point number
            attrValueNew = eval( attrValueNew )
            
            cmds.setAttr( obj + '.' + attrName,  attrValueNew  )
        except:
            print( traceback.format_exc()  )
            print(  'Failed for object: '  +  obj  )


if __name__=="__main__":
    attributeSetterUiCreate()
