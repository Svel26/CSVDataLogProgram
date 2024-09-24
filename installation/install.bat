@echo off

REM Check if virtual environment exists
if not exist "..\.venv" (
    echo Creating virtual environment...
    python -m venv ..\.venv
)

REM Activate virtual environment
call ..\.venv\Scripts\activate.bat

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Pip is not recognized. Please ensure Python is installed and added to PATH.
    pause
    exit /b
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if installation was successful
if errorlevel 1 (
    echo Failed to install dependencies. Please check the requirements.txt file.
    pause
    exit /b
)

REM Completed
echo Installation Complete!

REM Pause the command window
pause
