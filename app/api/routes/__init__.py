from fastapi import APIRouter
from app.api.routes import documents, qa

# CREATE MAIN API ROUTER
api_router = APIRouter()

# SUB-ROUTES
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(qa.router, prefix="/qa", tags=["qa"])