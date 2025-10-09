@echo off
echo ================================================================
echo  e^& Egypt Mini-RAG - SQL Chat App Launcher
echo ================================================================
echo.
echo Checking if backend is running...
curl -s http://127.0.0.1:8000/docs >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Backend is running
) else (
    echo ✗ Backend not running!
    echo.
    echo Please start backend first:
    echo   1. Open PowerShell
    echo   2. Run: cd c:\University\Mini_RAG\mini-rag-app\src
    echo   3. Run: python main.py
    echo.
    pause
    exit /b 1
)

echo.
echo Launching Streamlit SQL Chat App...
cd c:\University\Mini_RAG\mini-rag-app\streamlit_app
echo 📂 Directory: %CD%
echo 🚀 Starting: streamlit run app_sql_chat.py
echo.
echo ================================================================
echo  App will open in your browser at http://localhost:8501
echo  Press Ctrl+C to stop
echo ================================================================
echo.

streamlit run app_sql_chat.py
