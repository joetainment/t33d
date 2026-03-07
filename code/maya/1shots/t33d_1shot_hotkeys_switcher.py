"""
HotkeysSwitcher - Quickly switch between Maya hotkey sets.

Originally Written by Joe Crawford

"""

import maya.cmds as cmds
import maya.mel


def onMayaDroppedPythonFile(*args, **kwargs):
    result = cmds.confirmDialog(
        title='Hotkeys Switcher',
        message='What would you like to do with Hotkeys Switcher?',
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
    buttonLabel = 'HkySwtch'

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
        annotation='Open Hotkeys Switcher UI',
        imageOverlayLabel='Hky',
        image='pythonFamily.png',
    )


class T33d_HotkeysSwitcherFuncs(object):

    @staticmethod
    def getHotkeySets():
        """Return a sorted list of all defined hotkey sets."""
        sets = cmds.hotkeySet(query=True, hotkeySetArray=True) or []
        return sorted(sets)

    @staticmethod
    def getCurrentHotkeySet():
        """Return the name of the currently active hotkey set."""
        return cmds.hotkeySet(query=True, current=True)

    @staticmethod
    def setHotkeySet(name):
        """Activate the named hotkey set."""
        cmds.hotkeySet(name, edit=True, current=True)
        cmds.inViewMessage(
            assistMessage='Hotkeys activated: <hl>{}</hl>'.format(name),
            pos='midCenter',
            fade=True
        )


class T33d_HotkeysSwitcherUi(object):

    _Instance = None

    @classmethod
    def GetInstance(cls):
        return cls._Instance

    def __init__(self):
        self.funcs = T33d_HotkeysSwitcherFuncs
        self.widgets = {}

        winName = 'T33d_HotkeysSwitcherUi'
        if winName in cmds.lsUI(windows=True):
            cmds.deleteUI(winName)

        win = self.widgets['parentWidget'] = cmds.window(
            winName, title='T33d Hotkeys Switcher', width=260, height=110
        )

        col = self.widgets['col'] = cmds.columnLayout(adjustableColumn=True, parent=win)

        self.widgets['setLabel'] = cmds.text(
            'Hotkey Set:',
            align='left',
            parent=col
        )

        hotkeySets = self.funcs.getHotkeySets()
        currentSet = self.funcs.getCurrentHotkeySet()
        currentIndex = hotkeySets.index(currentSet) + 1 if currentSet in hotkeySets else 1

        self.widgets['dropdown'] = cmds.optionMenu(
            parent=col,
            changeCommand=lambda name: self.onDropdownChanged(name),
            annotation='Select a hotkey set to activate'
        )
        for s in hotkeySets:
            cmds.menuItem(label=s, parent=self.widgets['dropdown'])
        cmds.optionMenu(self.widgets['dropdown'], edit=True, select=currentIndex)

        self.widgets['nextButton'] = cmds.button(
            label='Next',
            parent=col,
            annotation='Switch to next hotkey set',
            command=lambda x: self.onNext()
        )

        self.widgets['prevButton'] = cmds.button(
            label='Previous',
            parent=col,
            annotation='Switch to previous hotkey set',
            command=lambda x: self.onPrevious()
        )

        cmds.showWindow(win)
        cmds.window(win, edit=True, width=260, height=110)

    def _getDropdownItems(self):
        return cmds.optionMenu(self.widgets['dropdown'], query=True, itemListLong=True) or []

    def _getDropdownLabels(self):
        items = self._getDropdownItems()
        return [cmds.menuItem(i, query=True, label=True) for i in items]

    def _getCurrentDropdownIndex(self):
        """Return 0-based index of the currently selected dropdown item."""
        return cmds.optionMenu(self.widgets['dropdown'], query=True, select=True) - 1

    def _selectDropdownByName(self, name):
        labels = self._getDropdownLabels()
        if name in labels:
            cmds.optionMenu(self.widgets['dropdown'], edit=True, select=labels.index(name) + 1)

    def onDropdownChanged(self, name):
        self.funcs.setHotkeySet(name)

    def onNext(self):
        labels = self._getDropdownLabels()
        if not labels:
            return
        idx = self._getCurrentDropdownIndex()
        nextIdx = (idx + 1) % len(labels)
        nextName = labels[nextIdx]
        self._selectDropdownByName(nextName)
        self.funcs.setHotkeySet(nextName)

    def onPrevious(self):
        labels = self._getDropdownLabels()
        if not labels:
            return
        idx = self._getCurrentDropdownIndex()
        prevIdx = (idx - 1) % len(labels)
        prevName = labels[prevIdx]
        self._selectDropdownByName(prevName)
        self.funcs.setHotkeySet(prevName)


def main():
    t33d_HotkeysSwitcherUi = T33d_HotkeysSwitcherUi()


if __name__ == "__main__":
    main()
