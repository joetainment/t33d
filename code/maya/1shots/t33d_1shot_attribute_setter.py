"""
AttributeSetterUi - A tool for quickly editing attributes
on many selected objects at once using Python expressions.

Originally Written by Joe Crawford

"""

import traceback
import maya.cmds as cmds
import maya.mel
import math
import random


def onMayaDroppedPythonFile(*args, **kwargs):
    result = cmds.confirmDialog(
        title='Attribute Setter',
        message='What would you like to do with Attribute Setter?',
        button=['Run', 'Run and Add to Shelf', 'Add to Shelf', 'Cancel'],
        defaultButton='Run',
        cancelButton='Cancel',
        dismissString='Cancel'
    )
    if result == 'Run':
        main()
    elif result == 'Run and Add to Shelf':
        main()
        _installToShelf()
    elif result == 'Add to Shelf':
        _installToShelf()


def _installToShelf():
    shelfName = 'T33d_1shots'
    buttonLabel = 'Attr Set'

    ## Get the top-level shelf tab bar and create our shelf if it doesn't exist
    shelfTopLevel = maya.mel.eval('$temp = $gShelfTopLevel')
    if not cmds.shelfLayout(shelfName, exists=True):
        cmds.shelfLayout(shelfName, parent=shelfTopLevel)

    ## Remove any existing button with the same label so we replace rather than duplicate
    existingButtons = cmds.shelfLayout(shelfName, query=True, childArray=True) or []
    for btn in existingButtons:
        if cmds.shelfButton(btn, query=True, exists=True):
            if cmds.shelfButton(btn, query=True, label=True) == buttonLabel:
                cmds.deleteUI(btn)

    ## Read this file's own source and use it directly as the command,
    ## so the shelf button is entirely self-contained with no external file dependency.
    filePath = __file__
    if filePath.endswith('.pyc'):
        filePath = filePath[:-1]
    with open(filePath, 'r') as f:
        cmd = f.read()

    cmds.shelfButton(
        parent=shelfName,
        label=buttonLabel,
        command=cmd,
        sourceType='python',
        annotation='Open Attribute Setter UI',
        imageOverlayLabel='Attr',
        image='pythonFamily.png',
    )


## Short help msg shown at top of window
BANNER = """ You can use python expressions.
Use "a" for the old attribute value,
and i for the object index.
So to double the values, you could use:    a * 2
To stack you could use:    a + i
To randomize from 20 to 30 could use:  random.uniform( 20.0, 30.0 )
"""


class T33d_AttributeSetterFuncs(object):

    _Instance = None

    @classmethod
    def GetInstance(cls):
        return cls._Instance

    @classmethod
    def setAttributes(cls, attrName, attrValueExpr, objs=None):
        """Set an attribute on all selected (or provided) objects using a Python expression."""
        if objs is None:
            objs = cmds.ls(selection=True, flatten=True)

        for i, obj in enumerate(objs):
            try:
                attrValueOld = cmds.getAttr(obj + '.' + attrName)
                a = attrValueOld
                attrValueNew = eval(attrValueExpr)
                cmds.setAttr(obj + '.' + attrName, attrValueNew)
            except:
                print(traceback.format_exc())
                print('Failed for object: ' + obj)


class T33d_AttributeSetterUi(object):

    _Instance = None

    @classmethod
    def GetInstance(cls):
        return cls._Instance

    def __init__(self):
        self.attrFuncs = T33d_AttributeSetterFuncs
        self.widgets = {}

        winName = 'T33d_AttributeSetterUi'
        if winName in cmds.lsUI(windows=True):
            cmds.deleteUI(winName)

        win = self.widgets['parentWidget'] = cmds.window(
            winName, title='T33d Attribute Setter', width=300, height=200
        )

        col = self.widgets['col'] = cmds.columnLayout(adjustableColumn=True, parent=win)

        self.widgets['bannerText'] = cmds.text(BANNER, align="left", parent=col)

        self.widgets['attrNameLabel'] = cmds.text(
            'Attribute to change:',
            align="left",
            parent=col
        )

        self.widgets['attrNameField'] = cmds.textField(parent=col)

        self.widgets['attrValueLabel'] = cmds.text(
            'New value for attribute:',
            align="left",
            parent=col
        )

        self.widgets['attrValueField'] = cmds.textField(parent=col)

        self.widgets['goButton'] = cmds.button(
            label="Set Attributes",
            align="left",
            parent=col,
            command=lambda x: self.onSetAttributes()
        )

        cmds.showWindow(win)
        cmds.window(win, edit=True, width=300, height=200)

    def onSetAttributes(self):
        attrName = cmds.textField(self.widgets['attrNameField'], query=True, text=True)
        attrValueExpr = cmds.textField(self.widgets['attrValueField'], query=True, text=True)
        self.attrFuncs.setAttributes(attrName, attrValueExpr)


## Register runTimeCommands so the user can make hotkeys for them
T33d_AttrSetter_CmdPrefix = __name__
if T33d_AttrSetter_CmdPrefix == '__main__':
    T33d_AttrSetter_CmdPrefix = "T33d_AttributeSetterFuncs"
else:
    T33d_AttrSetter_CmdPrefix = T33d_AttrSetter_CmdPrefix + '.T33d_AttributeSetterFuncs'

runTimeCommands = {
    'T33d_AttributeSetter_OpenUi':
        'import ' + (__name__ if __name__ != '__main__' else 't33d_1shot_attribute_setter') + '; '
        + (__name__ if __name__ != '__main__' else 't33d_1shot_attribute_setter') + '.main()',
}
for k, v in runTimeCommands.items():
    if cmds.runTimeCommand(k, query=True, exists=True):
        cmds.runTimeCommand(k, edit=True, command=v)
    else:
        cmds.runTimeCommand(k, command=v)


def main():
    t33d_AttributeSetterUi = T33d_AttributeSetterUi()


if __name__ == "__main__":
    main()
