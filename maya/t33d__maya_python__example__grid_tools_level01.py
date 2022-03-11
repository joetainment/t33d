"""
Grid Tools Example Level 01
A very simplified examples one with just the grow and shrink function.

This file can be placed in your Maya scripts folder
C:\Users\YourUserName\Documents\maya\maya2022\scripts

Usage
===============
To use:
import t33d__maya_python__example__grid_tools_level01
t33d__maya_python__example__grid_tools_level01.grow()

...or...
import t33d__maya_python__example__grid_tools_level01
t33d__maya_python__example__grid_tools_level01.shrink()


Usage As Hotkeys Shelf Buttons
================================
Hotkeys and shelf buttons will require that the module has been loaded.
so you should include the import line in them or their runtime commands!
"""

import maya.cmds as cmds

def grow():
    oldSpacing = cmds.grid( query=True, spacing=True )
    newSpacing = oldSpacing * 2    ## grow, make it double the size
    cmds.grid( spacing=newSpacing )

def shrink():
    import maya.cmds as cmds
    oldSpacing = cmds.grid( query=True, spacing=True )
    newSpacing = oldSpacing / 2.0    ## grow, make it double the size
    cmds.grid( spacing=newSpacing )

