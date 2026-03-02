## This will automatically run the build script in this folder
## then will use the mayapy.exe shortcut to run the script
## then will use the maya.exe shortcut to start maya

#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


# ── Executable discovery ───────────────────────────────────────────────────────

def _resolve_lnk_windows(lnk_path):
    """Resolve a Windows .lnk shortcut to its target path via PowerShell."""
    ps = f"(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk_path}').TargetPath"
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        capture_output=True, text=True
    )
    return result.stdout.strip() or None


def find_executables():
    """
    Returns (maya_exe, mayapy_exe) as strings.

    Windows: resolves .lnk shortcuts found in the same folder as this script.
    Other:   looks for 'maya' and 'mayapy' on PATH.
    """
    if sys.platform == "win32":
        maya_exe = mayapy_exe = None
        for lnk in SCRIPT_DIR.glob("*.lnk"):
            target = _resolve_lnk_windows(lnk)
            if not target:
                continue
            stem = Path(target).name.lower()
            if stem == "maya.exe":
                maya_exe = target
            elif stem == "mayapy.exe":
                mayapy_exe = target
        return maya_exe, mayapy_exe

    else:
        import shutil
        return shutil.which("maya"), shutil.which("mayapy")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _abort(msg):
    print(f"\n[t33d] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def _run(cmd, **kwargs):
    """Run a command; abort on non-zero exit."""
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        _abort(f"Command failed (exit {result.returncode}): {' '.join(str(c) for c in cmd)}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():

    # Step 1 — Build (zip from .dir + generate t33d_installer.py)
    print("[t33d] Building...")
    _run([sys.executable, str(SCRIPT_DIR / "t33d_installer_builder.py")],
         cwd=str(SCRIPT_DIR))

    # Step 2 — Locate Maya executables
    maya_exe, mayapy_exe = find_executables()

    if sys.platform == "win32":
        if not maya_exe or not mayapy_exe:
            _abort(
                "Could not resolve maya.exe and/or mayapy.exe from shortcuts.\n"
                f"         Expected .lnk shortcuts in: {SCRIPT_DIR}\n"
                "         Please add shortcuts to maya.exe and mayapy.exe there."
            )
    else:
        missing = [name for name, path in [("maya", maya_exe), ("mayapy", mayapy_exe)] if not path]
        if missing:
            _abort(
                f"Could not find {', '.join(missing)} on PATH.\n"
                "         Please ensure Maya's bin directory is included on PATH."
            )

    print(f"[t33d] maya:   {maya_exe}")
    print(f"[t33d] mayapy: {mayapy_exe}")

    # Step 3 — Install via mayapy
    # Call install() directly rather than _run(), which has an interactive Maya
    # guard that's appropriate for drag-and-drop use but not scripted installs.
    # Running under mayapy ensures site.USER_SITE resolves to Maya's location.
    installer = SCRIPT_DIR / "t33d_installer.py"
    print("[t33d] Installing...")
    install_cmd = (
        f"import importlib.util; "
        f"spec = importlib.util.spec_from_file_location('t33d_installer', r'{installer}'); "
        f"mod = importlib.util.module_from_spec(spec); "
        f"spec.loader.exec_module(mod); "
        f"mod.install()"
    )
    _run([mayapy_exe, "-c", install_cmd])

    # Step 4 — Launch Maya (detached; we don't wait for it)
    print("[t33d] Launching Maya...")
    subprocess.Popen([maya_exe])
    print("[t33d] Done.")


if __name__ == "__main__":
    main()
