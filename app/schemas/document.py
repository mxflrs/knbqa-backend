from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class DocumentBase(BaseModel):
    title: str

class DocumentCreate(DocumentBase):
    content: str
    
class DocumentResponse(DocumentBase):
    id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class DocumentChunkBase(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class DocumentChunkCreate(DocumentChunkBase):
    id: UUID
    embedding: Optional[List[float]]

class DocumentChunkCreate(DocumentChunkBase):
    id: UUID
    document_id: UUID
    chunk_index: int
    created_at: datetime
    
    class Config:
        orm_mode = True