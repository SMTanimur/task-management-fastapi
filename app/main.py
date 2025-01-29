from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.api import router as api_router
from app.core.config import settings

app = FastAPI(
    title="Task Management API",
    description="A Task Management API similar to Lark",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=f"{settings.API_V1_STR}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 