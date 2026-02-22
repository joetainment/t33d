"""
HotkeysSwitchToPrevious - Switch to the previous hotkey set alphabetically.

Originally Written by Joe Crawford

"""

import maya.cmds as cmds
import maya.mel


def onMayaDroppedPythonFile(*args, **kwargs):
    result = cmds.confirmDialog(
        title='Hotkeys Switch To Previous',
        message='What would you like to do with Hotkeys Switch To Previous?',
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
    buttonLabel = 'HkPrv'

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
        annotation='Switch to previous hotkey set',
        imageOverlayLabel='HkPrv',
        image='pythonFamily.png',
    )


def main():
    sets = sorted(cmds.hotkeySet(query=True, hotkeySetArray=True) or [])
    if not sets:
        return
    current = cmds.hotkeySet(query=True, current=True)
    if current in sets:
        prevIdx = (sets.index(current) - 1) % len(sets)
    else:
        prevIdx = len(sets) - 1
    newSet = sets[prevIdx]
    cmds.hotkeySet(newSet, edit=True, current=True)
    cmds.inViewMessage(
        assistMessage='Hotkeys activated: <hl>{}</hl>'.format(newSet),
        pos='midCenter',
        fade=True
    )


if __name__ == "__main__":
    main()
