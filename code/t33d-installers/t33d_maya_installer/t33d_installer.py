# t33d_installer.py
# Drag & drop into Maya viewport, or run directly with Python

import base64
import zipfile
import io
import os
import site
import sys
import subprocess

PAYLOAD_B64 = """
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
""".strip()

def _get_maya_scripts_dir():
    """Return the platform-appropriate Maya 2025 scripts folder path."""
    home = os.path.expanduser("~")
    if sys.platform == "win32":
        return os.path.join(home, "Documents", "maya", "2025", "scripts")
    elif sys.platform == "darwin":
        return os.path.join(home, "Library", "Preferences", "Autodesk", "maya", "2025", "scripts")
    else:
        return os.path.join(home, "maya", "2025", "scripts")


def _create_shortcut_windows(shortcut_path, target_path):
    """Create a Windows .lnk shortcut pointing to target_path."""
    ps = (
        f"$ws = New-Object -ComObject WScript.Shell; "
        f"$s = $ws.CreateShortcut('{shortcut_path}'); "
        f"$s.TargetPath = '{target_path}'; "
        f"$s.Save()"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        capture_output=True
    )


def _install_maya_extras(target_dir):
    """Place a README and (on Windows) a shortcut in the Maya scripts folder."""
    maya_scripts = _get_maya_scripts_dir()
    os.makedirs(maya_scripts, exist_ok=True)

    shortcut_note = (
        "A shortcut named 't33d_site-packages.lnk' in this folder points\n"
        "to the installed location for easy access.\n"
        if sys.platform == "win32" else ""
    )
    readme_text = (
        "t33d is installed in Maya's Python site-packages directory.\n\n"
        f"Installed location:\n"
        f"  {target_dir}\n\n"
        f"{shortcut_note}"
        "To uninstall t33d, delete the 't33d' folder and 't33d.pth' file\n"
        "from the installed location shown above.\n"
    )
    readme_path = os.path.join(maya_scripts, "t33d_installed_README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_text)
    print(f"[t33d] README written to: {readme_path}")

    if sys.platform == "win32":
        shortcut_path = os.path.join(maya_scripts, "t33d_site-packages.lnk")
        _create_shortcut_windows(shortcut_path, target_dir)
        print(f"[t33d] Shortcut created: {shortcut_path}")


def install():
    target_dir = site.USER_SITE
    os.makedirs(target_dir, exist_ok=True)

    zip_data = base64.b64decode(PAYLOAD_B64)

    with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
        zf.extractall(target_dir)

    print(f"[t33d] Installed to: {target_dir}")

    try:
        _install_maya_extras(target_dir)
    except Exception as e:
        print(f"[t33d] Warning: could not create Maya scripts extras: {e}")

    print(f"[t33d] Please restart Maya to complete installation.")

def _is_maya_python():
    try:
        import maya.utils
        return True
    except ImportError:
        return False

def _run():
    if not _is_maya_python():
        print("[t33d] This installer must be run inside Maya.")
        print("[t33d] To install: drag and drop this file into the Maya viewport.")
        return

    try:
        install()
    except Exception as e:
        print(f"[t33d] Installation failed: {e}")
        raise

# Maya drag & drop entry point
def onMayaDroppedPythonFile(*args, **kwargs):
    _run()

def _wait_for_keypress():
    try:
        import msvcrt
        print("\nPress any key to exit...")
        msvcrt.getch()
    except ImportError:
        input("\nPress Enter to exit...")

# Direct execution entry point
if __name__ == "__main__":
    _run()
    _wait_for_keypress()
