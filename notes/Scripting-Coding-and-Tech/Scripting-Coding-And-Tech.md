Scripting Coding And Tech
=========================


Notes on scripting tools, patterns, and workflows used in the t33d project.

Contents
--------

- [[python]] -- Python utilities and helpers
- [[mel]] -- Maya MEL scripting notes
- [[bash]] -- Shell scripts and automation

Overview
--------


This folder covers the scripting layer of the t33d pipeline. The focus is on tool scripts that run inside Maya, standalone CLI utilities, and automation that ties the two together.

Key themes:

- Keep scripts small and single-purpose
- Prefer Python over MEL for new work
- Document expected inputs/outputs in the file header

Related
-------

- [[pipeline]] -- Where scripts get wired into the broader workflow
- [[tools]] -- GUI wrappers around scripts