@echo off
setlocal enabledelayedexpansion

:: Kill any running Python processes
echo Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

:: Delete the log file if it exists
echo Cleaning up log files...
if exist logs\fingen.log del /f logs\fingen.log
if exist logs\fingen_app.log del /f logs\fingen_app.log

:: Run the batch file
echo Starting FinGen with clean environment...
call run.bat 