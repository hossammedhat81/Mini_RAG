@echo off
echo ================================================================
echo  🔍 WEB SEARCH DEBUG MODE - Complete Diagnostic
echo ================================================================
echo.

cd c:\University\Mini_RAG\mini-rag-app\streamlit_app

echo [Step 1/3] Testing Backend Web Search Endpoint...
echo ----------------------------------------------------------------
python test_web_search_diagnostic.py
echo.
echo.

echo [Step 2/3] Checking if backend is running...
echo ----------------------------------------------------------------
curl -s http://127.0.0.1:8000/ >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Backend is responding
) else (
    echo ❌ Backend NOT responding
    echo.
    echo To start backend:
    echo   cd c:\University\Mini_RAG\mini-rag-app\src
    echo   python main.py
    echo.
    pause
    exit /b
)
echo.
echo.

echo [Step 3/3] Starting Streamlit with Debug Mode...
echo ================================================================
echo.
echo 📌 WATCH FOR DEBUG OUTPUT IN THIS WINDOW:
echo ================================================================
echo   [DEBUG] enable_web_search = True
echo   [DEBUG] Web search result signal: WEB_SEARCH_SUCCESS
echo   [DEBUG] Adding message with metadata: web_search
echo   [DEBUG RENDER] Source: web_search
echo   [DEBUG RENDER] Is web search: True
echo ================================================================
echo.
echo 📋 IN BROWSER:
echo ================================================================
echo   1. Enable "🌐 Enable Internet Search" in Settings
echo   2. Click "🗑️ Clear Chat" to remove old messages
echo   3. Ask: "What is e& Egypt?"
echo   4. Watch for toast messages:
echo      - "🌐 Web Search Mode - Searching internet..."
echo      - "✅ Found 3 sources"
echo   5. Check badge:
echo      - Should be: 🌐 From Web Search (TEAL)
echo      - NOT: 📚 From Documents (PINK)
echo ================================================================
echo.
echo 🐛 IF BADGE IS WRONG:
echo ================================================================
echo   1. Check console output above (this window)
echo   2. Look for [DEBUG RENDER] lines
echo   3. Press Ctrl+C to stop
echo   4. Read DEBUG_GUIDE.md for solutions
echo ================================================================
echo.
pause
python -m streamlit run app_chatgpt_style.py
