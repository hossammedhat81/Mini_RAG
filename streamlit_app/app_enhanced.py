"""
Mini RAG System - Professional Dashboard (Enhanced Version)
Advanced UI/UX with e& Egypt branding
Powered by Hossam Medhat for e& Egypt

This is the production-ready version with enhanced UI/UX while maintaining
all working logic from streamlit_app_version2.py
"""

import streamlit as st
import requests
import os
from typing import Optional
import json
from io import BytesIO
from pydantic import BaseModel
import time
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "http://127.0.0.1:8000"

# ============================================================================
# PYDANTIC MODELS (Same as version2 - Don't change, they work!)
# ============================================================================

class ProcessRequest(BaseModel):
    file_id: Optional[str] = ""
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0

class SearchRequest(BaseModel):
    text: str
    limit: int = 5

class PushRequest(BaseModel):
    do_reset: int = 0

# ============================================================================
# API FUNCTIONS (Same as version2 - Don't change, they work!)
# ============================================================================

def upload_file(project_id: int, file: BytesIO, filename: str):
    content_type = 'application/pdf' if filename.lower().endswith('.pdf') else file.type
    files = {'file': (filename, file, content_type)}
    url = f"{API_BASE_URL}/api/v1/data/upload/{project_id}"
    response = requests.post(url, files=files)
    return response.json()

def process_file(project_id: int, process_request: ProcessRequest):
    url = f"{API_BASE_URL}/api/v1/data/process/{project_id}"    
    response = requests.post(url, json=process_request.model_dump())
    return response.json()

def push_to_index(project_id: int, push_request: PushRequest):
    url = f"{API_BASE_URL}/api/v1/nlp/index/push/{project_id}"
    response = requests.post(url, json=push_request.model_dump())
    return response.json()

def get_index_info(project_id: int):
    url = f"{API_BASE_URL}/api/v1/nlp/index/info/{project_id}"
    response = requests.get(url)
    return response.json()

def search_index(project_id: int, search_request: SearchRequest):
    url = f"{API_BASE_URL}/api/v1/nlp/index/search/{project_id}"
    response = requests.post(url, json=search_request.model_dump())
    return response.json()

def ask_question(project_id: int, search_request: SearchRequest):
    url = f"{API_BASE_URL}/api/v1/nlp/index/answer/{project_id}"
    response = requests.post(url, json=search_request.model_dump())
    return response.json()

# ============================================================================
# UI HELPER FUNCTIONS (New - Enhanced UX)
# ============================================================================

def render_header():
    """Render the app header with e& branding"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # Check if logo exists, if not show placeholder
        logo_path = "assets/e_and_egypt_logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=250)
        else:
            st.markdown("# 🎯 e&")
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #E31B6D; margin: 0;'>Mini RAG System</h1>
            <p style='color: #6c757d; font-size: 1.1rem; margin: 5px 0;'>
                Intelligent Document Processing & AI-Powered Q&A
            </p>
            <p style='color: #6c757d; font-size: 1.1rem; margin: 5px 0;'>
                Powered by Hossam Medhat for e& Egypt
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: right; padding: 10px;'>
            <p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>
                Version 3.0<br>
                Advanced UI
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    """Render the app footer with credits"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #E31B6D 0%, #0a0e27 100%); 
                border-radius: 10px; margin-top: 30px;'>
        <p style='color: white; font-size: 1rem; margin: 5px 0; font-weight: 600;'>
            🚀 Powered by <strong>Hossam Medhat</strong> for <strong>e& Egypt</strong>
        </p>
        <p style='color: #f8f9fa; font-size: 0.85rem; margin: 5px 0;'>
            Advanced AI Solutions | Document Intelligence | RAG Technology
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_status_card(title: str, value: str, icon: str, color: str = "#E31B6D"):
    """Display a status card"""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
                border: 3px solid {color}; padding: 20px; border-radius: 12px; margin: 15px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <div style='display: flex; align-items: center; justify-content: center;'>
            <span style='font-size: 2.5rem; margin-right: 20px;'>{icon}</span>
            <div style='text-align: center;'>
                <p style='color: #ecf0f1; font-size: 1rem; margin: 0; font-weight: 500;'>{title}</p>
                <p style='color: #ffffff; font-size: 2rem; font-weight: 700; margin: 8px 0;'>{value}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_success_message(message: str, show_balloons: bool = False):
    """Display success message with optional animation"""
    st.success(f"✅ {message}")
    if show_balloons:
        st.balloons()

def show_error_message(message: str):
    """Display error message"""
    st.error(f"❌ {message}")

