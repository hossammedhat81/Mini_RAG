"""
About Page
Information about the application and company
"""

import streamlit as st
from config import app_config
from utils import ui_components


def render():
    """Render the about page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>ℹ️ About Mini RAG System</h1>
    <p style='font-size: 1.1rem; color: #6c757d;'>
        Learn more about our intelligent document retrieval system
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Company logo and branding
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("assets/e_and_egypt_logo.png", width=300)
        except:
            st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, 
                        {app_config.SECONDARY_COLOR} 0%, {app_config.PRIMARY_COLOR} 100%); 
                        border-radius: 10px;'>
                <h1 style='color: white; font-size: 4rem; margin: 0;'>e&</h1>
                <p style='color: white; font-size: 1.5rem; margin: 0.5rem 0 0 0;'>Egypt</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content
    st.markdown(app_config.ABOUT_MESSAGE)
    
    st.markdown("---")
    
    # Features showcase
    st.markdown("## 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        features_1 = [
            ("📤", "Easy Document Upload", "Upload PDF and text files seamlessly"),
            ("🔄", "Intelligent Processing", "Automatic text extraction and chunking"),
            ("🎯", "Semantic Search", "Find information based on meaning, not just keywords"),
            ("💬", "AI-Powered Q&A", "Get accurate answers from your documents")
        ]
        
        for icon, title, description in features_1:
            st.markdown(f"""
            <div class="custom-card">
                <h3>{icon} {title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        features_2 = [
            ("🗂️", "Multi-Project Support", "Manage multiple document collections"),
            ("⚡", "Fast Processing", "Quick document processing and indexing"),
            ("📊", "Real-time Analytics", "Monitor system status and usage"),
            ("🔒", "Secure & Reliable", "Enterprise-grade security and reliability")
        ]
        
        for icon, title, description in features_2:
            st.markdown(f"""
            <div class="custom-card">
                <h3>{icon} {title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technology stack
    st.markdown("## 🛠️ Technology Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Backend
        - **FastAPI** - Modern async API framework
        - **PostgreSQL** - Relational database
        - **Qdrant** - Vector database
        - **SQLAlchemy** - ORM
        """)
    
    with col2:
        st.markdown("""
        ### AI & ML
        - **OpenAI GPT** - Text generation
        - **Cohere** - Embeddings
        - **LangChain** - RAG framework
        - **Vector Search** - Semantic retrieval
        """)
    
    with col3:
        st.markdown("""
        ### Frontend
        - **Streamlit** - Interactive UI
        - **Python** - Core language
        - **Custom CSS** - Styled components
        - **Responsive Design** - Mobile-friendly
        """)
    
    st.markdown("---")
    
    # Use cases
    st.markdown("## 📚 Use Cases")
    
    use_cases = [
        {
            "title": "📖 Research & Knowledge Management",
            "description": "Organize and query research papers, articles, and academic documents efficiently.",
            "benefits": ["Quick information retrieval", "Citation finding", "Topic exploration"]
        },
        {
            "title": "📄 Document Analysis",
            "description": "Analyze contracts, reports, and business documents with AI assistance.",
            "benefits": ["Key point extraction", "Summary generation", "Compliance checking"]
        },
        {
            "title": "💼 Customer Support",
            "description": "Build internal knowledge bases for customer support teams.",
            "benefits": ["Instant answer lookup", "Consistent responses", "Training material"]
        },
        {
            "title": "📚 Educational Content",
            "description": "Create interactive learning materials and Q&A systems.",
            "benefits": ["Student assistance", "Content discovery", "Study aids"]
        }
    ]
    
    for use_case in use_cases:
        with st.expander(use_case["title"]):
            st.markdown(f"**{use_case['description']}**")
            st.markdown("**Benefits:**")
            for benefit in use_case["benefits"]:
                st.markdown(f"- {benefit}")
    
    st.markdown("---")
    
    # Architecture diagram (text-based)
    st.markdown("## 🏗️ System Architecture")
    
    architecture_diagram = """
    ```
    ┌─────────────────────────────────────────────────────────────┐
    │                     User Interface (Streamlit)               │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
    │  │  Upload  │  │ Process  │  │  Search  │  │   Q&A    │   │
    │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
    └────────────────────────────┬────────────────────────────────┘
                                 │ REST API
    ┌────────────────────────────┴────────────────────────────────┐
    │                    FastAPI Backend                           │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
    │  │    Routes    │  │ Controllers  │  │    Models    │     │
    │  └──────────────┘  └──────────────┘  └──────────────┘     │
    └───┬────────────┬────────────┬────────────┬──────────────────┘
        │            │            │            │
    ┌───┴───┐    ┌───┴───┐    ┌───┴────┐   ┌──┴──────┐
    │ Files │    │  LLM  │    │ Vector │   │  PostgreSQL│
    │Storage│    │ APIs  │    │   DB   │   │  Database │
    └───────┘    └───────┘    └────────┘   └───────────┘
                  (OpenAI,     (Qdrant)
                   Cohere)
    ```
    """
    
    st.code(architecture_diagram, language=None)
    
    st.markdown("---")
    
    # Metrics and stats
    st.markdown("## 📊 System Capabilities")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ui_components.render_metric_card(
            title="Supported Files",
            value="PDF, TXT",
            icon="📄"
        )
    
    with col2:
        ui_components.render_metric_card(
            title="Max File Size",
            value=f"{app_config.MAX_FILE_SIZE_MB} MB",
            icon="💾"
        )
    
    with col3:
        ui_components.render_metric_card(
            title="Languages",
            value="Multi",
            icon="🌍"
        )
    
    with col4:
        ui_components.render_metric_card(
            title="API Response",
            value="< 2s",
            icon="⚡"
        )
    
    st.markdown("---")
    
    # Contact and support
    st.markdown("## 📞 Support & Contact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏢 Company Information
        **e& Egypt**  
        Digital Solutions Provider  
        
        Empowering digital transformation through innovative technology solutions.
        """)
    
    with col2:
        st.markdown("""
        ### 📧 Get in Touch
        - **Website:** [www.e-and.com](https://www.e-and.com)
        - **Support:** Contact your system administrator
        - **Documentation:** Available in the Help section
        """)
    
    st.markdown("---")
    
    # Version history
    with st.expander("📝 Version History"):
        st.markdown("""
        ### Version 3.0 (Current)
        - Complete UI redesign with modern interface
        - Enhanced chat history and search functionality
        - Improved error handling and user feedback
        - Advanced settings and configuration options
        - Better mobile responsiveness
        
        ### Version 2.0
        - Added multi-project support
        - Improved document processing
        - Enhanced vector search capabilities
        
        ### Version 1.0
        - Initial release
        - Basic upload and Q&A functionality
        - PDF and TXT support
        """)
    
    st.markdown("---")
    
    # Footer credits
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background-color: {app_config.BACKGROUND_COLOR}; 
                border-radius: 10px; margin-top: 2rem;'>
        <h3 style='color: {app_config.PRIMARY_COLOR};'>Mini RAG System {app_config.APP_VERSION}</h3>
        <p style='color: #6c757d; margin-top: 1rem;'>
            Developed with ❤️ by {app_config.COMPANY_NAME}
        </p>
        <p style='color: #6c757d; font-size: 0.9rem;'>
            © 2025 All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)
