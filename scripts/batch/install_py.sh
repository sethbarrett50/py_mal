@echo off
setlocal enabledelayedexpansion

set "PY_VERSION=3.14.0"

python --version 2>&1 | findstr /C:"Python 3.14" >nul 2>&1
if %errorlevel% == 0 goto :uv_install

if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set "PY_ARCH=amd64"
) else if "%PROCESSOR_ARCHITECTURE%"=="ARM64" (
    set "PY_ARCH=arm64"
) else (
    set "PY_ARCH=win32"
)

set "PY_EXE=python-%PY_VERSION%-%PY_ARCH%.exe"
set "PY_URL=https://www.python.org/ftp/python/%PY_VERSION%/%PY_EXE%"
set "TARGET=%temp%\%PY_EXE%"

net session >nul 2>&1
if %errorlevel% == 0 (
    set "FLAGS=/quiet InstallAllUsers=1 PrependPath=1 Include_test=0"
) else (
    set "FLAGS=/quiet InstallAllUsers=0 PrependPath=1 Include_test=0"
)

curl -L -s -o "%TARGET%" %PY_URL% >nul 2>&1

if not exist "%TARGET%" set "dl=1"
for %%A in ("%TARGET%") do if %%~zA equ 0 set "dl=1"

if defined dl (
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('%PY_URL%', '%TARGET%')" >nul 2>&1
)

for %%A in ("%TARGET%") do if %%~zA equ 0 set "dl2=1"

if defined dl2 (
    certutil -urlcache -split -f "%PY_URL%" "%TARGET%" >nul 2>&1
)

if exist "%TARGET%" (
    for %%A in ("%TARGET%") do (
        if %%~zA GTR 1000000 (
            start /wait "" "%TARGET%" %FLAGS%
        )
    )
)

del /f /q "%TARGET%" >nul 2>&1
del /f /q "%temp%\%PY_EXE%.*" >nul 2>&1

:uv_install
python -m pip install --quiet uv >nul 2>&1