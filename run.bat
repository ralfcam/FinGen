@echo off
setlocal enabledelayedexpansion

:: Create logs directory if it doesn't exist
if not exist logs mkdir logs

:: Use a fixed log file that gets reset each time
set LOGFILE=logs\fingen.log

:: Clear existing log file and start new log
echo [%date% %time%] Starting FinGen setup... > %LOGFILE%

echo Setting up FinGen...
echo [%date% %time%] Setting up FinGen... >> %LOGFILE%

:: Check if Python is installed
echo [%date% %time%] Checking Python installation... >> %LOGFILE%
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    echo [%date% %time%] ERROR: Python is not installed >> %LOGFILE%
    exit /b 1
)
python --version >> %LOGFILE% 2>&1

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    echo [%date% %time%] Creating virtual environment... >> %LOGFILE%
    python -m venv venv >> %LOGFILE% 2>&1
    if errorlevel 1 (
        echo [%date% %time%] ERROR: Failed to create virtual environment >> %LOGFILE%
        echo Failed to create virtual environment. See %LOGFILE% for details.
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
echo [%date% %time%] Activating virtual environment... >> %LOGFILE%
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [%date% %time%] ERROR: Failed to activate virtual environment >> %LOGFILE%
    echo Failed to activate virtual environment. See %LOGFILE% for details.
    exit /b 1
)

:: Ensure pip is updated
echo Updating pip...
echo [%date% %time%] Updating pip... >> %LOGFILE%
python -m pip install --upgrade pip >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo [%date% %time%] WARNING: Failed to update pip >> %LOGFILE%
    echo Warning: Failed to update pip. Continuing anyway...
)

:: Install dependencies
echo Installing dependencies...
echo [%date% %time%] Installing dependencies... >> %LOGFILE%
pip install -r requirements.txt >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo [%date% %time%] ERROR: Failed to install dependencies >> %LOGFILE%
    echo Failed to install dependencies. See %LOGFILE% for details.
    exit /b 1
)

:: Kill any existing Python processes that might be running the app
taskkill /f /im python.exe /fi "WINDOWTITLE eq C:\Users\joser\PycharmProjects\FinGen*" >nul 2>&1

:: Run the application with custom environment variable to avoid log file permission issues
echo Starting FinGen...
echo [%date% %time%] Starting FinGen... >> %LOGFILE%
echo [%date% %time%] Command: python app.py >> %LOGFILE%
set FINGEN_LOG_NAME=fingen_app
python app.py >> %LOGFILE% 2>&1
set APP_EXIT_CODE=%errorlevel%

:: Log completion
echo [%date% %time%] Application exited with code %APP_EXIT_CODE% >> %LOGFILE%
echo Log file created at %LOGFILE%

:: Exit with application's exit code without pausing
if %APP_EXIT_CODE% neq 0 (
    echo Application exited with errors. See %LOGFILE% for details.
    exit /b %APP_EXIT_CODE%
) 