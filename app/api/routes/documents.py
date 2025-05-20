from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import uuid

from app.db.database import get_db
from app.db.crud import DocumentRepository, ChunkRepository
from app.schemas.document import DocumentCreate, DocumentResponse
from app.core.document_processor import DocumentProcessor

router = APIRouter()
document_processor = DocumentProcessor()

@router.post("/", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: Session = Depends(get_db)
):
    # UPLOAD DOC AND PROCESS IT
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .md files are supported"
        )
    
    # READ FILE CONTENT
    content = await file.read()
    text_content = content.decode('utf-8')
    
    # CREATE DOC IN DB
    document = DocumentCreate(title=title, content=text_content)
    db_document = DocumentRepository.create_document(db, document)
    
    # PROCESS DOC
    chunks_data = document_processor.process_document(text_content, db_document.id)
    
    # STORE CHUNKS IN DB
    ChunkRepository.create_chunks(db, db_document.id, chunks_data)
    
    return db_document


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    skip: int = 0,
    limit = 100,
    db: Session = Depends(get_db)
):
    documents = DocumentRepository.get_all_documents(db, skip=skip, limit=limit)
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    document = DocumentRepository.get_docuent(db, document_id)  
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    return document
    
@router.delete("/{document_id}")
def delete_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    success = DocumentRepository.delete_document(db, document_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Document nor found"
        )
    return {"message": "Document deleted successfully"}