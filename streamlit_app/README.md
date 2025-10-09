# Mini RAG System - Streamlit Interface

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.48.0-red)
![License](https://img.shields.io/badge/license-Proprietary-orange)

**Professional Streamlit Interface for Mini RAG System**

*Powered by e& Egypt*

</div>

---

## 📋 Overview

This is the **version 3.0** of the Mini RAG System Streamlit interface - a complete redesign featuring a modern, professional UI with enhanced functionality and user experience. Built specifically for e& Egypt's document retrieval and question-answering platform.

## ✨ Features

### 🎨 Modern UI/UX
- **Clean, professional interface** with e& Egypt branding
- **Responsive design** that works on all screen sizes
- **Intuitive navigation** with sidebar menu
- **Custom color scheme** matching corporate identity
- **Smooth animations** and interactive components

### 📤 Document Management
- Upload PDF and text files
- Automatic text extraction and processing
- Configurable chunking parameters
- Multi-project support
- Real-time processing status

### 🔍 Intelligent Search
- Semantic search through documents
- AI-powered question answering
- Adjustable search parameters
- Result relevance scoring
- Export search results

### 💬 Chat Interface
- Interactive Q&A interface
- Chat history with timestamps
- Context-aware responses
- Export conversations
- Multi-project chat management

### ⚙️ Advanced Configuration
- API endpoint configuration
- Processing parameter defaults
- Display preferences
- Theme customization
- Settings persistence

## 🏗️ Project Structure

```
streamlit_app/
│
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── config.toml                 # Streamlit configuration
│
├── config/
│   ├── __init__.py
│   └── app_config.py          # Application configuration
│
├── utils/
│   ├── __init__.py
│   ├── api_client.py          # API communication handler
│   └── ui_components.py       # Reusable UI components
│
├── pages/
│   ├── __init__.py
│   ├── home.py                # Home/dashboard page
│   ├── upload_process.py      # Upload and processing page
│   ├── query_interface.py     # Search and Q&A page
│   ├── settings_page.py       # Settings and configuration
│   └── about.py               # About and information page
│
└── assets/
    ├── README.md
    └── e_and_egypt_logo.png   # Company logo (to be added)
```

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- Access to Mini RAG FastAPI backend
- Internet connection for API calls

### Setup Steps

1. **Navigate to the streamlit_app directory:**
   ```bash
   cd streamlit_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add the e& Egypt logo (optional):**
   - Place `e_and_egypt_logo.png` in the `assets/` folder
   - Recommended size: 400x200 pixels
   - Format: PNG with transparent background

4. **Configure the API endpoint:**
   - The default API URL is `http://fastapi:8000`
   - You can change this in the Settings page after launch
   - Or set the `API_BASE_URL` environment variable

## 💻 Usage

### Running the Application

**Basic launch:**
```bash
streamlit run app.py
```

**With custom port:**
```bash
streamlit run app.py --server.port 8501
```

**With custom API URL:**
```bash
API_BASE_URL=http://localhost:8000 streamlit run app.py
```

### Accessing the Application

Once running, open your browser and navigate to:
```
http://localhost:8501
```

## 📖 User Guide

### Getting Started

1. **Select a Project**
   - Use the sidebar to select or create a project by entering a Project ID
   - Each project maintains its own document collection

2. **Upload Documents**
   - Navigate to "Upload & Process" page
   - Upload PDF or text files (max 10MB)
   - View file information before upload

3. **Process Documents**
   - Configure chunk size (recommended: 1000-2000 characters)
   - Set overlap size (recommended: 200-300 characters)
   - Process documents to prepare for indexing
   - Automatically index to vector database

4. **Ask Questions**
   - Go to "Query Interface" page
   - Type your question in natural language
   - Adjust number of context documents if needed
   - View AI-generated answers with source context

5. **Search Documents**
   - Use semantic search to find relevant chunks
   - Adjust result limit for more or fewer results
   - Export search results for offline use

### Configuration Tips

**For General Documents:**
- Chunk Size: 1000-1500
- Overlap: 200-300
- Use Case: Articles, reports, general text

**For Technical Documentation:**
- Chunk Size: 1500-2000
- Overlap: 300-400
- Use Case: Code docs, technical manuals

**For Short Content:**
- Chunk Size: 500-800
- Overlap: 100-150
- Use Case: News, blog posts

**For Legal Documents:**
- Chunk Size: 2000-3000
- Overlap: 400-500
- Use Case: Contracts, legal texts

## 🎨 Customization

### Branding

The application uses e& Egypt's corporate colors:
- **Primary:** #E31B6D (Magenta)
- **Secondary:** #0a0e27 (Dark Blue)
- **Accent:** #00D9C0 (Teal)

### Configuration Files

**config/app_config.py** - Modify default values:
- API endpoints
- File size limits
- Processing defaults
- UI preferences
- Color schemes

**config.toml** - Streamlit settings:
- CORS configuration
- Server settings
- Security options

### Custom CSS

All custom styling is in `utils/ui_components.py` in the `apply_custom_css()` function. Modify as needed for custom branding.

## 🔧 API Integration

The application communicates with the FastAPI backend through the following endpoints:

### Upload Endpoint
```
POST /api/v1/data/upload/{project_id}
```

### Process Endpoint
```
POST /api/v1/data/process/{project_id}
```

### Index Endpoint
```
POST /api/v1/nlp/index/push/{project_id}
```

### Search Endpoint
```
POST /api/v1/nlp/index/search/{project_id}
```

### Q&A Endpoint
```
POST /api/v1/nlp/index/answer/{project_id}
```

### Info Endpoint
```
GET /api/v1/nlp/index/info/{project_id}
```

## 📊 System Requirements

### Minimum Requirements
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Storage:** 1 GB free space
- **Network:** Stable internet connection

### Recommended Requirements
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **Storage:** 5+ GB free space
- **Network:** High-speed connection

## 🐛 Troubleshooting

### Common Issues

**1. API Connection Failed**
- Check if FastAPI backend is running
- Verify API URL in Settings
- Check network connectivity
- Ensure CORS is properly configured

**2. File Upload Fails**
- Check file size (max 10MB)
- Verify file format (PDF or TXT only)
- Ensure sufficient disk space
- Check file permissions

**3. Processing Errors**
- Verify documents are uploaded first
- Check processing parameters are valid
- Ensure backend has sufficient resources
- Review backend logs for errors

**4. No Search Results**
- Ensure documents are processed and indexed
- Try different search queries
- Check project ID is correct
- Verify vector database is connected

**5. Slow Performance**
- Reduce chunk size for faster processing
- Lower search result limit
- Check backend server resources
- Optimize network connection

**6. 400 Bad Request Error** ⚠️ **COMMON ISSUE**
- **MOST LIKELY**: Index is empty - upload and process documents first!
- **Check Project ID**: Make sure project ID in settings matches your backend
- **Run Diagnostic Tool**: `python diagnostic_tool.py` to check all systems
- **See Detailed Guide**: `docs/TROUBLESHOOTING_400_ERROR.md`

## 🔧 Quick Diagnostic

If you're experiencing issues (especially 400 errors), run our diagnostic tool:

```powershell
# Navigate to streamlit_app folder
cd c:\University\Mini_RAG\mini-rag-app\streamlit_app

# Run the diagnostic
python diagnostic_tool.py
```

This will check:
- ✅ Backend health and connectivity
- ✅ Project existence and status
- ✅ Index health and document count
- ✅ Search endpoint functionality
- ✅ Answer endpoint functionality

For detailed troubleshooting steps, see: **[docs/TROUBLESHOOTING_400_ERROR.md](docs/TROUBLESHOOTING_400_ERROR.md)**

## 📚 Additional Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- Mini RAG System API Documentation (check backend)

### Support
- Contact system administrator
- Check backend logs
- Review error messages in UI
- Consult API documentation

## 🔐 Security Notes

- Never commit `.env` files with credentials
- Use environment variables for sensitive data
- Implement proper authentication in production
- Use HTTPS for production deployments
- Regularly update dependencies

## 📝 Version History

### Version 3.0 (Current)
- ✅ Complete UI/UX redesign
- ✅ Modern component-based architecture
- ✅ Enhanced chat history
- ✅ Advanced settings page
- ✅ Improved error handling
- ✅ Mobile-responsive design
- ✅ Custom branding integration

### Version 2.0
- Multi-project support
- Improved document processing
- Enhanced search functionality

### Version 1.0
- Initial release
- Basic upload and Q&A
- PDF and TXT support

## 👥 Credits

**Developed by:** e& Egypt Digital Solutions Team  
**Version:** 3.0  
**Year:** 2025

---

## 📄 License

Proprietary - © 2025 e& Egypt. All rights reserved.

This software is the property of e& Egypt and is intended for internal use only. Unauthorized copying, distribution, or use is strictly prohibited.

---

<div align="center">

**Made with ❤️ by e& Egypt**

*Empowering Digital Transformation*

</div>
