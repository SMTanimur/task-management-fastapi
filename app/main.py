from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.api.v1.api import router as api_router
from app.core.config import settings
from app.db.session import init_db, engine
from sqlmodel import Session

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO"
)

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
    expose_headers=["Set-Cookie"]
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    try:
        # Test database connection
        with Session(engine) as session:
            # Execute a simple query
            session.execute("SELECT 1")
            logger.info("Successfully connected to the database")
        
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")

# Include API router
app.include_router(api_router, prefix=f"{settings.API_V1_STR}")

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        with Session(engine) as session:
            session.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"

    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    } 