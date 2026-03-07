"""
Hotstrings - A quick command launcher for Maya.

A modal dialog box where you type a short command (a "hotstring") and press
Enter.  Maya looks it up in the actions dictionary and runs the associated
MEL or Python code.  Escape cancels without doing anything.

The idea is to stack far more keyboard-driven interactivity than hotkeys alone
allow -- single letters or short strings can trigger any Maya operation.

Originally Written by Joe Crawford

--- DEFINING ACTIONS ---

T33D_Hotstrings_Actions maps a hotstring key to an action value.
The value can be any of these forms:

  A plain string
      Treated as MEL code.  The description shown in the HUD defaults to the
      hotstring key itself.

  A 1-tuple
      Same as a plain string: ("polyCube;",)

  A 2-tuple  (description, code)
      Code is run as MEL.
      ("Create Cube", "polyCube;")

  A 3-tuple  (description, language, code)
      Language is 'mel' or 'python' (case-insensitive; blank defaults to mel).
      ("Create Cube", "mel", "polyCube;")
      ("Center Pivot", "",   "CenterPivot;")   # blank = mel

"""

import traceback
import maya.cmds as cmds
import maya.mel


def onMayaDroppedPythonFile(*args, **kwargs):
    result = cmds.confirmDialog(
        title='Hotstrings',
        message='What would you like to do with Hotstrings?',
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
    buttonLabel = 'Hstr'

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
        annotation='Open Hotstrings command launcher',
        imageOverlayLabel='Hstr',
        image='pythonFamily.png',
    )


# ---------------------------------------------------------------------------
# Actions dictionary -- edit this to add your own hotstrings
# ---------------------------------------------------------------------------

T33D_Hotstrings_Actions = {
    'c':    ("Create Cube",          "",         "polyCube;"),
    's':    ("Create Sphere",        "",         "polySphere;"),
    'el':   ("Select Edge Loop",     "",         "SelectEdgeLoop;"),
    'er':   ("Select Edge Ring",     "",         "SelectEdgeRing;"),
    'tc':   ("Center Pivot",         "",         "CenterPivot;"),
    'help': ("Show Help",            "python",   "hs.showHelp()"),
}

## Load user-defined actions from a companion file if it exists.
## That file can add, remove, or replace entries by operating on 'actions',
## which is bound to T33D_Hotstrings_Actions for the duration of the exec.
## Any error (missing file, syntax error, etc.) is silently ignored so the
## built-in actions above are always available as a fallback.
##
## Search order (first match wins):
##   1. Maya's versioned user scripts folder  (e.g. .../maya/2025/scripts/)
##      -- takes priority so the user can keep their personal actions there
##         without touching the 1shot folder
##   2. The folder containing this script file
##      -- convenient when both files live together in the 1shots folder
try:
    import os as _os
    _actionsFilename = 't33d_1shot_hotstrings_actions.py'
    ## Build candidate list carefully so that a missing __file__ (e.g. when
    ## running as a shelf button) only skips that one entry rather than
    ## aborting the entire search.
    _candidatePaths = [_os.path.join(cmds.internalVar(userScriptDir=True), _actionsFilename)]
    try:
        _candidatePaths.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), _actionsFilename))
    except NameError:
        pass
    _actionsFile = next((p for p in _candidatePaths if _os.path.isfile(p)), None)
    if _actionsFile:
        with open(_actionsFile, 'r') as _f:
            ## Use the current globals as the exec namespace so the actions
            ## file has full context (cmds, maya, etc.), then inject 'actions'
            ## as the live reference to T33D_Hotstrings_Actions.
            _execNs = dict(globals())
            _execNs['actions'] = T33D_Hotstrings_Actions
            exec(compile(_f.read(), _actionsFile, 'exec'), _execNs)
except Exception:
    pass



# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

class T33d_HotstringsFuncs(object):

    def __init__(self):
        self.actions = T33D_Hotstrings_Actions

    def _normalizeAction(self, value):
        """Return (description, language, code) regardless of input form."""
        if isinstance(value, str):
            return (value, 'mel', value)
        value = tuple(value)
        if len(value) == 1:
            return (value[0], 'mel', value[0])
        if len(value) == 2:
            desc, code = value
            return (desc, 'mel', code)
        # 3-tuple (or longer -- we always take the last item as code)
        desc, lang, code = value[0], value[1], value[-1]
        lang = (lang or 'mel').strip().lower()
        if lang in ('p', 'py', 'python'):
            lang = 'python'
        else:
            lang = 'mel'
        return (desc, lang, code)

    def runAction(self, text):
        text = text.strip()
        if not text:
            return

        if text not in self.actions:
            cmds.inViewMessage(
                assistMessage='Hotstrings: unknown command <hl>{}</hl>  (type  help  to list all)'.format(text),
                pos='midCenter',
                fade=True
            )
            return

        desc, lang, code = self._normalizeAction(self.actions[text])

        try:
            if lang == 'python':
                # 'hs' exposes this instance so Python actions can call
                # methods like hs.showHelp()
                exec(code, {'cmds': cmds, 'maya': __import__('maya'), 'hs': self})
            else:
                maya.mel.eval(code)

            cmds.inViewMessage(
                assistMessage='Hotstrings: <hl>{}</hl>'.format(desc if desc else text),
                pos='midCenter',
                fade=True
            )
        except Exception:
            print(traceback.format_exc())
            cmds.inViewMessage(
                assistMessage='Hotstrings: error in <hl>{}</hl>  (see Script Editor)'.format(text),
                pos='midCenter',
                fade=True
            )

    def showHelp(self):
        print('')
        print('--- Hotstrings Commands ---')
        for key in sorted(self.actions.keys()):
            desc, lang, _ = self._normalizeAction(self.actions[key])
            print('  {:<12}  {}  [{}]'.format(key, desc, lang))
        print('---------------------------')
        print('')
        cmds.inViewMessage(
            assistMessage='Hotstrings: help printed to Script Editor',
            pos='midCenter',
            fade=True
        )


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

class T33d_HotstringsUi(object):

    def __init__(self):
        self.funcs = T33d_HotstringsFuncs()

        # cmds.promptDialog is a blocking modal dialog.
        # Pressing Enter (or clicking OK) returns 'OK'.
        # Pressing Escape (or clicking Cancel) returns the dismissString.
        result = cmds.promptDialog(
            title='Hotstrings',
            message='Enter command  (type  help  to list all):',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel'
        )

        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
            self.funcs.runAction(text)
        # Escape / Cancel: do nothing, dialog simply closes


## Register a runTimeCommand so the user can bind a hotkey to open the window.
_moduleName = __name__ if __name__ != '__main__' else 't33d_1shot_hotstrings'
runTimeCommands = {
    'T33d_Hotstrings_OpenUi':
        'import {m}; {m}.main()'.format(m=_moduleName),
}
for _k, _v in runTimeCommands.items():
    if cmds.runTimeCommand(_k, query=True, exists=True):
        cmds.runTimeCommand(_k, edit=True, command=_v, commandLanguage='python')
    else:
        cmds.runTimeCommand(_k, command=_v, commandLanguage='python')


def main():
    T33d_HotstringsUi()


if __name__ == '__main__':
    main()


