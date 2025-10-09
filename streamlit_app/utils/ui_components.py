"""
UI Components Module
Reusable UI components for the Streamlit app
"""

import streamlit as st
from config import app_config
from typing import Optional, List, Dict, Any
import base64
from pathlib import Path


def apply_custom_css():
    """Apply custom CSS styling to the app"""
    
    css = f"""
    <style>
        /* Main color scheme */
        :root {{
            --primary-color: {app_config.PRIMARY_COLOR};
            --secondary-color: {app_config.SECONDARY_COLOR};
            --accent-color: {app_config.ACCENT_COLOR};
            --background-color: {app_config.BACKGROUND_COLOR};
            --text-color: {app_config.TEXT_COLOR};
        }}
        
        /* Main app container */
        .main {{
            background-color: var(--background-color);
        }}
        
        /* Header styling */
        .app-header {{
            background: linear-gradient(135deg, {app_config.SECONDARY_COLOR} 0%, {app_config.PRIMARY_COLOR} 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .app-header h1 {{
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }}
        
        .app-header p {{
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }}
        
        /* Card styling */
        .custom-card {{
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }}
        
        /* Success message */
        .success-message {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* Error message */
        .error-message {{
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* Info message */
        .info-message {{
            background-color: #d1ecf1;
            border-left: 4px solid #0c5460;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* Button styling */
        .stButton>button {{
            background: linear-gradient(135deg, {app_config.PRIMARY_COLOR} 0%, #C0134F 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(227, 27, 109, 0.3);
        }}
        
        /* File uploader */
        .uploadedFile {{
            border: 2px dashed {app_config.PRIMARY_COLOR};
            border-radius: 10px;
            padding: 1rem;
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            color: {app_config.PRIMARY_COLOR};
        }}
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {app_config.SECONDARY_COLOR};
        }}
        
        section[data-testid="stSidebar"] .stMarkdown {{
            color: white;
        }}
        
        /* Footer */
        .app-footer {{
            text-align: center;
            padding: 2rem;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
            margin-top: 3rem;
        }}
        
        /* Progress bar */
        .stProgress > div > div > div > div {{
            background-color: {app_config.PRIMARY_COLOR};
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: #f8f9fa;
            border-radius: 5px;
            font-weight: 600;
        }}
        
        /* Chat message */
        .chat-message {{
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            display: flex;
            align-items: flex-start;
        }}
        
        .chat-message.user {{
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }}
        
        .chat-message.assistant {{
            background-color: #f3e5f5;
            border-left: 4px solid {app_config.PRIMARY_COLOR};
        }}
        
        .chat-message .icon {{
            font-size: 1.5rem;
            margin-right: 1rem;
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            padding: 0 2rem;
            background-color: white;
            border-radius: 10px 10px 0 0;
            font-weight: 600;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {app_config.PRIMARY_COLOR};
            color: white;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def render_header():
    """Render the application header"""
    header_html = f"""
    <div class="app-header">
        <h1>🤖 {app_config.APP_TITLE}</h1>
        <p>Powered by {app_config.COMPANY_NAME} | {app_config.APP_VERSION}</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_footer():
    """Render the application footer"""
    footer_html = f"""
    <div class="app-footer">
        <p>© 2025 {app_config.COMPANY_NAME}. All rights reserved.</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">
            Mini RAG System {app_config.APP_VERSION} | Built with ❤️ using Streamlit & FastAPI
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, icon: str = "📊", delta: Optional[str] = None):
    """
    Render a metric card
    
    Args:
        title: Metric title
        value: Metric value
        icon: Icon emoji
        delta: Optional delta value
    """
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
    with col2:
        st.metric(label=title, value=value, delta=delta)


def render_info_card(title: str, content: str, icon: str = "ℹ️"):
    """
    Render an info card
    
    Args:
        title: Card title
        content: Card content
        icon: Icon emoji
    """
    card_html = f"""
    <div class="custom-card">
        <h3>{icon} {title}</h3>
        <p>{content}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_chat_message(role: str, content: str):
    """
    Render a chat message
    
    Args:
        role: Message role (user or assistant)
        content: Message content
    """
    icon = "👤" if role == "user" else "🤖"
    message_class = "user" if role == "user" else "assistant"
    
    message_html = f"""
    <div class="chat-message {message_class}">
        <div class="icon">{icon}</div>
        <div class="content">{content}</div>
    </div>
    """
    st.markdown(message_html, unsafe_allow_html=True)


def render_file_info(filename: str, filesize: float, filetype: str):
    """
    Render file information
    
    Args:
        filename: File name
        filesize: File size in KB
        filetype: File type
    """
    info_html = f"""
    <div class="custom-card">
        <h4>📄 {filename}</h4>
        <p><strong>Size:</strong> {filesize:.2f} KB</p>
        <p><strong>Type:</strong> {filetype}</p>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)


def render_search_result(result: Dict[str, Any], index: int):
    """
    Render a search result
    
    Args:
        result: Result dictionary
        index: Result index
    """
    score = result.get('score', 0)
    text = result.get('chunk_text', '')
    metadata = result.get('chunk_metadata', {})
    
    with st.expander(f"📝 Result {index} - Score: {score:.4f}"):
        st.markdown(f"**Text:**")
        st.write(text)
        
        if metadata:
            st.markdown(f"**Metadata:**")
            st.json(metadata)


def show_loading(message: str = "Processing..."):
    """
    Show loading spinner with message
    
    Args:
        message: Loading message
    """
    return st.spinner(message)


def show_success(message: str):
    """Show success message"""
    st.success(f"✅ {message}")


def show_error(message: str):
    """Show error message"""
    st.error(f"❌ {message}")


def show_warning(message: str):
    """Show warning message"""
    st.warning(f"⚠️ {message}")


def show_info(message: str):
    """Show info message"""
    st.info(f"ℹ️ {message}")


def create_download_button(data: str, filename: str, label: str = "Download"):
    """
    Create a download button
    
    Args:
        data: Data to download
        filename: File name
        label: Button label
    """
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime="text/plain"
    )
