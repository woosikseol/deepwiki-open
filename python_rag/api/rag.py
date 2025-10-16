"""
RAG implementation for python_rag
"""
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from jinja2 import Template

from api.config import (
    get_db_connection_string,
    get_language_name,
    TOP_K_RESULTS,
    DEFAULT_LANGUAGE,
    EMBEDDING_MODEL
)
from api.prompts import RAG_SYSTEM_PROMPT, RAG_TEMPLATE
from api.gemini_client import GeminiClient

# Import from python_chunking
import sys
from pathlib import Path

# Add python_chunking to path
python_chunking_path = Path(__file__).parent.parent.parent / "python_chunking"
if str(python_chunking_path) not in sys.path:
    sys.path.insert(0, str(python_chunking_path))

from core.embeddings.embeddings_provider import EmbeddingsProvider
from core.indexing.pgvector_index import PgVectorIndex
from core.index import Chunk

logger = logging.getLogger(__name__)


@dataclass
class RAGAnswer:
    """RAG answer structure"""
    answer: str
    contexts: List[Chunk]
    query: str
    language: str


class RAG:
    """
    RAG (Retrieval-Augmented Generation) implementation
    
    This class provides Question & Answer functionality using:
    - PostgreSQL + pgvector for vector storage and retrieval
    - Gemini API for text generation
    - all-MiniLM-L6-v2 for embeddings (same as python_chunking)
    """
    
    def __init__(
        self,
        language: str = DEFAULT_LANGUAGE,
        top_k: int = TOP_K_RESULTS,
        gemini_client: Optional[GeminiClient] = None
    ):
        """
        Initialize RAG component
        
        Args:
            language: Output language code (default: ko)
            top_k: Number of top results to retrieve
            gemini_client: Optional custom Gemini client
        """
        self.language = language
        self.top_k = top_k
        
        # Initialize Gemini client
        self.gemini_client = gemini_client or GeminiClient()
        
        # Initialize embeddings provider (same model as python_chunking)
        self.embeddings_provider = EmbeddingsProvider(model_name=EMBEDDING_MODEL)
        
        # Initialize pgvector index
        connection_string = get_db_connection_string()
        self.index = PgVectorIndex(
            embeddings_provider=self.embeddings_provider,
            connection_string=connection_string
        )
        
        logger.info(f"Initialized RAG with language={language}, top_k={top_k}")
    
    async def initialize(self):
        """Initialize database connection"""
        await self.index.initialize()
        logger.info("RAG initialized successfully")
    
    async def retrieve_contexts(
        self,
        query: str,
        filters: Optional[Dict] = None
    ) -> List[Chunk]:
        """
        Retrieve relevant contexts from the database
        
        Args:
            query: User query
            filters: Optional filters for retrieval
            
        Returns:
            List of relevant chunks
        """
        try:
            # Retrieve similar chunks from pgvector
            chunks = await self.index.retrieve(
                query=query,
                n_retrieve=self.top_k,
                filters=filters
            )
            
            logger.info(f"Retrieved {len(chunks)} contexts for query: {query[:50]}...")
            return chunks
            
        except Exception as e:
            logger.error(f"Error retrieving contexts: {e}")
            return []
    
    def _format_prompt(
        self,
        query: str,
        contexts: List[Chunk],
        language: str
    ) -> str:
        """
        Format the prompt using Jinja2 template
        
        Args:
            query: User query
            contexts: Retrieved contexts
            language: Output language code
            
        Returns:
            Formatted prompt
        """
        try:
            # Get language name
            language_name = get_language_name(language)
            
            # Prepare template
            template = Template(RAG_TEMPLATE)
            
            # Render prompt
            prompt = template.render(
                system_prompt=RAG_SYSTEM_PROMPT,
                query=query,
                contexts=contexts,
                language_name=language_name
            )
            
            return prompt
            
        except Exception as e:
            logger.error(f"Error formatting prompt: {e}")
            raise
    
    async def answer(
        self,
        query: str,
        language: Optional[str] = None,
        filters: Optional[Dict] = None,
        **generation_kwargs
    ) -> RAGAnswer:
        """
        Answer a user query using RAG
        
        Args:
            query: User query
            language: Output language (defaults to instance language)
            filters: Optional filters for retrieval
            **generation_kwargs: Additional arguments for generation
            
        Returns:
            RAGAnswer containing answer, contexts, and metadata
        """
        # Use provided language or default
        output_language = language or self.language
        
        try:
            # 1. Retrieve relevant contexts
            logger.info(f"Processing query: {query[:100]}...")
            contexts = await self.retrieve_contexts(query, filters)
            
            if not contexts:
                logger.warning("No contexts retrieved from database")
                return RAGAnswer(
                    answer="죄송합니다. 관련된 정보를 찾을 수 없습니다. 데이터베이스에 코드가 인덱싱되어 있는지 확인해주세요.",
                    contexts=[],
                    query=query,
                    language=output_language
                )
            
            # 2. Format prompt
            prompt = self._format_prompt(query, contexts, output_language)
            
            # 3. Generate answer using Gemini
            logger.info("Generating answer with Gemini...")
            answer_text = await self.gemini_client.generate_async(
                prompt,
                **generation_kwargs
            )
            
            # 4. Create and return RAGAnswer
            result = RAGAnswer(
                answer=answer_text,
                contexts=contexts,
                query=query,
                language=output_language
            )
            
            logger.info("Successfully generated answer")
            return result
            
        except Exception as e:
            logger.error(f"Error in RAG answer generation: {e}")
            return RAGAnswer(
                answer=f"오류가 발생했습니다: {str(e)}",
                contexts=[],
                query=query,
                language=output_language
            )
    
    def close(self):
        """Close database connection"""
        self.index.close()
        logger.info("RAG closed")

