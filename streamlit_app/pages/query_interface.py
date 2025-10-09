"""
Query Interface Page
Handles document search and Q&A functionality
"""

import streamlit as st
from config import app_config
from utils import api_client, ui_components
from datetime import datetime


def render():
    """Render the query interface page"""
    
    st.markdown(f"""
    <h1 style='color: {app_config.PRIMARY_COLOR};'>💬 Query Interface</h1>
    <p style='font-size: 1.1rem; color: #6c757d;'>
        Ask questions and search through your documents using AI-powered retrieval
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    project_id = st.session_state.project_id
    
    # Create tabs for different query modes
    tab1, tab2, tab3 = st.tabs(["🤖 Ask Questions", "🔍 Search Documents", "💬 Chat History"])
    
    # ========================================================================
    # TAB 1: ASK QUESTIONS (RAG)
    # ========================================================================
    with tab1:
        st.markdown("### Ask Your Questions")
        
        ui_components.show_info(
            "Ask questions about your documents. The AI will search through your "
            "knowledge base and provide contextual answers."
        )
        
        # Question input
        question = st.text_area(
            "Your Question",
            height=100,
            placeholder="e.g., What are the main points discussed in the document?",
            help="Type your question here. Be as specific as possible for better results."
        )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                num_results = st.slider(
                    "Number of context documents",
                    min_value=app_config.SEARCH_LIMIT_MIN,
                    max_value=app_config.SEARCH_LIMIT_MAX,
                    value=app_config.SEARCH_LIMIT_DEFAULT,
                    help="Number of relevant documents to retrieve for context"
                )
            
            with col2:
                show_context = st.checkbox(
                    "Show retrieved context",
                    value=False,
                    help="Display the documents used to generate the answer"
                )
        
        # Ask button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            ask_button = st.button("🚀 Get Answer", use_container_width=True)
        
        if ask_button:
            if not question.strip():
                ui_components.show_warning("Please enter a question!")
            else:
                # Show loading
                with ui_components.show_loading("🤔 Thinking... Generating answer..."):
                    result = api_client.ask_question(
                        project_id=project_id,
                        question=question,
                        limit=num_results
                    )
                
                if "error" in result:
                    ui_components.show_error(f"Failed to get answer: {result['error']}")
                elif "answer" in result:
                    answer = result.get("answer", "")
                    full_prompt = result.get("full_prompt", "")
                    chat_history = result.get("chat_history", [])
                    
                    # Display answer
                    st.markdown("---")
                    st.markdown("### 🎯 Answer")
                    
                    # Render as chat message
                    ui_components.render_chat_message("user", question)
                    ui_components.render_chat_message("assistant", answer)
                    
                    # Store in chat history
                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    
                    st.session_state.chat_history.append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'question': question,
                        'answer': answer,
                        'project_id': project_id,
                        'full_prompt': full_prompt,
                        'chat_history': chat_history
                    })
                    
                    # Show context if requested
                    if show_context:
                        with st.expander("📄 View Full Context"):
                            st.markdown("**Full Prompt:**")
                            st.text_area("Prompt", value=full_prompt, height=200, disabled=True)
                            
                            if chat_history:
                                st.markdown("**Chat History:**")
                                st.json(chat_history)
                    
                    # Download option
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        download_text = f"""
Question: {question}

Answer: {answer}

Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Project ID: {project_id}
                        """
                        st.download_button(
                            label="💾 Download Q&A",
                            data=download_text,
                            file_name=f"qa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                else:
                    ui_components.show_error("No answer received from the API")
    
    # ========================================================================
    # TAB 2: SEARCH DOCUMENTS
    # ========================================================================
    with tab2:
        st.markdown("### Search Your Documents")
        
        ui_components.show_info(
            "Search through your indexed documents using semantic search. "
            "Find relevant chunks based on meaning, not just keywords."
        )
        
        # Search input
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., information about payment methods",
            help="Enter your search query"
        )
        
        # Search options
        col1, col2 = st.columns(2)
        
        with col1:
            search_limit = st.slider(
                "Number of results",
                min_value=app_config.SEARCH_LIMIT_MIN,
                max_value=app_config.SEARCH_LIMIT_MAX,
                value=app_config.SEARCH_LIMIT_DEFAULT,
                help="Maximum number of search results to return"
            )
        
        with col2:
            show_metadata = st.checkbox(
                "Show metadata",
                value=True,
                help="Display metadata information for each result"
            )
        
        # Search button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            search_button = st.button("🔍 Search", use_container_width=True)
        
        if search_button:
            if not search_query.strip():
                ui_components.show_warning("Please enter a search query!")
            else:
                with ui_components.show_loading("Searching documents..."):
                    result = api_client.search_index(
                        project_id=project_id,
                        query=search_query,
                        limit=search_limit
                    )
                
                if "error" in result:
                    ui_components.show_error(f"Search failed: {result['error']}")
                elif "results" in result:
                    results = result.get("results", [])
                    
                    if not results:
                        ui_components.show_warning("No results found for your query.")
                    else:
                        st.markdown("---")
                        st.markdown(f"### 📊 Search Results ({len(results)} found)")
                        
                        # Display results
                        for i, res in enumerate(results, 1):
                            score = res.get('score', 0)
                            text = res.get('chunk_text', '')
                            metadata = res.get('chunk_metadata', {})
                            
                            with st.expander(f"📝 Result {i} - Relevance Score: {score:.4f}", expanded=(i==1)):
                                st.markdown("**Content:**")
                                st.write(text)
                                
                                if show_metadata and metadata:
                                    st.markdown("---")
                                    st.markdown("**Metadata:**")
                                    st.json(metadata)
                        
                        # Export results option
                        st.markdown("---")
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            export_text = f"Search Query: {search_query}\n\n"
                            export_text += f"Results: {len(results)}\n\n"
                            export_text += "="*50 + "\n\n"
                            
                            for i, res in enumerate(results, 1):
                                export_text += f"Result {i}:\n"
                                export_text += f"Score: {res.get('score', 0):.4f}\n"
                                export_text += f"Text: {res.get('chunk_text', '')}\n"
                                export_text += "\n" + "="*50 + "\n\n"
                            
                            st.download_button(
                                label="💾 Export Results",
                                data=export_text,
                                file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                else:
                    ui_components.show_error("No results received from the API")
    
    # ========================================================================
    # TAB 3: CHAT HISTORY
    # ========================================================================
    with tab3:
        st.markdown("### 💬 Chat History")
        
        if not st.session_state.get('chat_history'):
            ui_components.show_info(
                "No chat history yet. Start asking questions in the 'Ask Questions' tab!"
            )
        else:
            # Filter options
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                filter_project = st.checkbox(
                    "Show only current project",
                    value=True,
                    help="Filter history for current project only"
                )
            
            with col2:
                sort_order = st.selectbox(
                    "Sort order",
                    options=["Newest first", "Oldest first"]
                )
            
            with col3:
                if st.button("🗑️ Clear History"):
                    st.session_state.chat_history = []
                    st.rerun()
            
            st.markdown("---")
            
            # Filter and sort history
            history = st.session_state.chat_history
            
            if filter_project:
                history = [h for h in history if h.get('project_id') == project_id]
            
            if sort_order == "Oldest first":
                history = list(history)
            else:
                history = list(reversed(history))
            
            # Display history
            if not history:
                ui_components.show_info("No chat history for current filters.")
            else:
                st.markdown(f"**Total Conversations: {len(history)}**")
                st.markdown("---")
                
                for i, qa in enumerate(history, 1):
                    timestamp = qa.get('timestamp', 'N/A')
                    question = qa.get('question', '')
                    answer = qa.get('answer', '')
                    qa_project_id = qa.get('project_id', 'N/A')
                    
                    with st.expander(f"💬 Conversation {i} - {timestamp} (Project: {qa_project_id})"):
                        ui_components.render_chat_message("user", question)
                        ui_components.render_chat_message("assistant", answer)
                        
                        # Show full details button
                        if st.button(f"View Details", key=f"details_{i}"):
                            st.markdown("---")
                            st.markdown("**Full Context:**")
                            st.json({
                                'timestamp': timestamp,
                                'project_id': qa_project_id,
                                'full_prompt': qa.get('full_prompt', ''),
                                'chat_history': qa.get('chat_history', [])
                            })
    
    st.markdown("---")
    
    # Help section
    with st.expander("❓ Tips for Better Results"):
        st.markdown("""
        ### Getting the Best Answers
        
        **Ask Clear Questions:**
        - Be specific and clear in your questions
        - Include relevant context if needed
        - Avoid ambiguous or overly broad questions
        
        **Search Effectively:**
        - Use natural language in your queries
        - Try different phrasings if you don't get good results
        - Semantic search works on meaning, not just keywords
        
        **Adjust Parameters:**
        - Increase context documents for complex questions
        - Use fewer documents for simple, specific queries
        - Check retrieved context if answers seem off-topic
        
        **Best Practices:**
        - Process and index documents before querying
        - Use appropriate chunk sizes during processing
        - Keep your document collection organized
        """)
