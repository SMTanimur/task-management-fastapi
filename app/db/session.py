from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from app.core.logger import setup_logging

logger = setup_logging()

# Configure database engine with logging
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # SQL query logging
    echo_pool=settings.DEBUG,  # Connection pool logging
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,  # Maximum number of connections in the pool
    max_overflow=10  # Maximum number of connections that can be created beyond pool_size
)

def init_db():
    logger.info("Initializing database...")
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise e

def get_session():
    logger.debug("Creating new database session")
    try:
        with Session(engine) as session:
            yield session
            logger.debug("Database session closed successfully")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}", exc_info=True)
        raise e 