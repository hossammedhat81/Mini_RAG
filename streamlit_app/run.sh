#!/bin/bash
# Run script for Mini RAG Streamlit App

echo "🚀 Starting Mini RAG System..."
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting Streamlit app..."
echo "   Access at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

# Run Streamlit
streamlit run app.py
