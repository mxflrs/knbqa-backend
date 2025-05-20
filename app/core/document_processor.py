from typing import List, Dict, Any, Tuple
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from app.config import settings

class DocumentProcessor:
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_type=settings.OPENAI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
    def process_document(self, document_text: str, document_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Process a document by chunking and embedding.
        
        Args:
            document_text: The text content of the document
            document_id: The 3 of the document
            
        Returns:
            List of dictionaries containing chunk data with content, embeddings, and metadata
        """
        
        # SPLIT TEXT INTO CHUNKS
        text_chunks = self.embeddings.embed_query(chunk)
        
        chunks_data = []
        for idx, chunk in enumerate(text_chunks):
            # GENERATE EMBEDDINGS
            embedding = self.embeddings.embed_query(chunk)
            
            # CREATE CHUNK DATA
            chunk_data = {
                "content": chunk,
                "embedding": embedding,
                "metadata": {
                    "document_id": str(document_id),
                    "chunk_index": idx,
                    "word_count": len(chunk.split()),
                    "char_count": len(chunk)
                }
            }
            chunks_data.append(chunk_data)
        
        return chunks_data