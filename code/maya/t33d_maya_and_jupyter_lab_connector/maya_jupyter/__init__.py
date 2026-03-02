"""
maya_jupyter
============
A two-component system for using JupyterLab as an interactive Python
console for Autodesk Maya 2025 (full GUI instance).

Components
----------
maya_init.py   -- Run ONCE inside Maya's Script Editor.  Opens the
                  commandPort TCP socket and installs the _jupyter_exec()
                  wrapper into Maya's __main__ namespace.

kernel.py      -- The Jupyter kernel process (runs OUTSIDE Maya).
                  Registered with Jupyter via install.py.
                  Translates Jupyter cell executions into commandPort
                  calls and relays output back to JupyterLab.

install.py     -- Registers the kernel spec with Jupyter so it appears
                  in the JupyterLab kernel picker.

Quick start
-----------
1. In Maya's Script Editor (Python tab) — note: execfile() is Python 2 only;
   Maya 2025 uses Python 3:
       exec(open(r"<path>\\maya_jupyter\\maya_init.py").read())

2. In a terminal (with this package on sys.path or installed):
       python -m maya_jupyter.install

3. Launch JupyterLab and select the "Maya 2025" kernel.
"""

__version__ = "0.1.0"

from .kernel import MayaKernel  # noqa: F401

__all__ = ["MayaKernel"]
