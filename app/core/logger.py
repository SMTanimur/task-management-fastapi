import sys
import logging
from pathlib import Path
from loguru import logger
from app.core.config import settings

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Custom log format
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level> | "
    "Request ID: {extra[request_id]} | "
    "User: {extra[user]}"
)

# Configure loguru logger
def setup_logging():
    # Remove default handler
    logger.remove()
    
    # Add console handler with custom format
    logger.add(
        sys.stdout,
        colorize=True,
        format=LOG_FORMAT,
        level="DEBUG" if settings.DEBUG else "INFO",
        backtrace=True,
        diagnose=True,
    )
    
    # Add file handler for all logs
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        format=LOG_FORMAT,
        level="INFO",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    # Add file handler for errors only
    logger.add(
        "logs/error.log",
        rotation="100 MB",
        retention="30 days",
        format=LOG_FORMAT,
        level="ERROR",
        compression="zip",
        backtrace=True,
        diagnose=True,
        filter=lambda record: record["level"].name == "ERROR"
    )

    # Intercept standard library logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Configure standard library logging to use loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Set SQLAlchemy logging to use loguru
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    return logger

# Create a context manager for request logging
class RequestContextLogger:
    def __init__(self, request_id: str = None, user: str = "anonymous"):
        self.request_id = request_id
        self.user = user
        self.context = {}

    def __enter__(self):
        self.context = logger.bind(request_id=self.request_id, user=self.user)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass 