#!/usr/bin/env python3
# build_t33d_installer.py
# Combines t33d_installer_template.pytemplate + t33d_installer_contents.zip
# into a self-contained t33d_installer.py
#
# If t33d_installer_contents.dir/ exists, it is zipped first to produce
# t33d_installer_contents.zip (overwriting any existing zip).

import base64
import os
import sys
import zipfile

TEMPLATE_FILE  = "t33d_installer_template.pytemplate"
ZIP_FILE       = "t33d_installer_contents.zip"
DIR_SOURCE     = "t33d_installer_contents.dir"
OUTPUT_FILE    = "t33d_installer.py"
PLACEHOLDER    = "%%PAYLOAD_B64%%"


def build_zip_from_dir(dir_path, zip_path):
    """Zip all contents of dir_path into zip_path (files/folders go at zip root)."""
    print(f"[build] Building zip from: {dir_path}")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                abs_path = os.path.join(root, file)
                # arcname is relative to dir_path so contents land at zip root
                arcname = os.path.relpath(abs_path, dir_path)
                zf.write(abs_path, arcname)
    print(f"[build] Zip written:  {zip_path}  ({os.path.getsize(zip_path):,} bytes)")


def build():
    # Resolve paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))

    template_path = os.path.join(script_dir, TEMPLATE_FILE)
    zip_path      = os.path.join(script_dir, ZIP_FILE)
    dir_path      = os.path.join(script_dir, DIR_SOURCE)
    output_path   = os.path.join(script_dir, OUTPUT_FILE)

    # If the .dir source folder exists, rebuild the zip from it first
    if os.path.isdir(dir_path):
        build_zip_from_dir(dir_path, zip_path)

    # Validate inputs
    for path, name in [(template_path, TEMPLATE_FILE), (zip_path, ZIP_FILE)]:
        if not os.path.exists(path):
            print(f"[build] ERROR: Could not find {name} at: {path}")
            sys.exit(1)

    # Read and encode the zip
    with open(zip_path, "rb") as f:
        payload = base64.b64encode(f.read()).decode("utf-8")

    # Read the template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Check placeholder exists
    if PLACEHOLDER not in template:
        print(f"[build] ERROR: Placeholder '{PLACEHOLDER}' not found in template.")
        sys.exit(1)

    # Substitute
    output = template.replace(PLACEHOLDER, payload)

    # Write installer
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    zip_size = os.path.getsize(zip_path)
    out_size = os.path.getsize(output_path)
    print(f"[build] Zip:      {zip_path}  ({zip_size:,} bytes)")
    print(f"[build] Output:   {output_path}  ({out_size:,} bytes)")
    print(f"[build] Done. {OUTPUT_FILE} is ready.")

if __name__ == "__main__":
    build()
