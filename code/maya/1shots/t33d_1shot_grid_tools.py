"""
GridToolsUi - An example GUI tool for
working with configurable power-of-N grid sizes in Maya
(e.g. powers of 2 or powers of 10)

Originally Written by Joe Crawford

"""

import traceback
import maya.cmds as cmds
import maya.mel


def onMayaDroppedPythonFile( *args, **kwargs ):
    result = cmds.confirmDialog(
        title='Grid Tools',
        message='What would you like to do with Grid Tools?',
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
    buttonLabel = 'Grid Tools'

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
        annotation='Open Grid Tools UI',
        imageOverlayLabel='Grid',
        image='pythonFamily.png',
    )






class T33d_GridToolsFuncs(object):

    _Instance = None

    @classmethod
    def GetInstance(cls):
        return cls.__Instance

    @classmethod
    def reset(cls, setManip=False):
        cmds.grid(reset=True)
        if setManip == True:
            ## Reset grid is spacing of 5 with 5 divisions,
            ## ends up being just 1.0
            cls.setManipToSpacing(1.0)

    @classmethod
    def reset_via_numbers(cls, multiplier=1.0, spacing=1.0, wholeSize=4096, setManip=False):
        ## Reset, but remember, default grid size is wacky, based on 5.0
        cmds.grid(reset=True)
        ## now change it to be power of two friendly 1.0*multiplier
        ## also set divisions to one and size
        cmds.grid(
            size=wholeSize * multiplier,
            spacing=spacing * multiplier,
            divisions=1
        )
        if setManip == True:
            cls.setManipToSpacing(spacing * multiplier)

    @classmethod
    def getWholeSize(cls):
        """
        This function gets the size of the *entire* grid,
        not the spacing between grid lines.
        """
        return cmds.grid(query=True, size=True)

    @classmethod
    def setWholeSize(cls, wholeSize):
        """
        This function sets the size of the *entire* grid,
        not the spacing between grid lines.
        """
        cmds.grid(size=wholeSize)

    @classmethod
    def getSpacing(cls, log=False):
        sp = cmds.grid(query=True, spacing=True)
        if log:
            print("Grid spacing value is: " + str(sp))
        return sp

    @classmethod
    def getDivisions(cls, log=False):
        sp = cmds.grid(query=True, divisions=True)
        if sp < 1:  ## Just in case maya ever gives us a number lower than the logically smallest
            sp = 1
        if log:
            print("Grid spacing value is: " + str(sp))
        return sp

    @classmethod
    def setSpacing(cls, spacing, setManip=False, log=False):
        if log:
            print("Grid spacing value is: " + str(spacing))
        cmds.grid(spacing=spacing)
        if setManip:
            cls.setManipToSpacing(spacing)

    @classmethod
    def setManipToSpacing(cls, spacing):
        cmds.manipMoveContext('Move', edit=True, snapRelative=True, snapValue=spacing)

    @classmethod
    def grow(cls, setManip=False, log=False, exponent=2):
        spacing = cls.getSpacing(log=log)
        new_spacing = spacing * float(exponent)
        cls.setSpacing(new_spacing, setManip=setManip)
        if log:
            cls.showMsg("Grid size: " + str(cls.getSpacing()))

    @classmethod
    def showMsg(cls, msg):
        cmds.inViewMessage(statusMessage=msg, fade=True, fadeStayTime=300, fadeOutTime=1)

    @classmethod
    def shrink(cls, setManip=False, log=False, exponent=2):
        spacing = cls.getSpacing(log=log)
        new_spacing = spacing / float(exponent)
        cls.setSpacing(new_spacing, setManip=setManip)
        if log:
            cls.showMsg("Grid size: " + str(cls.getSpacing()))

    @classmethod
    def putSelectedVertsOnGrid(cls):
        cls.snapVertsToGrid()  ## basically just an alias of the function name

    @classmethod
    def snapVertsToGrid(cls):
        originalSelection = cmds.ls(selection=True, flatten=True)
        maya.mel.eval('ConvertSelectionToVertices;')
        selVerts = cmds.ls(selection=True, flatten=True)

        spacing = cls.getSpacing()
        divisions = cls.getDivisions()

        spacingOfDivisions = spacing / float(divisions)

        def onGrid(n, s):
            return (spacingOfDivisions * float(round(n / float(s))))

        for v in selVerts:
            if '.vtx[' in v:
                pos = cmds.pointPosition(v, world=True)
                x = onGrid(pos[0], spacingOfDivisions)
                y = onGrid(pos[1], spacingOfDivisions)
                z = onGrid(pos[2], spacingOfDivisions)
                cmds.xform(v, translation=[x, y, z], worldSpace=True)

        if originalSelection:
            cmds.select(originalSelection)
        else:
            cmds.select(clear=True)


    @classmethod
    def getGridSnappableSpacing(cls):
        snappableSpacing = cmds.grid(query=True, spacing=True) / cmds.grid(query=True, divisions=True)
        return snappableSpacing


    @classmethod
    def putSelectedObjsOnGrid(cls):
        ss = cls.getGridSnappableSpacing()
        cls.putSelectedObjsOnSnappableSpacing(ss)


    @classmethod
    def putSelectedObjsOnSnappableSpacing(cls, snappableSpacing):
        oSel = cmds.ls(selection=True)
        objs = oSel[:]
        for obj in objs:
            cls.putObjOnSnappableSpacing(obj, snappableSpacing)
        cmds.select(oSel)


    @classmethod
    def putObjsOnSnappableSpacing(cls, objs, snappableSpacing):
        oSel = cmds.ls(selection=True)
        for obj in objs:
            cls.putObjOnSnappableSpacing(obj, snappableSpacing)


    @classmethod
    def putObjOnSnappableSpacing(cls, obj, snappableSpacing):
        oSel = cmds.ls(selection=True)
        destinationObj = obj
        usedObj = obj

        cmds.select(destinationObj)
        t = cmds.xform(query=True, rotatePivot=True, worldSpace=True)
        vt = cls.onSnappableSpacingVec((t[0], t[1], t[2]), snappableSpacing)

        cmds.select(usedObj)
        cmds.move(vt[0], vt[1], vt[2], worldSpace=True, absolute=True, worldSpaceDistance=True)

        ## We compensate by getting the *object being moved*'s
        ## pivot
        t2 = cmds.xform(query=True, rotatePivot=True, worldSpace=True)
        vt2 = (t2[0], t2[1], t2[2])

        ## vExtra is the additional amount compensated
        vExtra = (vt[0] - vt2[0], vt[1] - vt2[1], vt[2] - vt2[2])

        vDest = (vt[0] + vExtra[0], vt[1] + vExtra[1], vt[2] + vExtra[2])

        vFinal = vDest

        cmds.move(vFinal[0], vFinal[1], vFinal[2], worldSpace=True, absolute=True, worldSpaceDistance=True)

        cmds.select(oSel)

    @classmethod
    def onSnappableSpacing(cls, n, snappableSpacing):
        return (snappableSpacing * float(round(n / float(snappableSpacing))))

    @classmethod
    def onSnappableSpacingVec(cls, v, snappableSpacing):
        x = cls.onSnappableSpacing(v[0], snappableSpacing)
        y = cls.onSnappableSpacing(v[1], snappableSpacing)
        z = cls.onSnappableSpacing(v[2], snappableSpacing)
        return (x, y, z)


