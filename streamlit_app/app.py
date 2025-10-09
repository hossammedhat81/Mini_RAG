"""
Mini RAG System - Professional Streamlit Interface
e& Egypt - Digital Solutions
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path

# Add components to path
sys.path.append(str(Path(__file__).parent))

# Import page modules
from pages import home, upload_process, query_interface, settings_page, about
from utils import api_client, check_api_health, ui_components
from config import app_config

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Mini RAG System | e& Egypt",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.e-and.com',
        'Report a bug': None,
        'About': "Mini RAG System - Powered by e& Egypt"
    }
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

ui_components.apply_custom_css()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize session state variables"""
    if 'project_id' not in st.session_state:
        st.session_state.project_id = 1
    
    if 'api_base_url' not in st.session_state:
        st.session_state.api_base_url = app_config.API_BASE_URL
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = None
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'index_info' not in st.session_state:
        st.session_state.index_info = None

initialize_session_state()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Header with logo and title
    ui_components.render_header()
    
    # Sidebar navigation
    with st.sidebar:
        try:
            st.image("assets/e_and_egypt_logo.png", width=200)
        except:
            # Fallback if logo not found
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, 
                        {app_config.SECONDARY_COLOR} 0%, {app_config.PRIMARY_COLOR} 100%); 
                        border-radius: 10px; margin-bottom: 1rem;'>
                <h1 style='color: white; font-size: 2.5rem; margin: 0;'>e&</h1>
                <p style='color: white; font-size: 1rem; margin: 0;'>Egypt</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
        
        selected_page = option_menu(
            menu_title="Navigation",
            options=["Home", "Upload & Process", "Query Interface", "Settings", "About"],
            icons=["house-fill", "cloud-upload-fill", "search", "gear-fill", "info-circle-fill"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#0a0e27"},
                "icon": {"color": "#E31B6D", "font-size": "18px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#1c2445",
                },
                "nav-link-selected": {"background-color": "#E31B6D"},
            }
        )
        
        st.markdown("---")
        
        # Project selector in sidebar
        st.markdown("### 🗂️ Project Configuration")
        project_id = st.number_input(
            "Project ID",
            min_value=1,
            value=st.session_state.project_id,
            step=1,
            help="Select or create a project by entering its ID"
        )
        
        if project_id != st.session_state.project_id:
            st.session_state.project_id = project_id
            st.rerun()
        
        # Display current project info
        st.info(f"📌 Active Project: **{st.session_state.project_id}**")
        
        # System status indicator
        st.markdown("---")
        st.markdown("### 🔌 System Status")
        
        # Check API connectivity
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
    
    # Route to selected page
    if selected_page == "Home":
        home.render()
    elif selected_page == "Upload & Process":
        upload_process.render()
    elif selected_page == "Query Interface":
        query_interface.render()
    elif selected_page == "Settings":
        settings_page.render()
    elif selected_page == "About":
        about.render()
    
    # Footer
    ui_components.render_footer()

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
