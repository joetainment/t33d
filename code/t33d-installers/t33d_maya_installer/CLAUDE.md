# t33d Installer System

This folder contains a build system for generating a self-contained Python installer
for the t33d Maya package. The installer can be drag-and-dropped into Maya or run
directly from the command line.

---

## Files

| File | Purpose |
|------|---------|
| `build_t33d_installer.py` | Generator script -- combines template + zip into the final installer |
| `t33d_installer_template.pytemplate` | Installer source code with a placeholder for the zip payload |
| `t33d_installer_contents.zip` | The t33d package files to be installed (not committed if large) |
| `t33d_installer.py` | **Generated output** -- the self-contained installer, ready for distribution |

---

## How It Works

### The installer

`t33d_installer.py` is a single self-contained Python file. It carries the entire
t33d package embedded inside it as a base64-encoded zip file. When run, it:

1. Decodes the base64 payload back into zip data (in memory, no temp files)
2. Extracts the zip contents directly into Maya's user `site-packages` folder
   (`site.USER_SITE`)
3. Prints a message asking the user to restart Maya

### Maya drag & drop

Maya supports drag-and-dropping `.py` files into the viewport. When this happens,
Maya executes the file and looks for a function named exactly
`onMayaDroppedPythonFile`. The installer defines this function as its entry point,
so the install runs automatically on drop.

The installer also works when run directly with `python t33d_installer.py` outside
of Maya, via the standard `if __name__ == "__main__"` guard.

### Why site-packages?

Maya 2025 runs with `site.USER_SITE_ENABLED = True`, meaning Python's standard user
site-packages directory is active. This is a per-user folder that does not require
admin privileges to write to. Anything placed there is automatically available to
Maya's Python interpreter on startup.

### The .pth file and deferred loading

The zip contains two key files that land in `site-packages`:

- **`t33d.pth`** -- a Python path configuration file containing the single line:
  `import t33dLocal`
  Python's `site` module processes `.pth` files at interpreter startup. Normally
  `.pth` files add directories to `sys.path`, but any line beginning with `import`
  is executed directly as Python code. This is a standard CPython feature.

- **`t33dLocal.py`** -- the bootstrap module imported by `t33d.pth`. Because `.pth`
  files are processed very early in startup, Maya's API (`maya.cmds`, OpenMaya, etc.)
  is not yet available at this point. `t33dLocal.py` therefore does minimal work
  immediately and instead uses `maya.utils.executeDeferred()` to schedule the real
  initialisation to run once Maya is fully up.

  ```python
  # t33dLocal.py pattern
  import maya.utils

  def _deferred_init():
      import t33d
      t33d.initialize()

  maya.utils.executeDeferred(_deferred_init)
  ```

  `maya.utils` is available early enough to call at `.pth` processing time.
  If the import fails for any reason (module not found, exception, etc.), Python's
  `site` module silently swallows the error and Maya continues to start normally.

- **`t33d/`** -- the actual t33d package, also in `site-packages`, imported by the
  deferred call above.

---

## Building the Installer

Ensure the following files are in the same folder:

- `build_t33d_installer.py`
- `t33d_installer_template.pytemplate`
- `t33d_installer_contents.zip`

Then run:

```
python build_t33d_installer.py
```

This produces `t33d_installer.py` in the same folder.

### What the builder does

1. Reads `t33d_installer_contents.zip` and base64-encodes it
2. Reads the template and replaces the placeholder `%%PAYLOAD_B64%%` with the
   encoded payload
3. Writes the result to `t33d_installer.py`
4. Reports the file sizes of the zip and the generated installer

The builder will exit with a clear error message if either input file is missing
or if the placeholder is not found in the template.

---

## Updating the Package

To release a new version:

1. Update the contents of `t33d_installer_contents.zip` with the new package files
2. Run `python build_t33d_installer.py`
3. Distribute the newly generated `t33d_installer.py`

The template only needs to change if the installer logic itself changes.

---

## zip Contents Layout

The zip should extract with this structure so files land correctly in `site-packages`:

```
t33d.pth
t33dLocal.py
t33d/
    __init__.py
    ... (rest of package)
```
