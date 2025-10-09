"""
Simple Mini RAG Streamlit App
Replicates Postman API endpoints for FastAPI backend
"""

import streamlit as st
import requests
import json
from typing import Optional, Dict, Any
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# Default API base URL
DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"

# Project ID (can be changed in sidebar)
DEFAULT_PROJECT_ID = 26

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def make_request(method: str, url: str, **kwargs) -> Dict[str, Any]:
    """
    Make HTTP request with error handling
    
    Args:
        method: HTTP method (GET, POST)
        url: Full URL
        **kwargs: Additional arguments for requests
        
    Returns:
        Dict with 'success' boolean and 'data' or 'error'
    """
    try:
        response = requests.request(method, url, timeout=120, **kwargs)
        
        if response.status_code in [200, 201]:
            try:
                return {"success": True, "data": response.json(), "status_code": response.status_code}
            except:
                return {"success": True, "data": response.text, "status_code": response.status_code}
        else:
            try:
                error_data = response.json()
            except:
                error_data = response.text
            return {
                "success": False, 
                "error": error_data, 
                "status_code": response.status_code
            }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out (120s limit)"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to API. Is the backend running?"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def display_response(response: Dict[str, Any], title: str = "Response"):
    """Display API response in a nice format"""
    if response.get("success"):
        st.success(f"✅ {title} - Status {response.get('status_code', 200)}")
        
        data = response.get("data", {})
        
        # Display as formatted JSON
        st.json(data)
        
        # Add download button for response
        st.download_button(
            label="💾 Download Response JSON",
            data=json.dumps(data, indent=2),
            file_name=f"response_{int(time.time())}.json",
            mime="application/json"
        )
    else:
        st.error(f"❌ {title} Failed")
        st.code(json.dumps(response.get("error", "Unknown error"), indent=2))
        if "status_code" in response:
            st.warning(f"Status Code: {response['status_code']}")

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Mini RAG API Client",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E31B6D;
        margin-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0a0e27;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #E31B6D;
        padding-bottom: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(227, 27, 109, 0.3);
    }
    div[data-testid="stExpander"] {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Base URL
    api_base_url = st.text_input(
        "API Base URL",
        value=DEFAULT_API_BASE_URL,
        help="Change this if your API is running on a different host/port"
    )
    
    # Project ID
    project_id = st.number_input(
        "Project ID",
        min_value=1,
        value=DEFAULT_PROJECT_ID,
        help="Project ID for all operations"
    )
    
    st.markdown("---")
    
    # Connection Test
    st.markdown("### 🔗 Connection Status")
    if st.button("Test Connection", use_container_width=True):
        with st.spinner("Testing..."):
            result = make_request("GET", f"{api_base_url}/api/v1/")
            if result.get("success"):
                st.success("✅ Connected!")
                st.json(result.get("data"))
            else:
                st.error("❌ Connection Failed")
                st.code(result.get("error"))
    
    st.markdown("---")
    
    # Info
    st.markdown("### ℹ️ Info")
    st.info("""
    **Mini RAG API Client**
    
    Simple interface to interact with your FastAPI backend.
    
    - Upload files
    - Process documents
    - Index data
    - Search & Q&A
    """)

# ============================================================================
# MAIN APP
# ============================================================================

# Header
st.markdown('<div class="main-header">🚀 Mini RAG API Client</div>', unsafe_allow_html=True)
st.markdown(f"**Current Project ID:** `{project_id}` | **API:** `{api_base_url}`")
st.markdown("---")

# ============================================================================
# SECTION 1: FILE UPLOAD & PROCESSING
# ============================================================================

st.markdown('<div class="section-header">📤 File Upload & Processing</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 1️⃣ Upload File")
    st.markdown(f"**Endpoint:** `POST /api/v1/data/upload/{project_id}`")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx", "doc"],
        help="Upload PDF, TXT, or DOCX files"
    )
    
    if uploaded_file is not None:
        st.info(f"📄 Selected: **{uploaded_file.name}** ({uploaded_file.size:,} bytes)")
        
        if st.button("🚀 Upload File", key="upload_btn"):
            with st.spinner("Uploading..."):
                # Prepare file for upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # Make request
                result = make_request(
                    "POST",
                    f"{api_base_url}/api/v1/data/upload/{project_id}",
                    files=files
                )
                
                display_response(result, "File Upload")
                
                # Store file_id in session state if successful
                if result.get("success"):
                    data = result.get("data", {})
                    if "file_id" in data:
                        st.session_state.last_file_id = data["file_id"]
                        st.success(f"File ID: `{data['file_id']}`")

with col2:
    st.markdown("#### 2️⃣ Process Data")
    st.markdown(f"**Endpoint:** `POST /api/v1/data/process/{project_id}`")
    
    # Processing parameters
    with st.expander("⚙️ Processing Parameters", expanded=True):
        chunk_size = st.number_input(
            "Chunk Size",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100,
            help="Size of text chunks in characters"
        )
        
        overlap_size = st.number_input(
            "Overlap Size",
            min_value=0,
            max_value=500,
            value=200,
            step=50,
            help="Overlap between chunks"
        )
        
        do_reset = st.checkbox(
            "Reset Existing Chunks",
            value=False,
            help="Delete all existing chunks before processing"
        )
        
        file_id = st.text_input(
            "Specific File ID (optional)",
            value="",
            help="Leave empty to process all files"
        )
    
    if st.button("⚡ Process Data", key="process_btn"):
        with st.spinner("Processing... This may take a while."):
            # Prepare payload
            payload = {
                "chunk_size": chunk_size,
                "overlap_size": overlap_size,
                "do_reset": 1 if do_reset else 0
            }
            
            # Only add file_id if it's not empty
            if file_id and file_id.strip():
                payload["file_id"] = file_id.strip()
            else:
                payload["file_id"] = ""  # Send empty string instead of None
            
            # Make request
            result = make_request(
                "POST",
                f"{api_base_url}/api/v1/data/process/{project_id}",
                json=payload
            )
            
            display_response(result, "Data Processing")

# ============================================================================
# SECTION 2: NLP INDEX OPERATIONS
# ============================================================================

st.markdown('<div class="section-header">🔧 NLP Index Operations</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 3️⃣ Push to NLP Index")
    st.markdown(f"**Endpoint:** `POST /api/v1/nlp/index/push/{project_id}`")
    
    with st.expander("⚙️ Index Parameters", expanded=True):
        do_reset_index = st.checkbox(
            "Reset Index",
            value=False,
            help="Delete existing index before pushing",
            key="reset_index"
        )
    
    if st.button("🚀 Push to Index", key="push_btn"):
        with st.spinner("Indexing... This may take a while."):
            # Prepare payload
            payload = {
                "do_reset": 1 if do_reset_index else 0
            }
            
            # Make request
            result = make_request(
                "POST",
                f"{api_base_url}/api/v1/nlp/index/push/{project_id}",
                json=payload
            )
            
            display_response(result, "Index Push")

with col2:
    st.markdown("#### 4️⃣ Show Index Info")
    st.markdown(f"**Endpoint:** `GET /api/v1/nlp/index/info/{project_id}`")
    
    st.markdown("")  # Spacing
    st.markdown("")  # Spacing
    
    if st.button("📊 Get Index Info", key="info_btn"):
        with st.spinner("Fetching index information..."):
            # Make request
            result = make_request(
                "GET",
                f"{api_base_url}/api/v1/nlp/index/info/{project_id}"
            )
            
            display_response(result, "Index Information")

# ============================================================================
# SECTION 3: SEARCH & Q&A
# ============================================================================

st.markdown('<div class="section-header">🔍 Search & Q&A</div>', unsafe_allow_html=True)

# Create tabs for Search and Q&A
tab1, tab2 = st.tabs(["🔍 Search Documents", "💬 Ask Questions"])

# ============================================================================
# TAB 1: SEARCH
# ============================================================================

with tab1:
    st.markdown("#### 5️⃣ Search Index")
    st.markdown(f"**Endpoint:** `POST /api/v1/nlp/index/search/{project_id}`")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., What are the main topics?",
            help="Enter your search query",
            key="search_query"
        )
    
    with col2:
        search_limit = st.number_input(
            "Results",
            min_value=1,
            max_value=20,
            value=5,
            help="Number of results to return"
        )
    
    if st.button("🔍 Search", key="search_btn", use_container_width=True):
        if not search_query.strip():
            st.warning("⚠️ Please enter a search query")
        else:
            with st.spinner("Searching..."):
                # Prepare payload
                payload = {
                    "text": search_query,
                    "limit": search_limit
                }
                
                # Make request
                result = make_request(
                    "POST",
                    f"{api_base_url}/api/v1/nlp/index/search/{project_id}",
                    json=payload
                )
                
                if result.get("success"):
                    st.success(f"✅ Search Complete - Status {result.get('status_code', 200)}")
                    
                    data = result.get("data", {})
                    results = data.get("results", [])
                    
                    if results:
                        st.markdown(f"### 📊 Found {len(results)} Results")
                        
                        for i, res in enumerate(results, 1):
                            score = res.get("score", 0)
                            text = res.get("chunk_text", "")
                            metadata = res.get("chunk_metadata", {})
                            
                            with st.expander(f"📝 Result {i} - Score: {score:.4f}", expanded=(i==1)):
                                st.markdown("**Content:**")
                                st.write(text)
                                
                                if metadata:
                                    st.markdown("---")
                                    st.markdown("**Metadata:**")
                                    st.json(metadata)
                        
                        # Download results
                        st.markdown("---")
                        st.download_button(
                            label="💾 Download Search Results",
                            data=json.dumps(results, indent=2),
                            file_name=f"search_results_{int(time.time())}.json",
                            mime="application/json"
                        )
                    else:
                        st.info("ℹ️ No results found")
                else:
                    display_response(result, "Search")

# ============================================================================
# TAB 2: Q&A
# ============================================================================

with tab2:
    st.markdown("#### 6️⃣ Ask Questions (RAG)")
    st.markdown(f"**Endpoint:** `POST /api/v1/nlp/index/answer/{project_id}`")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_area(
            "Your Question",
            placeholder="e.g., What is this document about?",
            help="Ask a question about your documents",
            height=100,
            key="question"
        )
    
    with col2:
        answer_limit = st.number_input(
            "Context Docs",
            min_value=1,
            max_value=20,
            value=3,
            help="Number of context documents to retrieve"
        )
        
        show_context = st.checkbox(
            "Show Context",
            value=False,
            help="Display retrieved context"
        )
    
    if st.button("🤖 Get Answer", key="answer_btn", use_container_width=True):
        if not question.strip():
            st.warning("⚠️ Please enter a question")
        else:
            with st.spinner("🤔 Thinking... Generating answer..."):
                # Prepare payload
                payload = {
                    "text": question,
                    "limit": answer_limit
                }
                
                # Make request
                result = make_request(
                    "POST",
                    f"{api_base_url}/api/v1/nlp/index/answer/{project_id}",
                    json=payload
                )
                
                if result.get("success"):
                    st.success(f"✅ Answer Generated - Status {result.get('status_code', 200)}")
                    
                    data = result.get("data", {})
                    answer_text = data.get("answer", "")
                    full_prompt = data.get("full_prompt", "")
                    chat_history = data.get("chat_history", [])
                    
                    # Display as chat
                    st.markdown("---")
                    st.markdown("### 💬 Conversation")
                    
                    # User question
                    with st.chat_message("user"):
                        st.markdown(question)
                    
                    # Assistant answer
                    with st.chat_message("assistant"):
                        st.markdown(answer_text)
                    
                    # Show context if requested
                    if show_context:
                        st.markdown("---")
                        with st.expander("📄 View Full Context"):
                            st.markdown("**Full Prompt:**")
                            st.text_area("Prompt", value=full_prompt, height=300, disabled=True)
                            
                            if chat_history:
                                st.markdown("**Chat History:**")
                                st.json(chat_history)
                    
                    # Download Q&A
                    st.markdown("---")
                    qa_data = {
                        "question": question,
                        "answer": answer_text,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "project_id": project_id,
                        "full_prompt": full_prompt,
                        "chat_history": chat_history
                    }
                    
                    st.download_button(
                        label="💾 Download Q&A",
                        data=json.dumps(qa_data, indent=2),
                        file_name=f"qa_{int(time.time())}.json",
                        mime="application/json"
                    )
                else:
                    display_response(result, "Question Answering")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <strong>Mini RAG API Client</strong> | 
    Built with Streamlit 🎈 | 
    FastAPI Backend 🚀
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INFO (FOR DEBUGGING)
# ============================================================================

with st.sidebar:
    st.markdown("---")
    with st.expander("🐛 Debug Info"):
        st.json({
            "API Base URL": api_base_url,
            "Project ID": project_id,
            "Session State": dict(st.session_state)
        })
