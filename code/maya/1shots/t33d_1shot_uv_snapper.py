"""
UvSnapper - A tool for snapping UVs since snapping on
individual axes doesn't work for some people in Maya 2022.

Part of the T33d scripts package.

"""

import traceback
import maya.cmds as cmds
import maya.mel


def onMayaDroppedPythonFile(*args, **kwargs):
    result = cmds.confirmDialog(
        title='UV Snapper',
        message='What would you like to do with UV Snapper?',
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
    buttonLabel = 'UV Snap'

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
        annotation='Open UV Snapper UI',
        imageOverlayLabel='UVSnp',
        image='pythonFamily.png',
    )


class T33d_UvSnapperFuncs(object):

    _Instance = None
    _TargetLoc = None

    @classmethod
    def GetInstance(cls):
        return cls._Instance

    @classmethod
    def setTarget(cls):
        cls._TargetLoc, _ = cls.getManipFromUvs()
        print(cls._TargetLoc)

    @classmethod
    def _requireTarget(cls):
        if cls._TargetLoc is None:
            header = "\n\nWarning From T33d UV Snapper:\n    "
            msg = "Target must be set before snapping to it."
            print(header + msg)
            raise Exception(msg)

    @classmethod
    def snapU(cls):
        cls._requireTarget()
        cls.snapToTargetInU(cls._TargetLoc)

    @classmethod
    def snapV(cls):
        cls._requireTarget()
        cls.snapToTargetInV(cls._TargetLoc)

    @classmethod
    def snapUV(cls):
        cls._requireTarget()
        cls.snapToTargetInUAndV(cls._TargetLoc)

    @classmethod
    def getManipFromUvs(cls):
        sel = cmds.ls(sl=True)
        pivotObj = None
        for e in sel:
            if ".map" in e:
                pivotObj = e.split('.')[0]
                break  ## Only use first in selection;
                ## Maya's UI only tracks the uvPivot
                ## of the first selected uv/obj

        src = pivotObj + ".uvPivot"
        locations = cmds.getAttr(src)
        tLoc = locations[0]
        return tLoc, pivotObj

    @classmethod
    def calcDelta(cls, cLoc, tLoc):
        """Calcs delta (difference) from current to target."""
        return (tLoc[0] - cLoc[0], tLoc[1] - cLoc[1])

    @classmethod
    def snapToTargetInU(cls, targetLoc):
        cLoc, pivotObj = cls.getManipFromUvs()
        delta = cls.calcDelta(cLoc, targetLoc)
        deltaU = delta[0]
        cmds.polyEditUV(u=deltaU)
        cls._postFixForPivot(cLoc, pivotObj, deltaU, 0.0)

    @classmethod
    def snapToTargetInV(cls, targetLoc):
        cLoc, pivotObj = cls.getManipFromUvs()
        delta = cls.calcDelta(cLoc, targetLoc)
        deltaV = delta[1]
        cmds.polyEditUV(v=deltaV)
        cls._postFixForPivot(cLoc, pivotObj, 0.0, deltaV)

    @classmethod
    def snapToTargetInUAndV(cls, targetLoc):
        cLoc, pivotObj = cls.getManipFromUvs()
        delta = cls.calcDelta(cLoc, targetLoc)
        deltaU, deltaV = delta[0], delta[1]
        cmds.polyEditUV(u=deltaU, v=deltaV)
        cls._postFixForPivot(cLoc, pivotObj, deltaU, deltaV)

    @classmethod
    def _postFixForPivot(cls, cLoc, pivotObj, deltaU, deltaV):
        destLoc = (cLoc[0] + deltaU, cLoc[1] + deltaV)
        cmds.setAttr(
            pivotObj + ".uvPivot",
            destLoc[0], destLoc[1]
        )


class T33d_UvSnapperUi(object):

    _Instance = None

    @classmethod
    def GetInstance(cls):
        return cls._Instance

    def __init__(self):
        self.uvFuncs = T33d_UvSnapperFuncs
        self.widgets = {}

        winName = 'T33d_UvSnapperUi'
        if winName in cmds.lsUI(windows=True):
            cmds.deleteUI(winName)

        win = self.widgets['parentWidget'] = cmds.window(
            winName, title='T33d UV Snapper', width=200, height=150
        )

        col = self.widgets['col'] = cmds.columnLayout(adjustableColumn=True, parent=win)

        self.widgets['setTargetButton'] = cmds.button(
            label="Set Target",
            command=lambda x: self.setTarget(),
            parent=col
        )
        self.widgets['snapUButton'] = cmds.button(
            label="Snap To Target In U",
            command=lambda x: self.onSnapU(),
            parent=col
        )
        self.widgets['snapVButton'] = cmds.button(
            label="Snap To Target In V",
            command=lambda x: self.onSnapV(),
            parent=col
        )
        self.widgets['snapUVButton'] = cmds.button(
            label="Snap To Target In Both U and V",
            command=lambda x: self.onSnapUV(),
            parent=col
        )

        cmds.showWindow(win)
        cmds.window(win, edit=True, width=200, height=150)

    def setTarget(self):
        self.uvFuncs.setTarget()

    def onSnapU(self):
        self.uvFuncs.snapU()

    def onSnapV(self):
        self.uvFuncs.snapV()

    def onSnapUV(self):
        self.uvFuncs.snapUV()


## Register runTimeCommands so the user can make hotkeys for them
T33d_UvSnapper_CmdPrefix = __name__
if T33d_UvSnapper_CmdPrefix == '__main__':
    T33d_UvSnapper_CmdPrefix = "T33d_UvSnapperFuncs"
else:
    T33d_UvSnapper_CmdPrefix = T33d_UvSnapper_CmdPrefix + '.T33d_UvSnapperFuncs'

runTimeCommands = {
    'T33d_UvSnapper_OpenUi':
        'import ' + (__name__ if __name__ != '__main__' else 't33d_1shot_uv_snapper') + '; '
        + (__name__ if __name__ != '__main__' else 't33d_1shot_uv_snapper') + '.main()',
    'T33d_UvSnapper_SetTarget':
        T33d_UvSnapper_CmdPrefix + ".setTarget()",
    'T33d_UvSnapper_SnapU':
        T33d_UvSnapper_CmdPrefix + ".snapU()",
    'T33d_UvSnapper_SnapV':
        T33d_UvSnapper_CmdPrefix + ".snapV()",
    'T33d_UvSnapper_SnapUV':
        T33d_UvSnapper_CmdPrefix + ".snapUV()",
}
for k, v in runTimeCommands.items():
    if cmds.runTimeCommand(k, query=True, exists=True):
        cmds.runTimeCommand(k, edit=True, command=v)
    else:
        cmds.runTimeCommand(k, command=v)


def main():
    t33d_UvSnapperUi = T33d_UvSnapperUi()


if __name__ == "__main__":
    main()
