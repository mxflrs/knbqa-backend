from uuid import UUID
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import numpy as np

from app.db.models import Document, DocumentChunk, QARecord
from app.schemas.document import DocumentCreate
from app. schemas.qa import QARequest, QAResponse

class DocumentRepository:
    
    @staticmethod
    def create_document(db: Session, document: DocumentCreate) -> Document:
        db_document = Document(
            title=document.title,
            content=document.content
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return db_document
    
    @staticmethod
    def get_docuent(db: Session, document_id: UUID) -> Optional[Document]:
        return db.query(Document).filter(Document.id == document_id).first()
    
    @staticmethod
    def get_all_documents(db: Session, skip: int = 0, limit: int = 100) -> List[Document]:
        return db.query(Document).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_document(db: Session, document_id: UUID) -> bool:
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            return False
        db.delete(document)
        db.commit()
        return True
    
    
class ChunkRepository:
    
    @staticmethod
    def create_chunks(db: Session, document_id: UUID, chunks: List[Dict[str, Any]]) -> List[DocumentChunk]:
        db_chunks = []
        
        for idx, chunk_data in enumerate(chunks):
            db_chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=idx,
                content=chunk_data["content"],
                embedding=chunk_data.get("embedding"),
                metadata=chunk_data.get("metadata", {})
            )
            db_chunk.append(db_chunk)
        
        db.add_all(db_chunks)
        db.commit()
        
        for chunk in db_chunks:
            db.refresh(chunk)
        return db_chunks
            
    @staticmethod
    def get_all_chunks(db: Session) -> List[DocumentChunk]:
        return db.query(DocumentChunk).all()
    
class QARepository:
    
    @staticmethod
    def create_qa_record(db: Session, question: str, answer: str, chain_trace: Dict[str, Any]) -> QARecord:
        qa_record = QARecord(
            question=question,
            answer=answer,
            chain_trace=chain_trace
        )
        db.add(qa_record)
        db.commit()
        db.refresh(qa_record)
        return qa_record
    
    @staticmethod
    def get_qa_history(db: Session, skip: int = 0, limit: int = 20) -> List[QARecord]:
        return db.query(QARecord).order_by(QARecord.created_at.desc()).offset(skip).limit(limit).all()
        