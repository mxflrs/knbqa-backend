from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.routes import api_router
from app.config import settings
from app.db.database import Base, engine

# CREATE DB TABLES
Base.metadata.create_all(bind=engine)

# INITI FASTAPI
app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUDE API ROUTER
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")