def show_info_box(message: str):
    """Display info box"""
    st.info(f"💡 {message}")

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def render_upload_process_page(project_id: int):
    """Upload & Process Documents Page"""
    
    st.markdown("## 📤 Upload & Process Documents")
    st.markdown("Upload your documents and process them into searchable chunks")
    st.markdown("---")
    
    # Project ID display
    show_status_card("Current Project ID", str(project_id), "🎯", "#0a0e27")
    
    # Upload Section
    st.markdown("### 📁 File Upload")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a file to upload",
            type=["txt", "pdf"],
            help="Upload PDF or TXT files for processing"
        )
    
    with col2:
        if uploaded_file is not None:
            st.markdown("#### 📊 File Details")
            st.markdown(f"**Name:** {uploaded_file.name}")
            st.markdown(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
            st.markdown(f"**Type:** {uploaded_file.type}")
    
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Upload File", use_container_width=True, type="primary"):
                with st.spinner("⏳ Uploading file..."):
                    try:
                        result = upload_file(project_id, uploaded_file, uploaded_file.name)
                        show_success_message("File uploaded successfully!", show_balloons=True)
                        
                        # Display result in expandable section
                        with st.expander("📋 View Upload Details", expanded=True):
                            st.json(result)
                            
                            if "file_id" in result:
                                st.session_state.last_file_id = result["file_id"]
                                st.success(f"🆔 File ID: `{result['file_id']}`")
                    except Exception as e:
                        show_error_message(f"Upload failed: {str(e)}")
    
    st.markdown("---")
    
    # Processing Section
    st.markdown("### ⚙️ Document Processing")
    st.markdown("Configure processing parameters and chunk your documents")
    
    # Enhanced processing form with dark theme and better visibility
    st.markdown("""
    <style>
        div[data-testid="stForm"] {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
            padding: 30px !important;
            border-radius: 12px !important;
            border: 2px solid #E31B6D !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        }
        div[data-testid="stForm"] label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
        }
        div[data-testid="stForm"] p {
            color: #ecf0f1 !important;
        }
        div[data-testid="stForm"] h4 {
            color: #ffffff !important;
            font-weight: 700 !important;
            margin-bottom: 20px !important;
        }
        div[data-testid="stForm"] input {
            background-color: #ffffff !important;
            border: 2px solid #bdc3c7 !important;
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        div[data-testid="stForm"] .stNumberInput > div > div > input {
            color: #2c3e50 !important;
            font-size: 1.1rem !important;
        }
        div[data-testid="stForm"] .stTextInput > div > div > input {
            color: #2c3e50 !important;
            font-size: 1.1rem !important;
        }
        div[data-testid="stForm"] .stCheckbox > label > div {
            color: #ffffff !important;
        }
        div[data-testid="stForm"] small {
            color: #bdc3c7 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("process_form", clear_on_submit=False):
        st.markdown("""
        <div style='background-color: #2c3e50; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: #ffffff; font-weight: 600; margin: 0; text-align: center;'>
                🔧 Processing Configuration
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            chunk_size = st.number_input(
                "Chunk Size (characters)",
                min_value=100,
                max_value=5000,
                value=200,
                step=100,
                help="Size of text chunks in characters"
            )
            
            file_id = st.text_input(
                "Specific File ID (optional)",
                value="",
                placeholder="Leave empty to process all files",
                help="Enter a specific file ID or leave blank for all files"
            )
        
        with col2:
            overlap_size = st.number_input(
                "Overlap Size (characters)",
                min_value=0,
                max_value=500,
                value=20,
                step=50,
                help="Number of overlapping characters between chunks"
            )
            
            do_reset = st.checkbox(
                "🔄 Reset Existing Chunks",
                value=False,
                help="Delete all existing chunks before processing"
            )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "⚡ Process Documents",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            st.markdown("---")
            st.markdown("### 🔄 Processing Status")
            
            # Process documents
            process_req = {
                "chunk_size": chunk_size,
                "overlap_size": overlap_size,
                "do_reset": 1 if do_reset else 0,
                "file_id": file_id if file_id.strip() else ""
            }
            process_req = ProcessRequest(**process_req)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Process
                status_text.text("📝 Processing documents...")
                progress_bar.progress(33)
                
                result = process_file(project_id=project_id, process_request=process_req)
                
                progress_bar.progress(66)
                status_text.text("✅ Processing completed!")
                
                show_success_message("Documents processed successfully!", show_balloons=False)
                
                with st.expander("📋 View Processing Details", expanded=True):
                    st.json(result)
                
                st.markdown("---")
                
                # Step 2: Index
                st.markdown("### 🔄 Indexing to Vector Database")
                status_text.text("🗂️ Building vector index...")
                
                do_reset_index = 0
                push_req = PushRequest(do_reset=do_reset_index)
                
                index_result = push_to_index(project_id, push_req)
                
                progress_bar.progress(100)
                status_text.text("✅ All operations completed!")
                
                show_success_message("Indexing completed successfully!", show_balloons=False)
                
                with st.expander("📋 View Indexing Details", expanded=True):
                    st.json(index_result)
                
                # Clear progress indicators
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                show_error_message(f"Operation failed: {str(e)}")

def render_search_query_page(project_id: int):
    """Search & Query Documents Page"""
    
    st.markdown("## 💬 Search & Query Documents")
    st.markdown("Ask questions or search through your indexed documents using AI")
    st.markdown("---")
    
    # Project ID display
    show_status_card("Current Project ID", str(project_id), "🎯", "#0a0e27")
    
    # Create tabs for different query modes
    tab1, tab2 = st.tabs(["🤖 Ask Questions (RAG)", "🔍 Search Documents"])
    
    # ========================================================================
    # TAB 1: ASK QUESTIONS
    # ========================================================================
    with tab1:
        st.markdown("### 🤖 AI-Powered Question Answering")
        
        show_info_box(
            "Ask questions about your documents. The AI will search through your "
            "knowledge base and provide contextual answers using advanced RAG technology."
        )
        
        # Question input
        question = st.text_area(
            "Your Question",
            height=120,
            placeholder="e.g., What are the main topics discussed in the documents?",
            help="Type your question here. Be as specific as possible for better results."
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            pass  # Spacer
        
        with col2:
            limit = st.slider(
                "Context Documents",
                min_value=1,
                max_value=20,
                value=3,
                help="Number of relevant documents to retrieve for context"
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            ask_button = st.button(
                "🚀 Get Answer",
                use_container_width=True,
                type="primary"
            )
        
        if ask_button:
            if not question.strip():
                st.warning("⚠️ Please enter a question!")
            else:
                with st.spinner("🤔 Thinking... Generating answer..."):
                    try:
                        search_req = SearchRequest(text=question, limit=limit)
                        result = ask_question(project_id, search_req)
                        
                        if "answer" in result:
                            st.markdown("---")
                            st.markdown("### 🎯 Answer")
                            
                            # Display as chat messages
                            with st.chat_message("user"):
                                st.markdown(question)
                            
                            with st.chat_message("assistant"):
                                st.markdown(result["answer"])
                            
                            # Success feedback
                            show_success_message("Answer generated successfully!", show_balloons=False)
                            
                            # Store in session state for history
                            if 'qa_history' not in st.session_state:
                                st.session_state.qa_history = []
                            
                            st.session_state.qa_history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'question': question,
                                'answer': result["answer"],
                                'project_id': project_id
                            })
                            
                            # Show details
                            with st.expander("📄 View Full Context & Details"):
                                st.markdown("**Full Prompt:**")
                                st.text_area(
                                    "Prompt",
                                    value=result.get("full_prompt", ""),
                                    height=200,
                                    disabled=True
                                )
                                
                                if result.get("chat_history"):
                                    st.markdown("**Chat History:**")
                                    st.json(result["chat_history"])
                            
                            # Download option
                            st.markdown("---")
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                download_data = {
                                    "question": question,
                                    "answer": result["answer"],
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "project_id": project_id,
                                    "full_prompt": result.get("full_prompt", ""),
                                    "chat_history": result.get("chat_history", [])
                                }
                                
                                st.download_button(
                                    label="💾 Download Q&A as JSON",
                                    data=json.dumps(download_data, indent=2),
                                    file_name=f"qa_{int(time.time())}.json",
                                    mime="application/json",
                                    use_container_width=True
                                )
                        else:
                            show_error_message("Failed to get answer")
                            st.json(result)
                            
                    except Exception as e:
                        show_error_message(f"Query failed: {str(e)}")
    
    # ========================================================================
    # TAB 2: SEARCH DOCUMENTS
    # ========================================================================
    with tab2:
        st.markdown("### 🔍 Semantic Document Search")
        
        show_info_box(
            "Search through your indexed documents using semantic search. "
            "Find relevant content based on meaning, not just keywords."
        )
        
        # Search input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Search Query",
                placeholder="e.g., information about payment methods",
                help="Enter your search query"
            )
        
        with col2:
            search_limit = st.slider(
                "Results",
                min_value=1,
                max_value=20,
                value=5,
                help="Maximum number of search results to return"
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            search_button = st.button(
                "🔍 Search",
                use_container_width=True,
                type="primary"
            )
        
        if search_button:
            if not search_query.strip():
                st.warning("⚠️ Please enter a search query!")
            else:
                with st.spinner("🔍 Searching documents..."):
                    try:
                        search_req = SearchRequest(text=search_query, limit=search_limit)
                        result = search_index(project_id, search_req)
                        
                        if "results" in result:
                            results = result.get("results", [])
                            
                            if not results:
                                st.info("ℹ️ No results found for your query.")
                            else:
                                st.markdown("---")
                                st.markdown(f"### 📊 Search Results ({len(results)} found)")
                                
                                show_success_message(f"Found {len(results)} relevant results!", show_balloons=False)
                                
                                # Display results
                                for i, res in enumerate(results, 1):
                                    score = res.get('score', 0)
                                    text = res.get('chunk_text', '')
                                    metadata = res.get('chunk_metadata', {})
                                    
                                    # Color code based on relevance
                                    if score > 0.8:
                                        border_color = "#28a745"  # Green
                                    elif score > 0.6:
                                        border_color = "#ffc107"  # Yellow
                                    else:
                                        border_color = "#6c757d"  # Gray
                                    
                                    with st.expander(
                                        f"📝 Result {i} - Relevance: {score:.4f}",
                                        expanded=(i == 1)
                                    ):
                                        st.markdown(f"""
                                        <div style='border-left: 4px solid {border_color}; padding-left: 15px;'>
                                        """, unsafe_allow_html=True)
                                        
                                        st.markdown("**Content:**")
                                        st.write(text)
                                        
                                        if metadata:
                                            st.markdown("---")
                                            st.markdown("**Metadata:**")
                                            st.json(metadata)
                                        
                                        st.markdown("</div>", unsafe_allow_html=True)
                                
                                # Export results
                                st.markdown("---")
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    export_data = {
                                        "query": search_query,
                                        "total_results": len(results),
                                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "project_id": project_id,
                                        "results": results
                                    }
                                    
                                    st.download_button(
                                        label="💾 Export Results as JSON",
                                        data=json.dumps(export_data, indent=2),
                                        file_name=f"search_results_{int(time.time())}.json",
                                        mime="application/json",
                                        use_container_width=True
                                    )
                        else:
                            show_error_message("Search failed")
                            st.json(result)
                            
                    except Exception as e:
                        show_error_message(f"Search failed: {str(e)}")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="Mini RAG System - e& Egypt",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #E31B6D;
            --secondary-color: #0a0e27;
            --accent-color: #00D9C0;
        }
        
        /* Enhanced button styling */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(227, 27, 109, 0.3);
        }
        
        /* Form styling */
        .stForm {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #f8f9fa;
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 600;
        }
        
        /* Card styling */
        .element-container {
            margin-bottom: 10px;
        }
        
        /* Success/Error message styling */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
            padding: 15px;
            font-weight: 500;
        }
        
        /* File uploader styling */
        .uploadedFile {
            border-radius: 8px;
            background: #f8f9fa;
            padding: 10px;
        }
        
        /* Chat message styling */
        .stChatMessage {
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    st.markdown("---")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        page = st.radio(
            "Select Page",
            ["📤 Upload & Process", "💬 Search & Query"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Project ID input
        st.markdown("### ⚙️ Configuration")
        project_id = st.number_input(
            "Project ID",
            min_value=1,
            value=1,
            help="Enter your project ID"
        )
        
        st.markdown("---")
        
        # API Status
        st.markdown("### 🔗 API Status")
        if st.button("Test Connection", use_container_width=True):
            with st.spinner("Testing..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/api/v1/", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Connected!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection Failed: {str(e)}")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Session Info")
        st.markdown(f"**Current Project:** `{project_id}`")
        st.markdown(f"**API:** `{API_BASE_URL}`")
        
        if 'qa_history' in st.session_state:
            st.markdown(f"**Q&A History:** {len(st.session_state.qa_history)} queries")
        
        if 'last_file_id' in st.session_state:
            st.markdown(f"**Last File ID:** `{st.session_state.last_file_id}`")
        
        st.markdown("---")
        
        # Help section
        with st.expander("❓ Help & Tips"):
            st.markdown("""
            **Quick Guide:**
            
            1️⃣ Upload files (PDF/TXT)
            2️⃣ Process & chunk them
            3️⃣ Auto-indexing to vector DB
            4️⃣ Search or ask questions
            
            **Tips:**
            - Use specific questions
            - Adjust context docs
            - Try different chunk sizes
            - Export results as JSON
            """)
    
    # Main content area
    if page == "📤 Upload & Process":
        render_upload_process_page(project_id)
    elif page == "💬 Search & Query":
        render_search_query_page(project_id)
    
    # Render footer
    render_footer()

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
