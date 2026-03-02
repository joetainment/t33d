"""
TransformTools - Quick access to common transform and pivot operations.

A window full of buttons for freeze, bake-pivot, and center-pivot operations.
Each button has a bracketed single-key shortcut shown in its label.
Type the key in the shortcut field at the top of the window, or just click.

Originally Written by Joe Crawford

"""

import traceback
import maya.cmds as cmds
import maya.mel


def onMayaDroppedPythonFile(*args, **kwargs):
    result = cmds.confirmDialog(
        title='Transform Tools',
        message='What would you like to do with Transform Tools?',
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
    buttonLabel = 'XfmTool'

    shelfTopLevel = maya.mel.eval('$temp = $gShelfTopLevel')
    if not cmds.shelfLayout(shelfName, exists=True):
        cmds.shelfLayout(shelfName, parent=shelfTopLevel)

    existingButtons = cmds.shelfLayout(shelfName, query=True, childArray=True) or []
    for btn in existingButtons:
        if cmds.shelfButton(btn, query=True, exists=True):
            if cmds.shelfButton(btn, query=True, label=True) == buttonLabel:
                cmds.deleteUI(btn)

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
        annotation='Open Transform Tools',
        imageOverlayLabel='Xfm',
        image='pythonFamily.png',
    )


# ---------------------------------------------------------------------------
# Action definitions
# (id, shortcut_key, label, group, annotation)
# ---------------------------------------------------------------------------

_ACTIONS = [
    ('centerPivot',               'c', 'Center Pivot',                      'Pivot',
     'Center the pivot on the bounding box of selected objects'),

    ('freezeAll',                 'f', 'Freeze Transforms',                 'Freeze',
     'Freeze translate, rotate, and scale to zero (makeIdentity T+R+S)'),
    ('freezeTranslate',           't', 'Freeze Translation',                'Freeze',
     'Freeze translate only'),
    ('freezeRotate',              'r', 'Freeze Rotation',                   'Freeze',
     'Freeze rotate only'),
    ('freezeScale',               's', 'Freeze Scale',                      'Freeze',
     'Freeze scale only'),

    ('bakePivotPos',              'p', 'Bake Pivot Position',               'Bake Pivot',
     'Bake the custom pivot position back into the standard pivot'),
    ('bakePivotOri',              'o', 'Bake Pivot Orientation',            'Bake Pivot',
     'Bake the custom pivot orientation back into the standard pivot'),
    ('bakePivotBoth',             'b', 'Bake Pivot Pos + Ori',              'Bake Pivot',
     'Bake the custom pivot position and orientation'),

    ('freezeAllBakeBoth',         '1', 'Freeze All + Bake Pos+Ori',        'Combined',
     'Freeze all transforms (T, R, S), then bake pivot position and orientation'),
    ('freezeScaleBakeBoth',       '2', 'Freeze Scale + Bake Pos+Ori',      'Combined',
     'Freeze scale only, then bake pivot position and orientation'),
    ('centerFreezeScaleBakeBoth', '3', 'Center + Freeze Scale + Bake',     'Combined',
     'Center pivot, freeze scale, then bake pivot position and orientation'),
]


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

class T33d_TransformToolsFuncs(object):

    @staticmethod
    def centerPivot():
        cmds.xform(centerPivots=True)

    @staticmethod
    def freezeAll():
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)

    @staticmethod
    def freezeTranslate():
        cmds.makeIdentity(apply=True, t=True, r=False, s=False, n=False, pn=True)

    @staticmethod
    def freezeRotate():
        cmds.makeIdentity(apply=True, t=False, r=True, s=False, n=False, pn=True)

    @staticmethod
    def freezeScale():
        cmds.makeIdentity(apply=True, t=False, r=False, s=True, n=False, pn=True)

    @staticmethod
    def _bakePivot(position=True, orientation=True):
        ## performBakePivot is the stable Maya proc behind Modify > Bake Pivot.
        ## It reads two option variables to decide what to bake.
        ## We set them immediately before calling so the checkbox state
        ## in Maya's own option box doesn't interfere with our intent.
        cmds.optionVar(iv=('bakePivotTranslate', int(position)))
        cmds.optionVar(iv=('bakePivotRotate',    int(orientation)))
        maya.mel.eval('performBakePivot 0')

    @staticmethod
    def bakePivotPos():
        T33d_TransformToolsFuncs._bakePivot(position=True, orientation=False)

    @staticmethod
    def bakePivotOri():
        T33d_TransformToolsFuncs._bakePivot(position=False, orientation=True)

    @staticmethod
    def bakePivotBoth():
        T33d_TransformToolsFuncs._bakePivot(position=True, orientation=True)

    @staticmethod
    def freezeAllBakeBoth():
        cmds.undoInfo(openChunk=True, chunkName='freezeAllBakeBoth')
        try:
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
            T33d_TransformToolsFuncs._bakePivot(position=True, orientation=True)
        finally:
            cmds.undoInfo(closeChunk=True)

    @staticmethod
    def freezeScaleBakeBoth():
        cmds.undoInfo(openChunk=True, chunkName='freezeScaleBakeBoth')
        try:
            cmds.makeIdentity(apply=True, t=False, r=False, s=True, n=False, pn=True)
            T33d_TransformToolsFuncs._bakePivot(position=True, orientation=True)
        finally:
            cmds.undoInfo(closeChunk=True)

    @staticmethod
    def centerFreezeScaleBakeBoth():
        cmds.undoInfo(openChunk=True, chunkName='centerFreezeScaleBakeBoth')
        try:
            cmds.xform(centerPivots=True)
            cmds.makeIdentity(apply=True, t=False, r=False, s=True, n=False, pn=True)
            T33d_TransformToolsFuncs._bakePivot(position=True, orientation=True)
        finally:
            cmds.undoInfo(closeChunk=True)


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

