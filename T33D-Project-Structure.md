T33D Project Structure
===================================


Most detailed information about the T33D project itself is located in a dedicated folder:

./notes/T33D-the-Project-Itself

(relative to this repo's root)

The main file holding the information there is:

[[./notes/T33D-the-Project-Itself/T33D-the-Project-Itself.md]]


This File
===================================

This file the file in which this text exists is the main CLAUDE.md file for the T33D repo.

This file should be directly inside the T33D repo's root folder, root project folder for the actual version controlled repositoy for T33D. (As of 2026-03-03 the VCS used is Git, so this path is a git repository containing a .git subfolder.)





Paths On Filesystem
================================

Obviously, this T33D repo can be cloned or moved anyway. However, there is a standard working location normally being used for it, usually used on the Virtual Machine's T33D development work is done on.


Filesystem path On T33D's Main Development Virtual Machine
--------------------------------------------------------------

T:\t33d\t33d 

On the main virtual machine that is used to develop this project, this root folder is typically in the root of the drive T:\ on windows, which is actually a mapped drive that is really a UNC location in a windows file sharing shared folder.

T:\   <-  network share mapped to drive letter where we do T33D dev work, and some other things
T:\t33d\   <-  main folder for doing all t33d work, including files related to the project that won't go in the git repository

The mapped drive may have files/folders outside the t33d folders and unrelated to the t33d project. They can be ignored.



T33D Repo Folder
=================

This t33d project root folder is not the T33D repo. Rather, the project root folder is a private folder for work, not all of which will be put in the repo. The private project root is shared local-only, only available to certain core developers on certain machines.

A subfolder of the private project root is the repo, named "t33d". It's the actual git repository.

T:\t33d\t33d\  <-  the actual git repo, as seen on dev VMs.

If the repo has been cloned or moved then it won't be in the private project root. That's fine because almost everything inside the repo uses relative paths.



Project Structure - Code and Notes
=================

Code and notes are generally split up. Code of course does contain some notes in the code comments, and notes obviously do include some example code, but for the most part these are seperated.  Apps and tools are developed in the main T33D code folder, while notes serves as our knowledge base.


Code Folder, Relative to Repo root
=====

./code



Notes Folder, Relative to Repo root
======

./notes








Styles Conventions etc
================================

The files in this folder, and the CLAUDE.md file there, explain the convensions, writing and formating styles, etc, for this project, T33D.
T:\t33d\t33d\notes\T33D-the-Project-Itself\Conventions-Styles-Guidelines-and-Our-Reasoning-for-Them
