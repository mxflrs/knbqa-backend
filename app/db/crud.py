from uuid import UUID
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import numpy as np

from app.db.models import Document, DocumentChunk, QARecord
from app.schemas.document import DocumentCreate # ! ADD THIS ONE
from app. schemas.qa import QARequest, QAResponse # ! ADD THIS ONE
