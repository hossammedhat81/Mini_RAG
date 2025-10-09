"""
🔧 Quick Diagnostic Tool for Mini RAG System
This script checks common issues that cause 400 errors
"""

import requests
import sys
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
PROJECT_ID = 1  # Change this to your project ID

def check_backend_health() -> bool:
    """Check if backend is accessible"""
    print("🏥 Checking backend health...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
            return True
        else:
            print(f"⚠️ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - is it running?")
        print(f"   Expected URL: {API_BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {str(e)}")
        return False

def check_project_exists(project_id: int) -> Dict[str, Any]:
    """Check if project exists and get its info"""
    print(f"\n📁 Checking project {project_id}...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/v1/nlp/index/info/{project_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Project {project_id} exists")
            
            collection_info = data.get('collection_info', {})
            if collection_info:
                vectors_count = collection_info.get('vectors_count', 0)
                indexed_vectors_count = collection_info.get('indexed_vectors_count', 0)
                
                print(f"   📊 Index Statistics:")
                print(f"   - Total vectors: {vectors_count}")
                print(f"   - Indexed vectors: {indexed_vectors_count}")
                
                if vectors_count == 0:
                    print("\n⚠️ WARNING: Index is empty!")
                    print("   You need to:")
                    print("   1. Upload documents")
                    print("   2. Process documents")
                    print("   3. Push to vector database")
                else:
                    print("✅ Index has documents")
                    
            return data
        else:
            print(f"❌ Failed to get project info: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return {}
            
    except Exception as e:
        print(f"❌ Error checking project: {str(e)}")
        return {}

def test_search_endpoint(project_id: int) -> bool:
    """Test the search endpoint with a simple query"""
    print(f"\n🔍 Testing search endpoint for project {project_id}...")
    try:
        payload = {
            "text": "test query",
            "limit": 3
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/nlp/index/search/{project_id}",
            json=payload,
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results_count = len(data.get('results', []))
            print(f"✅ Search endpoint works - found {results_count} results")
            return True
        else:
            print(f"❌ Search failed")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing search: {str(e)}")
        return False

def test_answer_endpoint(project_id: int) -> bool:
    """Test the answer endpoint with a simple question"""
    print(f"\n❓ Testing answer endpoint for project {project_id}...")
    try:
        payload = {
            "text": "What is this document about?",
            "limit": 3
        }
        
        print(f"   Endpoint: {API_BASE_URL}/api/v1/nlp/index/answer/{project_id}")
        print(f"   Payload: {payload}")
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/nlp/index/answer/{project_id}",
            json=payload,
            timeout=60
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            print(f"✅ Answer endpoint works")
            print(f"   Answer preview: {answer[:100]}...")
            return True
        else:
            print(f"❌ Answer endpoint failed")
            try:
                error_data = response.json()
                print(f"   Error Details: {error_data}")
                
                # Provide specific guidance based on error
                signal = error_data.get('signal', '')
                if 'NOT_FOUND' in signal:
                    print("\n💡 SOLUTION: The index is empty or project doesn't exist")
                    print("   → Upload and process documents first")
                elif 'RAG_ANSWER_ERROR' in signal:
                    print("\n💡 SOLUTION: RAG answering failed")
                    print("   → Check if documents are properly indexed")
                    print("   → Verify API keys (OpenAI, Cohere) are set")
                    
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing answer endpoint: {str(e)}")
        return False

def main():
    """Run all diagnostic checks"""
    print("=" * 60)
    print("🔬 Mini RAG System Diagnostic Tool")
    print("=" * 60)
    
    # Check 1: Backend Health
    backend_ok = check_backend_health()
    if not backend_ok:
        print("\n❌ STOP: Backend is not running!")
        print("\n🚀 Start the backend with:")
        print("   cd c:\\University\\Mini_RAG\\mini-rag-app")
        print("   python src/main.py")
        sys.exit(1)
    
    # Check 2: Project Exists
    project_info = check_project_exists(PROJECT_ID)
    if not project_info:
        print(f"\n⚠️ WARNING: Project {PROJECT_ID} might not exist")
        print("\n💡 Try changing PROJECT_ID in this script to 22")
        print("   Or create documents for project 1 first")
    
    # Check 3: Search Endpoint
    search_ok = test_search_endpoint(PROJECT_ID)
    
    # Check 4: Answer Endpoint
    answer_ok = test_answer_endpoint(PROJECT_ID)
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"Backend Health:     {'✅ OK' if backend_ok else '❌ FAILED'}")
    print(f"Project Exists:     {'✅ OK' if project_info else '❌ FAILED'}")
    print(f"Search Endpoint:    {'✅ OK' if search_ok else '❌ FAILED'}")
    print(f"Answer Endpoint:    {'✅ OK' if answer_ok else '❌ FAILED'}")
    print("=" * 60)
    
    if backend_ok and project_info and search_ok and answer_ok:
        print("\n🎉 All checks passed! Your system should work in Streamlit.")
        print("   If you still see errors, check the troubleshooting guide:")
        print("   → docs/TROUBLESHOOTING_400_ERROR.md")
    else:
        print("\n⚠️ Some checks failed. Review the output above for solutions.")
        print("\n📚 For detailed help, see:")
        print("   → docs/TROUBLESHOOTING_400_ERROR.md")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    # You can change these values:
    # API_BASE_URL = "http://localhost:8000"  # Change if using different port
    # PROJECT_ID = 22  # Change to match your project ID
    
    main()