class T33d_TransformToolsUi(object):

    _Instance = None

    @classmethod
    def GetInstance(cls):
        return cls._Instance

    def __init__(self):
        self.funcs = T33d_TransformToolsFuncs()
        self.widgets = {}
        self._clearingKeyCapture = False

        self._actionsByKey = {key: actionId for actionId, key, _, _, _ in _ACTIONS if key}

        winName = 'T33d_TransformToolsUi'
        if winName in cmds.lsUI(windows=True):
            cmds.deleteUI(winName)

        win = self.widgets['parentWidget'] = cmds.window(
            winName, title='T33d Transform Tools', width=300
        )

        mainCol = cmds.columnLayout(
            adjustableColumn=True, rowSpacing=2,
            columnOffset=('both', 6),
            parent=win
        )

        ## Keyboard shortcut capture.
        ## textChangedCommand fires on every keystroke in Maya 2020+.
        ## If it isn't available, buttons still work; keyboard shortcuts just won't.
        cmds.separator(parent=mainCol, style='none', height=4)
        cmds.text(
            label='Shortcut key (or click a button):',
            align='left', font='smallBoldLabelFont', parent=mainCol
        )
        self.widgets['keyCapture'] = cmds.textField(parent=mainCol, height=22)
        try:
            cmds.textField(
                self.widgets['keyCapture'], edit=True,
                textChangedCommand=lambda text, *a: self._onKeyTyped(text)
            )
        except Exception:
            pass

        self.widgets['closeOnUse'] = cmds.checkBox(
            parent=mainCol,
            label='Close this window on use  [x]',
            value=True,
        )

        ## Buttons, organised by group
        currentGroup = None
        for actionId, key, label, group, annotation in _ACTIONS:
            if group != currentGroup:
                currentGroup = group
                cmds.separator(parent=mainCol, style='in', height=12)
                cmds.text(label=group, align='left', font='smallBoldLabelFont', parent=mainCol)

            buttonLabel = '{}  [{}]'.format(label, key) if key else label
            cmds.button(
                parent=mainCol,
                label=buttonLabel,
                annotation=annotation,
                height=26,
                command=lambda x, aid=actionId: self._triggerAction(aid),
            )

        ## Footer
        cmds.separator(parent=mainCol, style='in', height=12)
        cmds.button(
            parent=mainCol,
            label='Cancel  [q]',
            annotation='Close this window without performing any action (q)',
            height=26,
            command=lambda x: self._cancel(),
        )
        cmds.separator(parent=mainCol, style='none', height=4)

        cmds.showWindow(win)
        cmds.setFocus(self.widgets['keyCapture'])

    def _cancel(self):
        winName = 'T33d_TransformToolsUi'
        if cmds.window(winName, exists=True):
            cmds.deleteUI(winName)

    def _toggleCloseOnUse(self):
        current = cmds.checkBox(self.widgets['closeOnUse'], query=True, value=True)
        cmds.checkBox(self.widgets['closeOnUse'], edit=True, value=not current)

    def _onKeyTyped(self, text):
        if self._clearingKeyCapture or not text:
            return
        key = text.strip()
        ## Clear immediately so the field is ready for the next keypress
        self._clearingKeyCapture = True
        cmds.textField(self.widgets['keyCapture'], edit=True, text='')
        self._clearingKeyCapture = False

        lowerKey = key.lower()
        if lowerKey == 'q':
            self._cancel()
        elif lowerKey == 'x':
            self._toggleCloseOnUse()
        else:
            actionId = self._actionsByKey.get(lowerKey)
            if actionId:
                self._triggerAction(actionId)

    def _triggerAction(self, actionId):
        label = next((lbl for aid, _, lbl, _, _ in _ACTIONS if aid == actionId), actionId)
        fn = getattr(self.funcs, actionId, None)
        if fn is None:
            return

        try:
            fn()
            cmds.inViewMessage(
                assistMessage='Transform Tools: <hl>{}</hl>'.format(label),
                pos='midCenter',
                fade=True
            )
        except Exception:
            print(traceback.format_exc())
            cmds.inViewMessage(
                assistMessage='Transform Tools: error in <hl>{}</hl>  (see Script Editor)'.format(label),
                pos='midCenter',
                fade=True
            )

        winName = 'T33d_TransformToolsUi'
        if cmds.window(winName, exists=True):
            if cmds.checkBox(self.widgets['closeOnUse'], query=True, value=True):
                cmds.deleteUI(winName)


## Register a runTimeCommand so the user can bind a hotkey to open this window.
_moduleName = __name__ if __name__ != '__main__' else 't33d_1shot_transform_tools'
runTimeCommands = {
    'T33d_TransformTools_OpenUi':
        'import {m}; {m}.main()'.format(m=_moduleName),
}
for _k, _v in runTimeCommands.items():
    if cmds.runTimeCommand(_k, query=True, exists=True):
        cmds.runTimeCommand(_k, edit=True, command=_v, commandLanguage='python')
    else:
        cmds.runTimeCommand(_k, command=_v, commandLanguage='python')


def main():
    T33d_TransformToolsUi()


if __name__ == '__main__':
    main()
