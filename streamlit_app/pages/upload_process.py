"""
Upload & Process Page
Handles file upload and document processing
"""

import streamlit as st
from config import app_config
from utils import api_client, ui_components


def render():
    """Render the upload & process page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>📤 Upload & Process Documents</h1>
    <p style='font-size: 1.1rem; color: #6c757d;'>
        Upload your documents and process them for intelligent search and retrieval
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    project_id = st.session_state.project_id
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["📁 Upload Files", "⚙️ Process Documents"])
    
    # ========================================================================
    # TAB 1: UPLOAD FILES
    # ========================================================================
    with tab1:
        st.markdown("### Upload Your Documents")
        
        ui_components.show_info(
            "Upload PDF or text files to add them to your knowledge base. "
            f"Maximum file size: {app_config.MAX_FILE_SIZE_MB} MB"
        )
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=app_config.ALLOWED_FILE_TYPES,
            help=f"Supported formats: {', '.join(app_config.ALLOWED_FILE_TYPES)}"
        )
        
        if uploaded_file is not None:
            # Display file information
            file_size_kb = uploaded_file.size / 1024
            
            st.markdown("#### 📋 File Information")
            ui_components.render_file_info(
                filename=uploaded_file.name,
                filesize=file_size_kb,
                filetype=uploaded_file.type
            )
            
            # Check file size
            if file_size_kb > app_config.MAX_FILE_SIZE_MB * 1024:
                ui_components.show_error(
                    f"File is too large! Maximum size is {app_config.MAX_FILE_SIZE_MB} MB"
                )
            else:
                # Upload button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Upload File", use_container_width=True):
                        with ui_components.show_loading("Uploading file..."):
                            result = api_client.upload_file(
                                project_id=project_id,
                                file=uploaded_file,
                                filename=uploaded_file.name
                            )
                        
                        if "error" in result:
                            ui_components.show_error(f"Upload failed: {result['error']}")
                        else:
                            file_id = result.get('file_id', 'N/A')
                            ui_components.show_success(
                                f"File uploaded successfully! File ID: {file_id}"
                            )
                            st.balloons()
                            
                            # Store in session state
                            if 'uploaded_files' not in st.session_state:
                                st.session_state.uploaded_files = []
                            st.session_state.uploaded_files.append({
                                'filename': uploaded_file.name,
                                'file_id': file_id,
                                'project_id': project_id
                            })
        
        # Show uploaded files for this project
        if st.session_state.get('uploaded_files'):
            st.markdown("---")
            st.markdown("### 📚 Uploaded Files in This Session")
            
            project_files = [
                f for f in st.session_state.uploaded_files 
                if f['project_id'] == project_id
            ]
            
            if project_files:
                for file_info in project_files:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"📄 **{file_info['filename']}**")
                    with col2:
                        st.code(file_info['file_id'], language=None)
            else:
                ui_components.show_info("No files uploaded for this project yet.")
    
    # ========================================================================
    # TAB 2: PROCESS DOCUMENTS
    # ========================================================================
    with tab2:
        st.markdown("### Process Your Documents")
        
        ui_components.show_info(
            "Configure processing parameters and process your uploaded documents. "
            "This will chunk your documents and prepare them for indexing."
        )
        
        # Processing form
        with st.form("process_form", clear_on_submit=False):
            st.markdown("#### ⚙️ Processing Configuration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                chunk_size = st.number_input(
                    "Chunk Size (characters)",
                    min_value=app_config.CHUNK_SIZE_MIN,
                    max_value=app_config.CHUNK_SIZE_MAX,
                    value=app_config.CHUNK_SIZE_DEFAULT,
                    step=100,
                    help="Size of text chunks in characters. Larger chunks preserve more context."
                )
            
            with col2:
                overlap_size = st.number_input(
                    "Overlap Size (characters)",
                    min_value=app_config.OVERLAP_SIZE_MIN,
                    max_value=app_config.OVERLAP_SIZE_MAX,
                    value=app_config.OVERLAP_SIZE_DEFAULT,
                    step=50,
                    help="Number of overlapping characters between chunks. Helps maintain context."
                )
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                do_reset = st.checkbox(
                    "🔄 Reset Existing Chunks",
                    value=False,
                    help="Delete all existing chunks before processing"
                )
            
            with col2:
                file_id = st.text_input(
                    "Specific File ID (optional)",
                    value="",
                    help="Leave empty to process all files, or enter a specific file ID"
                )
            
            st.markdown("---")
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button(
                    "⚡ Process Documents",
                    use_container_width=True
                )
            
        # Handle form submission OUTSIDE the form context
        if submitted:
            # Process documents
            st.markdown("### 🔄 Processing Status")
            
            with ui_components.show_loading("Processing documents... This may take a while."):
                result = api_client.process_documents(
                    project_id=project_id,
                    chunk_size=chunk_size,
                    overlap_size=overlap_size,
                    file_id=file_id if file_id else None,
                    do_reset=1 if do_reset else 0
                )
            
            if "error" in result:
                ui_components.show_error(f"Processing failed: {result['error']}")
            else:
                inserted_chunks = result.get('inserted_chunks', 0)
                processed_files = result.get('processed_files', 0)
                
                ui_components.show_success(
                    f"Processing completed! {processed_files} files processed, "
                    f"{inserted_chunks} chunks created."
                )
                
                st.session_state.processing_status = {
                    'chunks': inserted_chunks,
                    'files': processed_files
                }
                
                # Set flag to show index button
                st.session_state.ready_to_index = True
                st.rerun()  # Rerun to exit form context
        
    # Show index button OUTSIDE tab2 context if processing completed
    if st.session_state.get('ready_to_index', False):
        st.markdown("---")
        st.markdown("### 🔄 Next Step: Index Documents")
        st.info("💡 Documents are processed. Click below to build the vector index.")
        
        if st.button("🚀 Index Documents Now", use_container_width=True, key="index_button"):
            with ui_components.show_loading("Indexing documents to vector database..."):
                index_result = api_client.push_to_index(
                    project_id=project_id,
                    do_reset=0  # Don't reset when auto-indexing
                )
            
            if "error" in index_result:
                ui_components.show_error(f"Indexing failed: {index_result['error']}")
            else:
                indexed_count = index_result.get('inserted_items_count', 0)
                ui_components.show_success(
                    f"✅ Indexing completed! {indexed_count} items indexed."
                )
                st.balloons()
                # Clear the flag after successful indexing
                st.session_state.ready_to_index = False
                st.rerun()
    
    # Show processing stats if available (moved outside tab context)
    if st.session_state.get('processing_status'):
        st.markdown("---")
        st.markdown("### 📊 Latest Processing Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ui_components.render_metric_card(
                title="Files Processed",
                value=str(st.session_state.processing_status['files']),
                icon="📄"
            )
        
        with col2:
            ui_components.render_metric_card(
                title="Chunks Created",
                value=str(st.session_state.processing_status['chunks']),
                icon="📦"
            )
    
    st.markdown("---")
    
    # Help section
    with st.expander("❓ Need Help?"):
        st.markdown("""
        ### Understanding Document Processing
        
        **Chunk Size:**
        - Determines how much text is in each chunk
        - Recommended: 1000-2000 characters for most documents
        - Smaller chunks = more precise search, but less context
        - Larger chunks = more context, but less precise search
        
        **Overlap Size:**
        - Number of characters that overlap between chunks
        - Helps maintain context across chunk boundaries
        - Recommended: 10-20% of chunk size
        
        **Reset Existing Chunks:**
        - Check this if you want to reprocess all documents from scratch
        - Unchecked = append new chunks to existing ones
        
        **Specific File ID:**
        - Leave empty to process all uploaded files
        - Enter a file ID to process only that specific file
        """)