class T33d_GridToolsUi(object):

    _Instance = None

    @classmethod
    def GetInstance(cls):
        return cls.__Instance

    def __init__(self):
        self.annotationAboutInteraction = (
            "The settings should also auto apply when you change them,\n " +
            "but due to a Maya bug, you may occasionally have to apply manually,\n " +
            "with the button."
        )
        self.gtFuncs = T33d_GridToolsFuncs

        initialMultiplier = 1.0

        initialSpacing = (
            (cmds.grid(query=True, spacing=True) / cmds.grid(query=True, divisions=True))
            /
            initialMultiplier
        )
        initialWholeSize = cmds.grid(query=True, size=True) / initialMultiplier
        self.widgets = {}

        win = self.widgets['parentWidget'] = cmds.window(
            title=" Grid Tools Ui", width=100, height=200
        )

        col = self.widgets['col'] = cmds.columnLayout(adjustableColumn=True, parent=win)

        self.widgets['mayaOptionsButton'] = cmds.button(
            label="Maya Grid Options...",
            command=lambda x: maya.mel.eval("GridOptions;"),
            parent=col
        )
        self.widgets['resetButton'] = cmds.button(
            label="Reset (To Maya Defaults)",
            command=lambda x: self.resetToMayaDefault(),
            parent=col
        )
        self.widgets['reset2Button'] = cmds.button(
            label="Apply These Settings",
            annotation=self.annotationAboutInteraction,
            command=lambda x: self.gtFuncs.reset_via_numbers(
                multiplier=self.getMultiplierFromUi(),
                spacing=self.getSpacingFromUi(),
                wholeSize=self.getWholeSizeFromUi(),
                setManip=True,
            ),
            parent=col
        )

        exponentRow = self.widgets['exponentRow'] = cmds.rowLayout(numberOfColumns=2, parent=col)
        self.widgets['exponentRowText'] = cmds.text(label='Exponent:', parent=exponentRow)
        self.widgets['exponentIntField'] = cmds.intField(
            value=10,
            minValue=2,
            parent=exponentRow,
            annotation=(
                "The base used by Grow and Shrink.\n" +
                "2  = powers of 2  (double / half each step)\n" +
                "10 = powers of 10 (10x / 0.1x each step)"
            ),
        )
        cmds.setParent(col)

        multiplierRow = self.widgets['multiplierRow'] = cmds.rowLayout(numberOfColumns=2, parent=col)
        self.widgets['multiplierRowText'] = cmds.text(label='Multiplier:', parent=multiplierRow)
        self.widgets['multiplierFloatField'] = cmds.floatField(
            value=initialMultiplier,
            parent=multiplierRow,
            annotation=(
                "This will mutiply with both spacing and whole size \n " +
                "to determine the final amount used. \n \n" +
                self.annotationAboutInteraction
            ),
            changeCommand=lambda x: self.onChangedField(),
            enterCommand=lambda x: self.onChangedField(),
        )
        cmds.setParent(col)

        spacingRow = self.widgets['spacingRow'] = cmds.rowLayout(numberOfColumns=2, parent=col)
        self.widgets['spacingRowText'] = cmds.text(label='Spacing:', parent=spacingRow)
        self.widgets['spacingFloatField'] = cmds.floatField(
            value=initialSpacing,
            parent=spacingRow,
            annotation=(
                "This will control grid point spacing,\n " +
                "and will multiply with multiplier\n " +
                "to determine the final amount used. \n \n" +
                self.annotationAboutInteraction
            ),
            changeCommand=lambda x: self.onChangedField(),
            enterCommand=lambda x: self.onChangedField(),
        )
        cmds.setParent(col)

        wholeSizeRow = self.widgets['wholeSizeRow'] = cmds.rowLayout(numberOfColumns=2, parent=col)
        self.widgets['wholeSizeRowText'] = cmds.text(label='Whole:', parent=wholeSizeRow)
        self.widgets['wholeSizeFloatField'] = cmds.floatField(
            value=initialWholeSize,
            parent=wholeSizeRow,
            annotation=(
                "This will control the extents of the whole grid,\n " +
                "(width/height) and will multiply with multiplier \n " +
                "to determine the final amount used. \n \n" +
                "Note, Maya's grid width is like a radius, \n" +
                "visible grid in Maya always looks twice as tall/wide, \n" +
                "since the 'size' setting in Maya is distance from grid center, \n" +
                "that's how Maya is intended to work. \n \n" +
                self.annotationAboutInteraction
            ),
            changeCommand=lambda x: self.onChangedField(),
            enterCommand=lambda x: self.onChangedField(),
        )
        cmds.setParent(col)

        setManipRow = self.widgets['setManipRow'] = cmds.rowLayout(numberOfColumns=2, parent=col)
        self.widgets['setManipRowText'] = cmds.text(label='Auto adjust discreet move:', parent=setManipRow)
        self.widgets['setManipCheckBox'] = cmds.checkBox(value=True, label=' ', parent=setManipRow)
            ## the checkbox has a built in label, but that shows on wrong side
        cmds.setParent(col)

        self.widgets['spacerBlankText'] = cmds.text(label='  ', parent=col)

        self.widgets['snapButton'] = cmds.button(
            label="Snap Selected Objs To Grid",
            command=lambda x: self.gtFuncs.putSelectedObjsOnGrid(),
            parent=col
        )
        self.widgets['snapButton'] = cmds.button(
            label="Snap Selected Verts To Grid",
            command=lambda x: self.gtFuncs.snapVertsToGrid(),
            parent=col
        )
        self.widgets['snapText'] = cmds.text(label='  ', parent=col)

        self.widgets['growButton'] = cmds.button(
            label="Grow",
            command=lambda x: self.growWithWarning(log=True),
            parent=col
        )
        self.widgets['shrinkButton'] = cmds.button(
            label="Shrink",
            command=lambda x: self.shrinkWithWarning(log=True),
            parent=col
        )

        # Show Window
        cmds.showWindow(win)
        cmds.window(win, edit=True, width=200, height=330)


    def resetToMayaDefault(self):
        self.gtFuncs.reset(setManip=True)
        ## Maya default size is 5 with 5 divisions, results in one
        ## since this tool doesn't use divisions
        spacing = cmds.grid(query=True, spacing=True) / cmds.grid(query=True, divisions=True)
        wholeSize = cmds.grid(query=True, size=True)

        cmds.floatField(self.widgets['spacingFloatField'], edit=True, value=spacing)
        cmds.floatField(self.widgets['multiplierFloatField'], edit=True, value=1.0)
        cmds.floatField(self.widgets['wholeSizeFloatField'], edit=True, value=wholeSize)


    def getMultiplierFromUi(self):
        return cmds.floatField(self.widgets['multiplierFloatField'], query=True, value=True)

    def getSpacingFromUi(self):
        return cmds.floatField(self.widgets['spacingFloatField'], query=True, value=True)

    def getWholeSizeFromUi(self):
        return cmds.floatField(self.widgets['wholeSizeFloatField'], query=True, value=True)

    def getSetManipFromUi(self):
        return cmds.checkBox(self.widgets['setManipCheckBox'], query=True, value=True)

    def getExponentFromUi(self):
        return cmds.intField(self.widgets['exponentIntField'], query=True, value=True)

    def growWithWarning(self, log=False):
        ## This grow function will increase total size if required.
        self.applyUiNumbers()

        exponent = self.getExponentFromUi()
        ## Scale the UI spacing field up by the exponent
        currentSpacing = cmds.floatField(self.widgets['spacingFloatField'], query=True, value=True)
        cmds.floatField(self.widgets['spacingFloatField'], edit=True, value=float(exponent) * currentSpacing)
        ## Scale the actual grid spacing by the exponent
        self.gtFuncs.grow(setManip=True, log=log, exponent=exponent)

        ## Check to make sure the spacing isn't too big
        ## if the grid spacing is too large, adjust the whole grid size to accomadate
        spacingOfActualGrid = cmds.grid(query=True, spacing=True) / cmds.grid(query=True, divisions=True)
        wholeSizeOfActualGrid = cmds.grid(query=True, size=True)
        multiplier = self.getMultiplierFromUi()

        if spacingOfActualGrid > wholeSizeOfActualGrid:
            spacing = self.getSpacingFromUi()
            newWholeSizeNoMultiplier = spacing
            newWholeSizeWithMultiplier = newWholeSizeNoMultiplier * self.getMultiplierFromUi()
            cmds.grid(size=newWholeSizeWithMultiplier)
            cmds.floatField(self.widgets['wholeSizeFloatField'], edit=True, value=newWholeSizeNoMultiplier)


    def shrinkWithWarning(self, log=False):
        self.applyUiNumbers()

        exponent = self.getExponentFromUi()
        ## Scale the UI spacing field down by the exponent
        currentSpacing = cmds.floatField(self.widgets['spacingFloatField'], query=True, value=True)
        cmds.floatField(self.widgets['spacingFloatField'], edit=True, value=currentSpacing / float(exponent))

        self.gtFuncs.shrink(setManip=True, log=log, exponent=exponent)

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
        self.widgets[name] = widget
        return widget


