"""
maya_jupyter/install.py
=======================
Register the Maya Jupyter kernel spec with Jupyter so it appears in
JupyterLab's kernel picker as "Maya 2025".

Run once after setting up this package:

    python -m maya_jupyter.install

Or equivalently (if the package has an entry point configured):

    install-maya-kernel

What this script does
---------------------
Jupyter discovers kernels by reading "kernel spec" directories, each of
which contains at minimum a ``kernel.json`` file.  That JSON tells Jupyter:

  - What command to run to start the kernel process.
  - What language the kernel speaks.
  - What display name to show in the UI.

We generate ``kernel.json`` dynamically at install time (rather than
shipping a static one) so that ``argv[0]`` is always the full path to the
CURRENT Python executable.  This matters inside virtual environments where
``python`` might not be on PATH, or might refer to the wrong interpreter.

The generated kernel.json looks like:
{
  "argv": [
    "/path/to/python",
    "-m", "maya_jupyter.kernel",
    "-f", "{connection_file}"
  ],
  "display_name": "Maya 2025",
  "language": "python"
}

For this to work, the Python at argv[0] must be able to import
``maya_jupyter``.  If you installed with ``pip install -e .`` (editable
install), this is automatic.  If you're running the scripts directly without
installing, ensure the parent directory of ``maya_jupyter/`` is on PYTHONPATH.

Multiple Maya instances
-----------------------
If you need to connect to several Maya instances simultaneously, run
install_kernel() multiple times with different ``kernel_name`` and
``display_name`` arguments, and pass a different ``--MayaKernel.maya_port``
in each kernel's argv list.
"""

import json
import sys
import tempfile
from pathlib import Path

# The internal Jupyter kernel identifier (no spaces; used in directory names
# and as the kernel name in notebook metadata).
DEFAULT_KERNEL_NAME    = 'maya_jupyter'
DEFAULT_DISPLAY_NAME   = 'Maya 2025'


def install_kernel(
    kernel_name:  str  = DEFAULT_KERNEL_NAME,
    display_name: str  = DEFAULT_DISPLAY_NAME,
    user:         bool = True,
    prefix:       str  = None,
) -> str:
    """
    Install the Maya Jupyter kernel spec.

    Parameters
    ----------
    kernel_name : str
        Internal Jupyter identifier for the kernel.  Must not contain spaces.
        Appears in ``jupyter kernelspec list`` output and in notebook metadata.
    display_name : str
        Human-readable name shown in JupyterLab's kernel picker.
    user : bool
        If True (default), install into the current user's Jupyter data
        directory (~/.local/share/jupyter on Linux/macOS,
        %APPDATA%/jupyter on Windows).
        If False and prefix is None, install system-wide (requires root/admin).
    prefix : str or None
        If provided, install into ``<prefix>/share/jupyter/kernels/``.
        Useful for virtual environments.  Overrides ``user``.

    Returns
    -------
    str
        Path to the installed kernel spec directory.
    """
    from jupyter_client.kernelspec import KernelSpecManager

    # Build kernel.json using the current Python executable so that the kernel
    # process is guaranteed to run in the same environment as this script.
    kernel_json = {
        'argv': [
            sys.executable,            # full path — works in venvs
            '-m', 'maya_jupyter.kernel',
            '-f', '{connection_file}', # placeholder filled by Jupyter at launch
        ],
        'display_name': display_name,
        'language':     'python',

        # 'interrupt_mode': 'message'
        # Uncomment the line above when interrupt (Ctrl-C) handling is
        # implemented.  'message' uses the ZMQ interrupt_request protocol
        # instead of OS signals, which is safer on Windows and avoids
        # accidentally killing Maya.
    }

    # Write the spec into a temporary directory and let KernelSpecManager
    # copy it into the appropriate Jupyter data path.
    with tempfile.TemporaryDirectory() as tmp_dir:
        spec_dir = Path(tmp_dir) / kernel_name
        spec_dir.mkdir()
        (spec_dir / 'kernel.json').write_text(
            json.dumps(kernel_json, indent=2),
            encoding='utf-8',
        )

        ksm = KernelSpecManager()
        install_kwargs = {
            'kernel_name': kernel_name,
            'replace':     True,
        }
        if prefix:
            install_kwargs['prefix'] = prefix
            install_kwargs['user']   = False
        else:
            install_kwargs['user']   = user

        dest = ksm.install_kernel_spec(str(spec_dir), **install_kwargs)

    return dest


def main():
    """Command-line entry point: ``python -m maya_jupyter.install``"""
    dest = install_kernel()
    print(f'[maya_jupyter] Kernel spec installed to:')
    print(f'               {dest}')
    print()
    print(f'[maya_jupyter] Next steps:')
    print(f'  1. In Maya\'s Script Editor (Python tab), run:')
    print(f'       execfile(r"<path_to_maya_init.py>")')
    print(f'  2. Launch JupyterLab:  jupyter lab')
    print(f'  3. Create a new notebook and select the "Maya 2025" kernel.')
    print()
    print(f'[maya_jupyter] Verify installation with:')
    print(f'       jupyter kernelspec list')


if __name__ == '__main__':
    main()
