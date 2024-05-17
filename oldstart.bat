@echo off
echo Starting Chatbot

REM Function to check if in venv
:check_venv
if defined VIRTUAL_ENV (
    echo Already in a virtual environment.
    exit /b 0
) else (
    if exist myenv\Scripts\activate.bat (
        echo Virtual environment 'myenv' exists.
        exit /b 0
    ) else (
        echo No virtual environment found.
        exit /b 1
    )
)

REM Main function to start venv
:start_venv
call :check_venv
if %errorlevel% equ 0 (
    goto run_bot
)

if exist myenv (
    echo Activating existing virtual environment 'myenv'...
    call myenv\Scripts\activate.bat
) else (
    echo Creating and activating new virtual environment 'myenv'...
    python -m venv myenv
    call myenv\Scripts\activate.bat
)

:run_bot
REM Infinite loop
:loop
    python chatbot-ollamaV4.py
    REM Optional: add a small sleep to prevent a tight loop in case the script exits quickly
    timeout /t 1 >nul
goto loop

cmd /k
