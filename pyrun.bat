@echo off
setlocal enabledelayedexpansion

set arg1=%1
set arg2=%2

set folder=python\ml\lab%arg1%\lab%arg1%_%arg2%.py

for %%I in (%folder%) do (
    set py_dir=%%~dpI
    cd /d "%%~dpI"
)

python "lab%arg1%_%arg2%.py"
