Git Ignore Strategies for End User Editable Folders in T33D
============================================================


Generally, we use code like below in .gitignore files for untracked directories that we want to exist when the repo is first cloned.

The strategy explained in the code comments below.


```

*
!.gitignore


## Why?
## ====================
##
## * ignores everything
## !.gitignore exempts itself so it gets tracked and cloned
##
## this way this folder exist when repo is cloned
## but changes to it won't get propagated
## deleting this .gitignore after cloning should be safe
## even if the user later uses git pull origin main
## the only potential problem would be if they edit
## the .gitignore file, but that's on them!

```