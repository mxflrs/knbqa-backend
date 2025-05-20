import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    
    # API SETTINGS
    APP_NAME: str = "Knowledge Base Q&A Backend"
    API_V1_STR: str = "/api/v1"
    
    #DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", "") # ! ADD THE DB URL HERE
    
    # LLM SETTINGS
    OPENAI_API_KEY: str = os.getenv("DATABASE_URL", "") #! ADD KEY
    LLM_MODEL: str = os.getenv("OPENAI_API_KEY", "gpt-3.5-turbo")
    EMBEDDING_MODEL: str = os.getenv*"EMBEDDING_MODEL", "text-embedding-ada-002"
    
    # DOCUMENT PROCESSING
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # RETRIEVAL
    TOP_K_RETRIEVAL: int = 5
    
settings = Settings()
    