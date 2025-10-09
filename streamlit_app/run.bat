@echo off
REM Run script for Mini RAG Streamlit App (Windows)

echo 🚀 Starting Mini RAG System...
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Starting Streamlit app...
echo    Access at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ================================
echo.

REM Run Streamlit
streamlit run app.py