## Register runTimeCommands so the user can make hotkeys for them
T33d_GridTools_CmdPrefix = __name__
if T33d_GridTools_CmdPrefix == '__main__':
    T33d_GridTools_CmdPrefix = "T33d_GridToolsFuncs"
else:
    T33d_GridTools_CmdPrefix = T33d_GridTools_CmdPrefix + '.T33d_GridToolsFuncs'

runTimeCommands = {
    'T33d_GridTools_Grow':
        T33d_GridTools_CmdPrefix + ".grow(log=True)",
    'T33d_GridTools_Shrink':
        T33d_GridTools_CmdPrefix + ".shrink(log=True)",
    'T33d_GridTools_SnapObjsToGrid':
        T33d_GridTools_CmdPrefix + ".putSelectedObjsOnGrid()",
    'T33d_GridTools_SnapVertsToGrid':
        T33d_GridTools_CmdPrefix + ".snapVertsToGrid()",
}
for k, v in runTimeCommands.items():
    if cmds.runTimeCommand(k, query=True, exists=True):
        cmds.runTimeCommand(k, edit=True, command=v)
    else:
        cmds.runTimeCommand(k, command=v)


def main():
    t33d_GridToolsUi = T33d_GridToolsUi()

if __name__ == "__main__":
    main()
