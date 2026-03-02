# Maya JupyterLab Kernel

Use JupyterLab as a Python console for Autodesk Maya 2025 (full GUI).
Cells in your notebook execute inside the live Maya session -- all scene state,
`maya.cmds`, `pymel`, and the full Maya Python API are available.

---

## How it works

Maya exposes a TCP server called `commandPort`.  This kernel uses it to send
code to Maya and receive results.  The tricky part: commandPort can give you
either the return value of a Python expression **or** stdout output, but not
both at once.  (And Maya 2025's echo-output mode is broken with a str/bytes
bug anyway.)

The fix is a small wrapper function (`_jupyter_exec`) installed inside Maya
that captures stdout internally and packs everything -- printed output,
expression results, and error tracebacks -- into a single JSON response.

---

## Requirements

- Autodesk Maya 2025 (full GUI, not standalone Python)
- Python with `ipykernel >= 6` and `jupyter-client >= 7` (outside Maya)
- JupyterLab

---

## Setup

### Step 1 -- Install the kernel package (outside Maya)

```bash
cd T:/t33d/t33d/code/maya/t33d_maya_and_jupyter_lab_connector
pip install -e .
```

Or, without installing, just make sure the connector folder is on your PYTHONPATH.

### Step 2 -- Register the kernel with Jupyter

```bash
python -m maya_jupyter.install
# or, if installed:
install-maya-kernel
```

Verify:
```bash
jupyter kernelspec list
# Should show:  maya_jupyter   /path/to/kernels/maya_jupyter
```

### Step 3 -- Start Maya and open the commandPort

In Maya's Script Editor → Python tab, run:

```python
exec(open(r"T:/t33d/t33d/code/maya/t33d_maya_and_jupyter_lab_connector/maya_jupyter/maya_init.py").read())
```

Note: `execfile()` was Python 2.  Maya 2025 is Python 3, so use `exec(open(...).read())`.

You should see:
```
[maya_jupyter] commandPort opened   : :7001
[maya_jupyter] _jupyter_exec ready  : __main__._jupyter_exec
[maya_jupyter] Waiting for Jupyter kernel connections...
```

To run this automatically every time Maya starts, add the `exec(open(...).read())` call
to your `userSetup.py`.

### Step 4 -- Use JupyterLab

```bash
jupyter lab
```

Create a new notebook and select **"Maya 2025"** as the kernel.

---

## Configuration

| Method | Variable | Default | Description |
|---|---|---|---|
| Env var | `MAYA_KERNEL_HOST` | `127.0.0.1` | Maya machine's IP (for remote Maya) |
| Env var | `MAYA_KERNEL_PORT` | `7001` | Must match `JUPYTER_PORT` in `maya_init.py` |
| Env var | `MAYA_KERNEL_TIMEOUT` | `30` | Seconds to wait for Maya response |
| CLI flag | `--MayaKernel.maya_port=7002` | -- | Alternative to env var |

Example -- connecting to Maya on a different port:
```bash
MAYA_KERNEL_PORT=7002 jupyter lab
```

### Multiple Maya instances

1. In each Maya, change `JUPYTER_PORT` at the top of `maya_init.py` before running it.
2. Run `install-maya-kernel` once per instance with custom names:
   ```python
   from maya_jupyter.install import install_kernel
   install_kernel(kernel_name='maya_7002', display_name='Maya 2025 (port 7002)')
   ```
3. Edit the installed `kernel.json` to add `--MayaKernel.maya_port=7002` to the argv.

---

## Usage notes

- **State persists between cells** -- variables, imports, and function
  definitions are all in Maya's `__main__` namespace and live as long as Maya
  does.

- **Print output and expression results both work** -- `print("hello")` shows
  output; `cmds.ls()` shows a result.  Note: a single-expression cell like
  `cmds.ls()` shows the return value; a multi-statement cell like
  `print("a"); 1+1` only shows the stdout -- the `1+1` result is not displayed
  because the whole cell goes through `exec` rather than `eval`.  Use `print()`
  for anything you want to see from a multi-statement cell.

- **Kernel restart = nothing** -- restarting the Jupyter kernel just starts a
  new kernel process.  Maya and its scene are unaffected.  Variables in Maya's
  namespace persist even through a kernel restart.

- **Long operations** -- increase `MAYA_KERNEL_TIMEOUT` for render-heavy cells.
  Maya's GUI will be unresponsive while a cell is running (that's normal; Maya
  is single-threaded for Python operations).

- **Ctrl-C does not interrupt Maya** -- there is no interrupt mechanism yet.
  If a cell is stuck, you'll need to wait for `recv_timeout` to expire or
  restart Maya.

---

## Troubleshooting

**"Connection refused"**
→ Maya is not running, or `maya_init.py` hasn't been run, or the port number
doesn't match.

**"Empty response from Maya"**
→ Maya is running and the port is open, but `_jupyter_exec` is not installed.
Re-run `maya_init.py` inside Maya.

**Cells hang forever**
→ The cell is running a blocking operation in Maya.  Wait, or kill Maya.
Increase `MAYA_KERNEL_TIMEOUT` to give it more time before the kernel gives up.

**"Could not parse Maya response as JSON"**
→ Something unexpected came back from the commandPort.  Check Maya's Script
Editor output window for errors.  Make sure `-echoOutput` is NOT set in the
`cmds.commandPort(...)` call.

---

## Files

```
t33d_maya_and_jupyter_lab_connector/
    README.md          ← this file
    CLAUDE.md          ← AI/agent context and extended technical notes
    pyproject.toml     ← package metadata
    maya_jupyter/
        __init__.py    ← package init
        maya_init.py   ← run inside Maya (commandPort + wrapper setup)
        kernel.py      ← Jupyter kernel process (runs outside Maya)
        install.py     ← registers kernel with Jupyter
```
