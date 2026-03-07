
Importing Modules For Python In Maya
=========================================

In order for scripts to make use of any of nice functionality from inside Python, the Python script needs to import the correct modules first. Thus almost all scripts start their code with a bunch of import statements. (Pretty much all of our future examples will have similar import statements.)

Note:  Imports should usually come at the beginning of your scripts!


<pre>
## Standard common modules
import math, sys, random, traceback  ## standard python modules

## Standard Maya Modules
import maya
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om     ##  or for older Maya API (v1)  #import maya.OpenMaya as OmOld

## Pymel - If you want to and are allowed to use it. (Some pipelines avoid it.)
import pymel.all as pm


## Most scripts just use the following, so you can, as standard practice, just copy paste it to your scripts...
import math, sys, random, traceback
import maya.cmds as cmds
import maya.mel as mel

</pre

