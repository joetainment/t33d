## If you are trying to help with t33d and work on devloping i
##   you should probably talk to Joe. Especially if you're a beginner student,
##   you may not want to worry about any of this git stuff!
##

## t33d git dev cmds help
##   It is generally assumed for this project developers are using
##   something like bash, and are in a unix like environment
##   git usage in gereral is most straightforward in unix like envs
## 
##   if you are on windows, either cygwin or wsl can be used
##
##   other tools, (e.g. windows native tools) can of course work
##   but this help won't cover them





## Git commit bash commands, to be used by user directly in control of git repo...



## Most of the time:
##   git changes, commits and pushes should be done as seperate commands.
##   To avoid typing too much, consider using aliases for the commands.
##
## Commands to put changes made into the actual repo:
# git add -A
# (export t33dTmpGitCommitMsg="" ; git commit -m "$t33dTmpGitCommitMsg" )
# git push origin main




## Git commit, msg, push oneliner.  Be careful with this!
# teedTmpGitCommitMsg="" bash -c 'git add -A && git commit -m "$t33dTmpGitCommitMsg" && git push origin main'
##
##   So that you don't reuse the msg carelessly
##   be sure to execute the command first as a comment,
##   then use up arrow once to get commented line from history,
##   and delete the first chatacter so it isn't a comment anymore
##   and only then execute the uncommented comment.
##     becayse it still has a space before the command,
##     that uncommented version won't be saved to the history





## (it won't truly export because the export only happens in the subshell, due to parens
##
# (export FOO=bar; somecommand someargs | somecommand2)

#### THE BELOW WON'% WORK WITHOUT ADJUSTMENT, Sh3ll
## Other ways of using tmp vars for single lines
# FOO=bar bash -c 'somecommand someargs | somecommand2'
# 
# (export teedTmpGitCommitMsg="" ; git add -A && git commit -m "$t33dTmpGitCommitMsg" && git push origin main )
