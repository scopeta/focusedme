@echo off
echo Installing FocusedMe for Windows...
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install focusedme with playsound for Windows
echo Installing FocusedMe dependencies...
python -m pip install playsound>=1.3.0 rich>=13.5.0

echo Installing FocusedMe...
python -m pip install focusedme

echo.
echo Installation complete! You can now run FocusedMe by typing:
echo.
echo     focusedme
echo.
echo For help, run:
echo.
echo     focusedme -h
echo.

pause
