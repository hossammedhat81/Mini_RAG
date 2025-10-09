@echo off
echo ================================================================
echo  🌐 Mini RAG with Web Search - Quick Start
echo ================================================================
echo.
echo [1/2] Testing web search endpoint...
cd c:\University\Mini_RAG\mini-rag-app\streamlit_app
python test_web_search.py
echo.
echo.
echo [2/2] Starting Streamlit app...
echo.
echo ================================================================
echo  📌 INSTRUCTIONS:
echo ================================================================
echo  1. App will open at http://localhost:8501
echo  2. Click "⚙️ Settings" in sidebar
echo  3. Enable "🌐 Enable Internet Search"
echo  4. Ask: "What is the weather in Cairo?"
echo  5. You should see web results with sources!
echo ================================================================
echo.
pause
python -m streamlit run app_chatgpt_style.py
