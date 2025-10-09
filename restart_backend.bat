@echo off
echo ================================================================
echo  e^& Egypt Mini-RAG - SQL Feature Backend Restart Script
echo ================================================================
echo.

echo [1/5] Stopping old backend process...
echo.
taskkill /F /PID 20360 2>nul
if %errorlevel%==0 (
    echo     ✓ Process 20360 stopped
) else (
    echo     ℹ Process 20360 not found or already stopped
)

echo.
echo [2/5] Waiting for port to be released...
timeout /t 2 /nobreak >nul
echo     ✓ Wait complete
echo.

echo [3/5] Checking if port 8000 is free...
netstat -ano | findstr :8000 >nul
if %errorlevel%==0 (
    echo     ⚠ Port 8000 still in use. Please close manually:
    echo       - Press Ctrl+Shift+Esc
    echo       - Find python.exe using port 8000
    echo       - End Task
    pause
) else (
    echo     ✓ Port 8000 is free
)

echo.
echo [4/5] Starting backend with SQL routes...
cd c:\University\Mini_RAG\mini-rag-app\src
echo     📂 Directory: %CD%
echo     🚀 Starting: python main.py
echo.
echo ================================================================
echo  Backend starting... Watch for "Application startup complete"
echo  Press Ctrl+C to stop
echo ================================================================
echo.

python main.py
