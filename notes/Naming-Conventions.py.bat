@echo off
REM    This line, is a comment, ignored in batch files when running the code
REM    because it starts with REM
REM
REM    The first line in this file, above,
REM    turns off the printout of the code being run itself
REM
REM    --------- actual program below --------------------------


REM Go to folder this batch file is in!
cd /d %~dp0


python .\Naming-Conventions.py


REM  Give the User some time to see the output, copy paste, etc
REM  Eventually close automatically in case the user forgets to close
timeout 55