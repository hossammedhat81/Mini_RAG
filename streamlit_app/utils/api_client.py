"""
API Client Module
Handles all API communication with the FastAPI backend
"""

import requests
import streamlit as st
from typing import Optional, Dict, Any
from io import BytesIO
from config import app_config
import logging

# Configure logging
logger = logging.getLogger(__name__)

class APIClient:
    """API Client for communicating with FastAPI backend"""
    
    def __init__(self):
        self.base_url = st.session_state.get('api_base_url', app_config.API_BASE_URL)
        self._connection_verified = False
    
    def _verify_connection(self) -> bool:
        """
        Verify API connection before making requests.
        This helps provide better error messages for connection issues.
        
        Returns:
            True if connection is healthy, False otherwise
        """
        if self._connection_verified:
            return True
            
        try:
            response = requests.get(
                f"{self.base_url}{app_config.HEALTH_CHECK_ENDPOINT}",
                timeout=app_config.HEALTH_CHECK_TIMEOUT
            )
            if response.status_code == 200:
                self._connection_verified = True
                return True
            else:
                st.warning(f"⚠️ API returned status {response.status_code}. Requests may fail.")
                return False
        except requests.exceptions.ConnectionError:
            st.error(
                f"❌ **Cannot connect to FastAPI backend at `{self.base_url}`**\n\n"
                f"**Troubleshooting:**\n"
                f"1. Make sure the FastAPI backend is running on `{self.base_url}`\n"
                f"2. For local development, use `http://127.0.0.1:8000`\n"
                f"3. For Docker, use `http://fastapi:8000`\n\n"
                f"**Start the backend with:**\n"
                f"```bash\n"
                f"cd src\n"
                f"python main.py\n"
                f"```"
            )
            return False
        except requests.exceptions.Timeout:
            st.error(f"⏱️ Connection timeout to {self.base_url}")
            return False
        except Exception as e:
            st.error(f"❌ Connection check failed: {str(e)}")
            return False
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and return JSON data with detailed error handling
        
        Args:
            response: HTTP response object
            
        Returns:
            Dictionary containing response data or error information
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Try to extract detailed error from API response
            try:
                error_data = response.json()
                signal = error_data.get('signal', 'unknown_error')
                detail = error_data.get('detail', str(e))
                
                # Map common error signals to user-friendly messages
                error_messages = {
                    'rag_answer_error': '❌ Could not generate answer. The index may be empty or documents not indexed.',
                    'project_not_found_error': '❌ Project not found. Please check the project ID.',
                    'file_upload_failed': '❌ File upload failed. Check file format and size.',
                    'processing_failed': '❌ Document processing failed. Check file content.',
                    'vectordb_search_error': '❌ Search failed. The index may not be built yet.',
                    'no_files_error': '❌ No files found to process. Upload files first.',
                    'file_id_error': '❌ Invalid file ID. The file may not exist.',
                }
                
                error_msg = error_messages.get(signal, f"❌ API Error: {detail}")
                st.error(error_msg)
                
                return {
                    "error": detail,
                    "signal": signal,
                    "success": False,
                    "status_code": response.status_code
                }
            except ValueError:
                # Response is not JSON
                error_msg = f"❌ HTTP {response.status_code}: {response.text[:200]}"
                st.error(error_msg)
                return {
                    "error": str(e),
                    "success": False,
                    "status_code": response.status_code
                }
        except requests.exceptions.ConnectionError as e:
            error_msg = (
                f"❌ **Connection Failed**\n\n"
                f"Cannot reach FastAPI at `{self.base_url}`\n\n"
                f"Make sure the backend is running."
            )
            st.error(error_msg)
            return {"error": "Connection failed", "success": False}
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The operation may take longer than expected.")
            return {"error": "Timeout", "success": False}
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
            return {"error": str(e), "success": False}
    
    def upload_file(self, project_id: int, file: BytesIO, filename: str) -> Dict[str, Any]:
        """
        Upload a file to the API
        
        Args:
            project_id: Project identifier
            file: File content as BytesIO
            filename: Original filename
        
        Returns:
            API response as dictionary containing:
            - file_id: ID of uploaded file (on success)
            - signal: Response signal from API
            - error: Error message (on failure)
        """
        # Verify connection first
        if not self._verify_connection():
            return {"error": "API connection failed", "success": False}
            
        try:
            content_type = 'application/pdf' if filename.lower().endswith('.pdf') else 'text/plain'
            files = {'file': (filename, file, content_type)}
            url = f"{self.base_url}/api/v1/data/upload/{project_id}"
            
            response = requests.post(url, files=files, timeout=60)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"❌ Upload failed: {str(e)}")
            return {"error": str(e), "success": False}
    
    def process_documents(self, project_id: int, chunk_size: int = 1000, 
                         overlap_size: int = 200, file_id: Optional[str] = None,
                         do_reset: int = 0) -> Dict[str, Any]:
        """
        Process uploaded documents into chunks
        
        Args:
            project_id: Project identifier
            chunk_size: Size of each text chunk (default: 1000)
            overlap_size: Overlap between chunks (default: 200)
            file_id: Specific file ID to process (optional, processes all if None)
            do_reset: Whether to delete existing chunks (1) or not (0)
        
        Returns:
            API response as dictionary containing:
            - inserted_chunks: Number of chunks created
            - processed_files: Number of files processed
            - signal: Response signal from API
        """
        # Verify connection first
        if not self._verify_connection():
            return {"error": "API connection failed", "success": False}
            
        try:
            url = f"{self.base_url}/api/v1/data/process/{project_id}"
            
            # Build request payload matching FastAPI ProcessRequest schema
            payload = {
                "chunk_size": chunk_size,
                "overlap_size": overlap_size,
                "do_reset": do_reset
            }
            
            # Only include file_id if provided
            if file_id:
                payload["file_id"] = file_id
            
            logger.debug(f"Processing documents with payload: {payload}")
            
            response = requests.post(url, json=payload, timeout=300)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"❌ Processing failed: {str(e)}")
            return {"error": str(e), "success": False}
    
    def push_to_index(self, project_id: int, do_reset: int = 0) -> Dict[str, Any]:
        """
        Push processed documents to vector index
        
        Args:
            project_id: Project identifier
            do_reset: Whether to reset existing index (1) or not (0)
        
        Returns:
            API response as dictionary containing:
            - inserted_items_count: Number of vectors inserted
            - signal: Response signal from API
        """
        # Verify connection first
        if not self._verify_connection():
            return {"error": "API connection failed", "success": False}
            
        try:
            url = f"{self.base_url}/api/v1/nlp/index/push/{project_id}"
            payload = {"do_reset": do_reset}
            
            logger.debug(f"Pushing to index with payload: {payload}")
            
            response = requests.post(url, json=payload, timeout=300)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"❌ Index push failed: {str(e)}")
            return {"error": str(e), "success": False}
    
    def get_index_info(self, project_id: int) -> Dict[str, Any]:
        """
        Get vector index information and statistics
        
        Args:
            project_id: Project identifier
        
        Returns:
            API response as dictionary containing:
            - collection_info: Dictionary with vector count, dimensions, etc.
            - signal: Response signal from API
        """
        # Connection verification is optional for GET requests
        # as they're usually less critical
        try:
            url = f"{self.base_url}/api/v1/nlp/index/info/{project_id}"
            response = requests.get(url, timeout=30)
            return self._handle_response(response)
        except Exception as e:
            st.warning(f"⚠️ Could not get index info: {str(e)}")
            return {"error": str(e), "success": False}
    
    def search_index(self, project_id: int, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search the vector index for similar documents
        
        Args:
            project_id: Project identifier
            query: Search query text
            limit: Maximum number of results to return (default: 5)
        
        Returns:
            API response as dictionary containing:
            - results: List of matching documents with scores
            - signal: Response signal from API
        """
        # Verify connection first
        if not self._verify_connection():
            return {"error": "API connection failed", "success": False}
            
        try:
            url = f"{self.base_url}/api/v1/nlp/index/search/{project_id}"
            
            # IMPORTANT: Backend expects "text" field, NOT "query"
            payload = {
                "text": query,  # Must be "text" not "query"!
                "limit": limit
            }
            
            logger.debug(f"Searching index with payload: {payload}")
            
            response = requests.post(url, json=payload, timeout=60)
            return self._handle_response(response)
        except Exception as e:
            st.error(f"❌ Search failed: {str(e)}")
            return {"error": str(e), "success": False}
    
    def ask_question(self, project_id: int, question: str, limit: int = 5, 
                    debug_mode: bool = False) -> Dict[str, Any]:
        """
        Ask a question and get AI-powered answer using RAG
        
        Args:
            project_id: Project identifier
            question: Question text to ask
            limit: Number of similar documents to retrieve for context (default: 5)
            debug_mode: Show detailed debug information (default: False)
        
        Returns:
            API response as dictionary containing:
            - answer: The generated answer
            - full_prompt: The complete prompt sent to LLM
            - chat_history: Previous chat context
            - signal: Response signal from API
        """
        # Verify connection first
        if not self._verify_connection():
            return {"error": "API connection failed", "success": False}
            
        try:
            url = f"{self.base_url}/api/v1/nlp/index/answer/{project_id}"
            
            # IMPORTANT: Backend expects "text" field, NOT "query"
            # This matches the SearchRequest Pydantic model in src/routes/schemes/nlp.py
            payload = {
                "text": question,  # Must be "text" not "query"!
                "limit": limit
            }
            
            # Optional debug logging
            if debug_mode:
                st.info(f"🔍 **Debug Info:**\n- Endpoint: `{url}`\n- Payload: `{payload}`")
            
            logger.debug(f"Asking question with payload: {payload}")
            
            response = requests.post(url, json=payload, timeout=90)
            
            if debug_mode:
                st.info(f"📡 **Response Status:** {response.status_code}")
            
            return self._handle_response(response)
        except Exception as e:
            st.error(f"❌ Question failed: {str(e)}")
            return {"error": str(e), "success": False}
    
    def check_health(self) -> bool:
        """
        Check if API is healthy and reachable
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            # Backend has /api/v1/ endpoint, not /api/v1/health
            url = f"{self.base_url}/api/v1/"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False


# Create singleton instance
api_client = APIClient()


def check_api_health() -> bool:
    """Check API health status"""
    return api_client.check_health()
