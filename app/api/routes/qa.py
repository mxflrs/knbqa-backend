from typing import List
import json
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import asyncio
from datetime import datetime
import uuid

from app.db.database import get_db
from app.db.crud import QARepository
from app.schemas.qa import QARequest, QAResponse, QAHistoryResponse
from app.core.qa_chain import QAChain
from app.core.retriever import VectorRetriever

router = APIRouter()

@router.post("/ask", response_model=QAResponse)
async def ask_question(
    qa_request: QARequest,
    db: Session = Depends(get_db)
):
    if qa_request.stream:
        return await stream_qa_response(qa_request, db)
    
    # CREATE RETRIEVER
    retriever = VectorRetriever(db)
    
    # SETUP QA CHAIN
    qa_chain = QAChain(retriever_fn=lambda q: retriever.retrieve(q))
    
    # PROCESS QUESTION
    result = qa_chain.run(qa_request.question)
    
    result["created_at"] = datetime.utcnow()
    result["id"] = uuid.uuid4()
    result["chain_trace"] = (
        result["chain_visualization"].dict()
        if hasattr(result["chain_visualization"], "dict")
        else result["chain_visualization"]
    )
    
    result.pop("chain_visualization", None)
    
    # STORE QUESTION in the DB
    QARepository.create_qa_record(
        db=db,
        question=qa_request.question,
        answer=result["answer"],
        chain_trace=result["chain_trace"]
    )
    
    return result


async def stream_qa_response(qa_request: QARequest, db: Session):
    retriever = VectorRetriever(db)
    qa_chain = QAChain(retriever_fn=lambda q: retriever.retrieve(q))
    result = qa_chain.run(qa_request.question)
    
    async def save_record():
        QARepository.create_qa_record(
            db=db,
            question=qa_request.question,
            answer=result["answer"],
            chain_trace=result["chain_visualization"].dict()
        )
    
    background_tasks = BackgroundTasks()
    background_tasks.add_task(save_record)
    
    async def generate():
        # First yield the chain visualization
        yield json.dumps({
            "type": "chain_visualization",
            "data": result["chain_visualization"].dict()
        }) + "\n"
        # Then stream the answer token by token
        for token in result["answer"].split(" "):
            await asyncio.sleep(0.05)
            yield json.dumps({
                "type": "token",
                "data": token + " "
            }) + "\n"
    
    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
        background=background_tasks
    )


@router.get("/history", response_model=List[QAHistoryResponse])
def get_qa_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    qa_records = QARepository.get_qa_history(db, skip=skip, limit=limit)
    return qa_records
