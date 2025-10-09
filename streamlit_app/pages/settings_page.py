"""
Settings Page
Configure application settings and preferences
"""

import streamlit as st
from config import app_config
from utils import ui_components


def render():
    """Render the settings page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>⚙️ Settings</h1>
    <p style='font-size: 1.1rem; color: #6c757d;'>
        Configure application settings and preferences
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create tabs for different settings sections
    tab1, tab2, tab3 = st.tabs(["🔌 API Configuration", "📊 Processing Defaults", "🎨 Display Settings"])
    
    # ========================================================================
    # TAB 1: API CONFIGURATION
    # ========================================================================
    with tab1:
        st.markdown("### API Connection Settings")
        
        with st.form("api_settings_form"):
            api_base_url = st.text_input(
                "API Base URL",
                value=st.session_state.get('api_base_url', app_config.API_BASE_URL),
                help="Base URL for the FastAPI backend"
            )
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                test_connection = st.form_submit_button("🔍 Test Connection")
            
            with col2:
                save_settings = st.form_submit_button("💾 Save Settings")
            
            if test_connection:
                with ui_components.show_loading("Testing connection..."):
                    import requests
                    try:
                        response = requests.get(f"{api_base_url}/api/v1/health", timeout=5)
                        if response.status_code == 200:
                            ui_components.show_success("✅ Connection successful!")
                        else:
                            ui_components.show_error(f"❌ Connection failed with status {response.status_code}")
                    except Exception as e:
                        ui_components.show_error(f"❌ Connection failed: {str(e)}")
            
            if save_settings:
                st.session_state.api_base_url = api_base_url
                ui_components.show_success("Settings saved successfully!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Current Configuration")
        
        config_info = {
            "API Base URL": st.session_state.get('api_base_url', app_config.API_BASE_URL),
            "Active Project ID": st.session_state.get('project_id', 1),
        }
        
        for key, value in config_info.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{key}:**")
            with col2:
                st.code(value, language=None)
    
    # ========================================================================
    # TAB 2: PROCESSING DEFAULTS
    # ========================================================================
    with tab2:
        st.markdown("### Document Processing Defaults")
        
        ui_components.show_info(
            "Set default values for document processing parameters. "
            "These will be used as initial values in the upload & process page."
        )
        
        with st.form("processing_defaults_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                default_chunk_size = st.number_input(
                    "Default Chunk Size",
                    min_value=app_config.CHUNK_SIZE_MIN,
                    max_value=app_config.CHUNK_SIZE_MAX,
                    value=st.session_state.get('default_chunk_size', app_config.CHUNK_SIZE_DEFAULT),
                    step=100,
                    help="Default size for text chunks"
                )
            
            with col2:
                default_overlap_size = st.number_input(
                    "Default Overlap Size",
                    min_value=app_config.OVERLAP_SIZE_MIN,
                    max_value=app_config.OVERLAP_SIZE_MAX,
                    value=st.session_state.get('default_overlap_size', app_config.OVERLAP_SIZE_DEFAULT),
                    step=50,
                    help="Default overlap between chunks"
                )
            
            st.markdown("---")
            
            default_search_limit = st.slider(
                "Default Search Result Limit",
                min_value=app_config.SEARCH_LIMIT_MIN,
                max_value=app_config.SEARCH_LIMIT_MAX,
                value=st.session_state.get('default_search_limit', app_config.SEARCH_LIMIT_DEFAULT),
                help="Default number of search results to return"
            )
            
            st.markdown("---")
            
            if st.form_submit_button("💾 Save Defaults", use_container_width=True):
                st.session_state.default_chunk_size = default_chunk_size
                st.session_state.default_overlap_size = default_overlap_size
                st.session_state.default_search_limit = default_search_limit
                ui_components.show_success("Default settings saved!")
        
        st.markdown("---")
        st.markdown("### Processing Recommendations")
        
        recommendations = {
            "General Documents": {
                "Chunk Size": "1000-1500",
                "Overlap": "200-300",
                "Use Case": "Most text documents, articles, reports"
            },
            "Technical Documentation": {
                "Chunk Size": "1500-2000",
                "Overlap": "300-400",
                "Use Case": "Code documentation, technical manuals"
            },
            "Short Articles": {
                "Chunk Size": "500-800",
                "Overlap": "100-150",
                "Use Case": "News articles, blog posts"
            },
            "Legal Documents": {
                "Chunk Size": "2000-3000",
                "Overlap": "400-500",
                "Use Case": "Contracts, legal texts requiring full context"
            }
        }
        
        for doc_type, settings in recommendations.items():
            with st.expander(f"📄 {doc_type}"):
                for key, value in settings.items():
                    st.markdown(f"**{key}:** {value}")
    
    # ========================================================================
    # TAB 3: DISPLAY SETTINGS
    # ========================================================================
    with tab3:
        st.markdown("### Display & UI Settings")
        
        with st.form("display_settings_form"):
            show_advanced_options = st.checkbox(
                "Show Advanced Options by Default",
                value=st.session_state.get('show_advanced_options', False),
                help="Display advanced options expanded by default"
            )
            
            show_timestamps = st.checkbox(
                "Show Timestamps in Chat History",
                value=st.session_state.get('show_timestamps', True),
                help="Display timestamps for each conversation"
            )
            
            auto_expand_results = st.checkbox(
                "Auto-expand First Search Result",
                value=st.session_state.get('auto_expand_results', True),
                help="Automatically expand the first result in search"
            )
            
            enable_animations = st.checkbox(
                "Enable Animations",
                value=st.session_state.get('enable_animations', True),
                help="Show balloons and other animations on success"
            )
            
            st.markdown("---")
            
            if st.form_submit_button("💾 Save Display Settings", use_container_width=True):
                st.session_state.show_advanced_options = show_advanced_options
                st.session_state.show_timestamps = show_timestamps
                st.session_state.auto_expand_results = auto_expand_results
                st.session_state.enable_animations = enable_animations
                ui_components.show_success("Display settings saved!")
        
        st.markdown("---")
        st.markdown("### Theme Information")
        
        st.markdown(f"""
        **Current Theme:** {app_config.COMPANY_NAME} Corporate
        
        **Colors:**
        - Primary: {app_config.PRIMARY_COLOR}
        - Secondary: {app_config.SECONDARY_COLOR}
        - Accent: {app_config.ACCENT_COLOR}
        """)
        
        # Color preview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background-color: {app_config.PRIMARY_COLOR}; padding: 2rem; 
                        border-radius: 10px; text-align: center; color: white;'>
                <strong>Primary</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: {app_config.SECONDARY_COLOR}; padding: 2rem; 
                        border-radius: 10px; text-align: center; color: white;'>
                <strong>Secondary</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background-color: {app_config.ACCENT_COLOR}; padding: 2rem; 
                        border-radius: 10px; text-align: center; color: white;'>
                <strong>Accent</strong>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System information
    st.markdown("### 📋 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Application Version:** {app_config.APP_VERSION}  
        **Company:** {app_config.COMPANY_NAME}  
        **Year:** 2025
        """)
    
    with col2:
        st.markdown(f"""
        **Max File Size:** {app_config.MAX_FILE_SIZE_MB} MB  
        **Allowed Types:** {', '.join(app_config.ALLOWED_FILE_TYPES)}  
        **Processing Batch Size:** {app_config.PROCESSING_BATCH_SIZE}
        """)
    
    # Reset settings
    st.markdown("---")
    st.markdown("### 🔄 Reset Settings")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚠️ Reset All Settings to Default", use_container_width=True):
            # Reset to defaults
            st.session_state.api_base_url = app_config.API_BASE_URL
            st.session_state.default_chunk_size = app_config.CHUNK_SIZE_DEFAULT
            st.session_state.default_overlap_size = app_config.OVERLAP_SIZE_DEFAULT
            st.session_state.default_search_limit = app_config.SEARCH_LIMIT_DEFAULT
            st.session_state.show_advanced_options = False
            st.session_state.show_timestamps = True
            st.session_state.auto_expand_results = True
            st.session_state.enable_animations = True
            
            ui_components.show_success("All settings reset to default!")
            st.rerun()
