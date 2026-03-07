"""
remap_drive.py

Remaps the T: drive to \\<current_gateway>\t33d-share, persistently.
If the drive is already mapped (to any path), it is disconnected first.
No questions asked — just overrides whatever is there.

Requirements:
    pip install pywin32

Usage:
    python remap_drive.py                         # pops up a Tk window
    python remap_drive.py --drive T: --share t33d-share
    python remap_drive.py --drive T: --share t33d-share --dry-run
    python remap_drive.py --no-gui                # force CLI mode
"""

import argparse
import subprocess
import sys
import re

try:
    import win32wnet
    import win32netcon
    import pywintypes
except ImportError:
    sys.exit(
        "pywin32 is required. Install it with:  pip install pywin32\n"
        "Then run:  python Scripts/pywin32_postinstall.py -install"
    )


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def get_default_gateway() -> str:
    """Return the IPv4 address of the default gateway (first one found)."""
    output = subprocess.check_output(["ipconfig"], text=True, encoding="oem")
    for line in output.splitlines():
        if "Default Gateway" in line:
            match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", line)
            if match:
                ip = match.group(1)
                if not ip.startswith("0."):
                    return ip
    raise RuntimeError("Could not determine the default gateway from ipconfig output.")


def remap_drive(drive: str, remote: str, dry_run: bool = False) -> str:
    """
    Force-disconnect drive (if mapped) then reconnect to remote, persistently.
    Returns a human-readable status string.
    """
    drive = drive.rstrip("\\").upper()
    if not drive.endswith(":"):
        drive += ":"

    lines = [f"Drive  : {drive}", f"New UNC: {remote}"]

    if dry_run:
        lines.append("[DRY RUN] No changes made.")
        return "\n".join(lines)

    # Disconnect — ignore errors (drive may not be mapped at all)
    try:
        win32wnet.WNetCancelConnection2(drive, win32netcon.CONNECT_UPDATE_PROFILE, True)
        lines.append("Existing mapping removed.")
    except pywintypes.error:
        lines.append("No existing mapping found, continuing.")

    # Reconnect persistently
    nr = win32wnet.NETRESOURCE()
    nr.lpLocalName  = drive
    nr.lpRemoteName = remote
    nr.dwType       = win32netcon.RESOURCETYPE_DISK

    win32wnet.WNetAddConnection2(nr, None, None, win32netcon.CONNECT_UPDATE_PROFILE)
    lines.append(f"Mapped {drive} -> {remote}  (persists at logon)")

    return "\n".join(lines)


def do_remap(drive: str = "T:", share: str = "t33d-share", dry_run: bool = False) -> str:
    """Convenience wrapper: detect gateway, build UNC, remap. Returns status string."""
    gateway = get_default_gateway()
    remote  = f"\\\\{gateway}\\{share}"
    return remap_drive(drive, remote, dry_run=dry_run)


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

def run_gui(drive: str, share: str) -> None:
    """Show a minimal Tk window with a single Connect button."""
    import tkinter as tk
    from tkinter import messagebox

    root = tk.Tk()
    root.title("Map Network Drive")
    root.resizable(False, False)

    # ---- layout ----
    pad = {"padx": 20, "pady": 10}

    info_var = tk.StringVar(value=f"Drive:  {drive.upper().rstrip(chr(92))}:\nShare:  {share}")
    tk.Label(root, textvariable=info_var, justify="left", font=("Segoe UI", 10)).pack(**pad)

    status_var = tk.StringVar(value="Ready.")
    status_lbl = tk.Label(root, textvariable=status_var, justify="left",
                          font=("Segoe UI", 9), fg="gray")
    status_lbl.pack(padx=20, pady=(0, 5))

    btn = tk.Button(root, text="Connect Drive", width=20, height=2,
                    font=("Segoe UI", 10, "bold"))

    def on_connect():
        btn.config(state="disabled")
        status_var.set("Connecting …")
        root.update()
        try:
            result = do_remap(drive, share)
            status_var.set("Done.")
            status_lbl.config(fg="green")
            root.update()
            messagebox.showinfo("Success", result, parent=root)
        except Exception as exc:
            status_var.set("Failed.")
            status_lbl.config(fg="red")
            root.update()
            messagebox.showerror("Error", str(exc), parent=root)
        finally:
            root.destroy()

    btn.config(command=on_connect)
    btn.pack(padx=20, pady=(0, 20))

    root.mainloop()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_cli(drive: str, share: str, dry_run: bool) -> None:
    print("=== Network Drive Remapper ===\n")
    print("Detecting default gateway ...")
    result = do_remap(drive, share, dry_run=dry_run)
    print(result)
    print("\nDone.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Remap a network drive to use the current default gateway IP.\n\n"
            "When called with no arguments a Tk GUI window is shown.\n"
            "Pass any argument (e.g. --drive, --share, --no-gui) to use CLI mode."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--drive",   default="T:",         help="Drive letter to remap (default: T:)")
    parser.add_argument("--share",   default="t33d-share", help="Share name (default: t33d-share)")
    parser.add_argument("--dry-run", action="store_true",  help="Show what would happen without making changes")
    parser.add_argument("--no-gui",  action="store_true",  help="Force CLI mode even with no other arguments")
    args = parser.parse_args()

    # Use GUI only when the user supplied zero arguments
    use_gui = (len(sys.argv) == 1) and not args.no_gui

    if use_gui:
        try:
            run_gui(args.drive, args.share)
        except Exception as exc:
            print(f"GUI failed ({exc}), falling back to CLI help:\n")
            parser.print_help()
            sys.exit(1)
    else:
        run_cli(args.drive, args.share, args.dry_run)


if __name__ == "__main__":
    main()