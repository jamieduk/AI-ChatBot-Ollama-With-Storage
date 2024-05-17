@echo off
echo Starting Chatbot

:run_bot
REM Infinite loop
:loop
    echo Running chatbot script...
    python chatbot-ollamaV4.py
    REM Optional: add a small sleep to prevent a tight loop in case the script exits quickly
    timeout /t 1 >nul
goto loop

REM Prevent the command prompt from closing
cmd /k
