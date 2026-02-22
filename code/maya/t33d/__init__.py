"""
This will be the main file for the integrated "not standalone" t33d Python module for Maya.

This module will use Maya2022 and require Python 3. Whereas some of the standalone scripts will work with both 2 and 3, this module won't bother trying to be compatible with version 2.

The other files, the standalone scripts can be used in small bundles of similarly prefixed named files, without depending on other files.

However, more advanced functionality can go in the actual module, and the modules must be used as a whole.
"""
import sys
selfMod = sys.modules[__name__]
# selfPkg =   ## the local sub package (might have deep dots)
# selfRootPkg =  ## the highest top level packages (no dots)

#get
