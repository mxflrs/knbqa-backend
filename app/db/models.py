from datetime import datetime
import uuid
from typing import List, Dict, Any, Optional

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.database import Base

class Document(Base):
    
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # RELATIONSHIP -- ONE DOCUMENT HAS MANY CHUNKS
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete_orphan")
    
class DocumentChunk(Base):
    
    __tablename__ = "document_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSONB, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # RELATIONSHIP -- MANY CHUNKS BELONG TO ONE DOCUMENT
    document = relationship("Document", back_populates="chunks")
    
class QARecord(Base):

    __tablename__ = "qa_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    chain_trace = Column(JSONB, nullable=True)
    created_at = Column(datetime, default=datetime.utcnow)