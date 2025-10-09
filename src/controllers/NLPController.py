from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List
import json

# Web search support
try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    
    async def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_name=collection_name)
    
    async def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = await self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    async def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   chunks_ids: List[int], 
                                   do_reset: bool = False):
        
        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items
        texts = [ c.chunk_text for c in chunks ]
        metadata = [ c.chunk_metadata for c in  chunks]
        vectors = self.embedding_client.embed_text(text=texts, 
                                                  document_type=DocumentTypeEnum.DOCUMENT.value)

        # step3: create collection if not exists
        _ = await self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # step4: insert into vector db
        _ = await self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        return True

    async def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):

        # step1: get collection name
        query_vector = None
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: get text embedding vector
        vectors = self.embedding_client.embed_text(text=text, 
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vectors or len(vectors) == 0:
            return False
        
        if isinstance(vectors, list) and len(vectors) > 0:
            query_vector = vectors[0]

        if not query_vector:
            return False    

        # step3: do semantic search
        results = await self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=limit
        )

        if not results:
            return False

        return results
    
    async def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        
        answer, full_prompt, chat_history = None, None, None

        # step1: retrieve related documents
        retrieved_documents = await self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": self.generation_client.process_text(doc.text),
            })
            for idx, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt", {
            "query": query
        })

        # step3: Construct Generation Client Prompts
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

        # step4: Retrieve the Answer
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        return answer, full_prompt, chat_history

    def search_web(self, query: str, max_results: int = 3):
        """Search internet using DuckDuckGo (no API key needed)"""
        if not SEARCH_AVAILABLE:
            return {
                "success": False,
                "error": "Web search not available. Install: pip install duckduckgo-search"
            }
        
        try:
            # Use backend='api' to avoid rate limiting issues
            # Try multiple times with different backends if rate limited
            backends = ['api', 'html', 'lite']
            last_error = None
            
            for backend in backends:
                try:
                    with DDGS() as ddgs:
                        results = list(ddgs.text(
                            query, 
                            max_results=max_results,
                            backend=backend
                        ))
                    
                    if results:
                        return {
                            "success": True,
                            "results": results,
                            "count": len(results)
                        }
                except Exception as e:
                    last_error = str(e)
                    continue
            
            # If all backends fail, return error
            return {
                "success": False,
                "error": f"All search backends failed. Last error: {last_error}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def answer_with_web_search(self, query: str, max_results: int = 3):
        """Generate answer using web search results"""
        import logging
        logger = logging.getLogger('uvicorn.error')
        
        logger.info(f"Starting web search for query: {query}")
        search_results = self.search_web(query, max_results)
        
        if not search_results.get("success"):
            error = search_results.get("error", "Unknown error")
            logger.error(f"Web search failed: {error}")
            return None, None
        
        logger.info(f"Web search successful, found {len(search_results['results'])} results")
        
        # Format search results for LLM
        results_text = "\n\n".join([
            f"Source {i+1}: {r['title']}\n{r['body']}\nURL: {r['href']}"
            for i, r in enumerate(search_results["results"])
        ])
        
        # Generate answer from search results
        system_prompt = "You are a helpful assistant. Answer the question using the provided web search results."
        
        full_prompt = f"""Web Search Results:
{results_text}

Question: {query}

Answer the question using the information from the search results above. Include relevant URLs."""
        
        logger.info("Generating LLM answer from search results...")
        
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]
        
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )
        
        logger.info(f"LLM answer generated, length: {len(answer) if answer else 0}")
        
        return answer, search_results["results"]


