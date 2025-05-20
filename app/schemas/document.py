from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class DocumentBase(BaseModel):
    title: str

class DocumentCreate(DocumentBase):
    content: str
    
class DocumentResponse(DocumentBase):
    id: UUID
    created_at: datetime
    
    # class Config:
    #     orm_mode = True
    model_config = {
        "from_attributes": True
    }

        
class DocumentChunkBase(BaseModel):
    content: str
    chunk_metadata: Optional[Dict[str, Any]] = None

class DocumentChunkCreate(DocumentChunkBase):
    document_id: UUID
    embedding: Optional[List[float]] = None

class DocumentChunkResponse(DocumentChunkBase):
    id: UUID
    document_id: UUID
    chunk_index: int
    created_at: datetime
    
    # class Config:
    #     orm_mode = True
    model_config = {
        "from_attributes": True
    }
