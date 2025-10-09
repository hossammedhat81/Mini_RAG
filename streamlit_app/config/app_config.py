"""
Application Configuration
Centralized configuration for the Mini RAG Streamlit app
"""

import os
from typing import List

# ============================================================================
# API CONFIGURATION
# ============================================================================

# Default to 127.0.0.1 for local development (more reliable than localhost)
# Use "http://fastapi:8000" when running in Docker
# Set API_BASE_URL environment variable to override
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Health check endpoint (backend has /api/v1/ not /api/v1/health)
HEALTH_CHECK_ENDPOINT = "/api/v1/"
HEALTH_CHECK_TIMEOUT = 5  # seconds

# ============================================================================
# FILE UPLOAD CONFIGURATION
# ============================================================================

ALLOWED_FILE_TYPES = ["pdf", "txt"]
MAX_FILE_SIZE_MB = 10
CHUNK_SIZE_DEFAULT = 1000
OVERLAP_SIZE_DEFAULT = 200
CHUNK_SIZE_MIN = 100
CHUNK_SIZE_MAX = 5000
OVERLAP_SIZE_MIN = 0
OVERLAP_SIZE_MAX = 500

# ============================================================================
# RAG CONFIGURATION
# ============================================================================

SEARCH_LIMIT_DEFAULT = 5
SEARCH_LIMIT_MIN = 1
SEARCH_LIMIT_MAX = 20

# ============================================================================
# UI CONFIGURATION
# ============================================================================

APP_TITLE = "Mini RAG System"
COMPANY_NAME = "e& Egypt"
APP_VERSION = "v3.0"

# Color scheme - e& Egypt branding
PRIMARY_COLOR = "#E31B6D"  # e& magenta
SECONDARY_COLOR = "#0a0e27"  # Dark blue
ACCENT_COLOR = "#00D9C0"  # Teal
BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#1a1a1a"

# ============================================================================
# PROCESSING CONFIGURATION
# ============================================================================

PROCESSING_BATCH_SIZE = 10

# ============================================================================
# TEMPLATES & MESSAGES
# ============================================================================

WELCOME_MESSAGE = """
Welcome to the **Mini RAG System** powered by **e& Egypt**! 

This intelligent document retrieval and question-answering system helps you:
- 📤 Upload and process documents (PDF, TXT)
- 🔍 Search through your document database
- 💬 Get AI-powered answers to your questions
- 📊 Manage multiple projects efficiently
"""

ABOUT_MESSAGE = """
### About Mini RAG System

The Mini RAG (Retrieval-Augmented Generation) System is a cutting-edge solution 
developed by **e& Egypt** for intelligent document management and question answering.

#### Key Features:
- **Document Processing**: Upload PDFs and text files with automatic chunking
- **Vector Indexing**: Advanced semantic search using vector embeddings
- **AI-Powered Q&A**: Get accurate answers from your documents
- **Multi-Project Support**: Manage multiple document collections
- **Real-time Processing**: Fast document processing and indexing

#### Technology Stack:
- **Backend**: FastAPI with async support
- **Vector Database**: Qdrant for efficient similarity search
- **LLM Integration**: OpenAI GPT & Cohere models
- **Frontend**: Streamlit for interactive UI

#### Version: 3.0
#### Company: e& Egypt
#### Year: 2025
"""
