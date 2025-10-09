"""
Home Page
Welcome page with system overview and quick stats
"""

import streamlit as st
from config import app_config
from utils import api_client, ui_components


def render():
    """Render the home page"""
    
    # Welcome section
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: {app_config.PRIMARY_COLOR}; font-size: 3rem;'>
            Welcome to Mini RAG System
        </h1>
        <p style='font-size: 1.2rem; color: #6c757d; margin-top: 1rem;'>
            Intelligent Document Retrieval & Question Answering Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick info cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ui_components.render_info_card(
            title="📤 Upload Documents",
            content="Upload PDF and text files to build your knowledge base",
            icon="📄"
        )
    
    with col2:
        ui_components.render_info_card(
            title="🔍 Smart Search",
            content="Search through your documents using semantic search",
            icon="🎯"
        )
    
    with col3:
        ui_components.render_info_card(
            title="💬 AI Answers",
            content="Get intelligent answers powered by advanced LLMs",
            icon="🤖"
        )
    
    st.markdown("---")
    
    # Current project stats
    st.markdown("## 📊 Current Project Overview")
    
    project_id = st.session_state.project_id
    
    # Fetch index info
    with ui_components.show_loading("Fetching project information..."):
        result = api_client.get_index_info(project_id)
    
    if "error" not in result and "collection_info" in result:
        collection_info = result.get("collection_info", {})
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ui_components.render_metric_card(
                title="Project ID",
                value=str(project_id),
                icon="🗂️"
            )
        
        with col2:
            points_count = collection_info.get("points_count", 0)
            ui_components.render_metric_card(
                title="Indexed Chunks",
                value=str(points_count),
                icon="📚"
            )
        
        with col3:
            vectors_count = collection_info.get("vectors_count", 0)
            ui_components.render_metric_card(
                title="Vectors",
                value=str(vectors_count),
                icon="🔢"
            )
        
        with col4:
            status = collection_info.get("status", "N/A")
            ui_components.render_metric_card(
                title="Status",
                value=status,
                icon="✅"
            )
        
        # Detailed info
        with st.expander("📋 View Detailed Information"):
            st.json(collection_info)
    
    else:
        ui_components.show_warning(
            "No index found for this project. Please upload and process documents first."
        )
    
    st.markdown("---")
    
    # Getting started guide
    st.markdown("## 🚀 Getting Started")
    
    with st.expander("📖 Quick Start Guide", expanded=False):
        st.markdown("""
        ### Follow these steps to get started:
        
        1. **Select a Project** 
           - Use the sidebar to select or create a new project by entering a Project ID
        
        2. **Upload Documents** 📤
           - Navigate to "Upload & Process" page
           - Upload your PDF or text files
           - Configure chunking parameters
           - Process the documents
        
        3. **Index Documents** 🔄
           - Documents are automatically indexed after processing
           - Vector embeddings are created for semantic search
        
        4. **Ask Questions** 💬
           - Go to "Query Interface" page
           - Type your question
           - Get AI-powered answers based on your documents
        
        ### Tips for Best Results:
        - Use clear, specific questions
        - Keep document chunks at reasonable sizes (1000-2000 characters)
        - Use appropriate overlap for better context (200-300 characters)
        - Multiple related documents improve answer quality
        """)
    
    # System information
    st.markdown("---")
    st.markdown("## ⚙️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Supported File Types:**
        - 📄 PDF Documents
        - 📝 Text Files (.txt)
        
        **Maximum File Size:**
        - 10 MB per file
        """)
    
    with col2:
        st.markdown("""
        **Processing Features:**
        - Automatic text extraction
        - Intelligent chunking
        - Vector embedding generation
        - Semantic search indexing
        """)
    
    # Recent activity (if available)
    if st.session_state.get('chat_history'):
        st.markdown("---")
        st.markdown("## 💬 Recent Questions")
        
        recent_questions = st.session_state.chat_history[-5:]  # Last 5 questions
        for i, qa in enumerate(reversed(recent_questions), 1):
            with st.expander(f"Q{i}: {qa.get('question', '')[:100]}..."):
                st.markdown(f"**Question:** {qa.get('question', '')}")
                st.markdown(f"**Answer:** {qa.get('answer', '')}")
