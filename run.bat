@echo off
title CAPACITY CONNECT — Employee Performance Portal
color 0b
cd /d "%~dp0"

echo ======================================================================
echo           CAPACITY CONNECT — Streamlit Performance Portal
echo ======================================================================
echo.

:: 1. Check if .venv exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at "%~dp0.venv"
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment. Ensure Python is installed and in PATH.
        goto :error
    )
    echo [INFO] Installing required dependencies...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies from requirements.txt.
        goto :error
    )
) else (
    echo [OK] Virtual environment detected: .venv
)

:: 2. Activate Virtual Environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    goto :error
)

:: 3. Verify Streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Streamlit is not installed in .venv. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed.
        goto :error
    )
)

:: 4. Launch Streamlit Application
echo.
echo ======================================================================
echo  Starting Capacity Connect on http://localhost:8501
echo  Press Ctrl+C in this terminal window to stop the server.
echo ======================================================================
echo.

python -m streamlit run app.py

if errorlevel 1 (
    goto :error
)

goto :end

:error
echo.
echo ======================================================================
echo [ERROR] An error occurred while launching the application.
echo ======================================================================
pause
exit /b 1

:end
exit /b 0
