from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# CREATE SQL ENGINE
engine = create_engine(settings.DATABASE_URL)

# CREATE SESSION LOCAL CLASS
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# CREATE BASE CLASS FOR MODELS
Base = declarative_base()

# GET DB SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()