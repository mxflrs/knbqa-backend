from typing import List, Dict, Any
import numpy as np
from sqlalchemy.orm import Session
from langchain_openai import OpenAIEmbeddings

from app.config import settings
from app.db.models import DocumentChunk

class VectorRetriever:
    
    # RETRIEVER FOR FINDING RELEVANT DOCUMENT CHUNKS USING VECTOR SIMILARITY
    
    def __init__(self, db: Session):
        self.db = db
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        # CALC COSINE SIMILARITY BETWEEN TWO VECTORS
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
        return np.dot(a, b) / (a_norm * b_norm)
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        # RETURN LIST OF RELEVANT DOCS CHUNKS WITH SIMILARITY SCORES
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVAL
            
        query_embedding = self.embeddings.embed_query(query)
        all_chunks = self.db.query(DocumentChunk).all()
        
        # CALCULATE SIMILARITY SCORES
        results = []
        for chunk in all_chunks:
            if chunk.embedding:
                # CONVERT EMBEDDING FROM JSON TO LIST IF NEEDED
                chunk_embedding = chunk.embedding if isinstance(chunk.embedding, List) else list(chunk.embedding)
                
                similarity = self._cosine_similarity(query_embedding, chunk_embedding)
                
                results.append({
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "metadata": chunk.metadata,
                    "similarity": similarity
                })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
                