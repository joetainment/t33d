CLAUDE.md - The Claude File In The T33D Repo's root
=====================================================

Whenever Claude code is used with this repo, it should start by reading all the CLAUDE.md filesin the T33D repo. Not just in this folder, but in it's subfolders as well.

Those CLAUDE.md files should make it obvious which other files Claude needs to use to understand the projects organization/convensions/etc.



This File
=============

This file, the file in which this text exists, is the main CLAUDE.md file for the T33D repo, which relative to the repo, should be:

./CLAUDE.md



T33D Project structure
==========================

Beyond the CLAUDE files themselves, Claude should also read about the project structure in the

  [[T33D-Project-Structure]]

  Repo relative url:
  [T33D Project Structure](./T33D-Project-Structure)
  


Claude Work Logs Should Be Saved In This Project
=================================================  
  
When starting work, claude should start a new log file, named with the date and time (relative to the repo root):

claude-logs.gitIgnoreThis/claude-YYYY-MM-DDTHHNNSS.log


Claude should append to the log file quick short summaries of its tasks, and actions accomplished or failed.

Each entry should be timestampped and include which host machine ran it.

If possible Claude should include relative links as to where related memories can be found in the host machines machine-local memory locations, rather than duplicating too much of the memory in the claude-log files. If linking to paths of machine local memories can't be easily done, it's okay if doesn't get done.






