from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class QARequest(BaseModel):
    question: str = Field(..., description="The question to answer")
    stream: bool = Field(False, description="Whether to stream the response")
    
class ChainNode(BaseModel):
    id: str
    type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    
class ChainEdge(BaseModel):
    source: str
    target: str
    label: Optional[str] = None
    
class ChainVisualization(BaseModel):
    nodes: List[ChainNode]
    edges: List[ChainEdge]
    
class QAWorkflowState(BaseModel):
    question: str
    context: str = ""
    answer: str = ""
    question_node_id: str = ""

class QAResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    question: str
    answer: str
    chain_trace: Optional[Dict[str, Any]] = None
    created_at: datetime
    
class QAHistoryResponse(BaseModel):
    id: UUID
    question: str
    answer: str
    chain_trace: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    # class Config:
    #     orm_mode = True
    model_config = {
        "from_attributes": True
    }

    