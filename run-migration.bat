@echo off
echo Starting WordPress Migration Orchestrator...
echo.
echo This script requires WSL (Windows Subsystem for Linux) to run.
echo If you don't have WSL installed, please install it first.
echo.
pause

REM Check if WSL is available
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WSL is not installed or not available.
    echo Please install WSL first: https://docs.microsoft.com/en-us/windows/wsl/install
    pause
    exit /b 1
)

echo Switching to WSL environment...
echo.

REM Get the current directory and convert to WSL path
set "CURRENT_DIR=%CD%"
set "WSL_PATH=%CURRENT_DIR:\=/%"
set "WSL_PATH=%WSL_PATH:C:=/mnt/c%"

REM Execute the script in WSL
wsl bash -c "cd '%WSL_PATH%' && chmod +x wp-migration-orchestrator.sh && ./wp-migration-orchestrator.sh"

pause