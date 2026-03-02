import os
import sys
import traceback
import importlib.abc

LOG_FILE = r"""T:\t33d\t33d\code\t33d-installers\t33d_maya_installer\output-of-t33d_on_import.log"""


def _log(msg):
    with open(LOG_FILE, mode="a", encoding="utf-8") as fh:
        fh.write(msg)


def _deferred_init():
    # Safe to use maya.cmds, OpenMaya, do UI work, etc. here
    print("t33d deferred load working!")

    # Maya can evict entries from sys.modules during its startup sequence.
    # We hold a hard reference to the module object (_this_module, captured at
    # import time) so we can put ourselves back even if the key was cleared.
    if __name__ in sys.modules:
        _log(f"[t33d] pid={os.getpid()} deferred_init: '{__name__}' already in sys.modules\n")
    else:
        sys.modules[__name__] = _this_module
        _log(f"[t33d] pid={os.getpid()} deferred_init: '{__name__}' was missing — re-registered\n")

    _log(f"[t33d] pid={os.getpid()} deferred_init ran OK\n")


def _schedule_deferred_init(maya_utils=None):
    """Call executeDeferred once maya.utils is fully loaded."""
    try:
        if maya_utils is None:
            maya_utils = sys.modules["maya.utils"]
        maya_utils.executeDeferred(_deferred_init)
        _log(f"[t33d] pid={os.getpid()} executeDeferred registered OK\n")
    except Exception:
        _log(f"[t33d] pid={os.getpid()} executeDeferred FAILED:\n{traceback.format_exc()}\n")


class _MayaReadyWatcher(importlib.abc.MetaPathFinder):
    """
    Non-invasive meta-path watcher. Always returns None — never touches loaders
    or interferes with any actual import.

    On every maya.* import attempt it checks whether maya.utils is now fully
    initialised (i.e. has executeDeferred). The moment it is, we schedule our
    deferred init and stop watching.
    """
    _scheduled = False

    def find_spec(self, fullname, path, target=None):
        if self._scheduled or not fullname.startswith("maya."):
            return None
        maya_utils = sys.modules.get("maya.utils")
        if maya_utils is not None and hasattr(maya_utils, "executeDeferred"):
            self._scheduled = True
            _log(f"[t33d] pid={os.getpid()} maya.utils ready (triggered by '{fullname}')\n")
            _schedule_deferred_init(maya_utils=maya_utils)
        return None  # never intercept; let the real import machinery handle it


# ── module init ───────────────────────────────────────────────────────────────

_log(f"[t33d] pid={os.getpid()} __init__ entered\n")

# Capture a hard reference to this module object now.
# Even if Maya later removes sys.modules['t33d'], this keeps the object alive
# so _deferred_init can put it back.
_this_module = sys.modules.get(__name__)

_maya_utils = sys.modules.get("maya.utils")
if _maya_utils is not None and hasattr(_maya_utils, "executeDeferred"):
    # Imported after Maya is fully up (e.g. manual import from Script Editor)
    _log(f"[t33d] pid={os.getpid()} maya.utils already loaded, scheduling direct\n")
    _schedule_deferred_init(maya_utils=_maya_utils)
else:
    # Normal case: imported early via .pth before Maya sets up its modules
    sys.meta_path.insert(0, _MayaReadyWatcher())
    _log(f"[t33d] pid={os.getpid()} _MayaReadyWatcher installed\n")
