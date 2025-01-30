FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config installer.max-workers 10 \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# Create necessary directories
RUN mkdir -p logs alembic/versions

# Copy application code
COPY . .

# Install the application
RUN poetry install --no-interaction --no-ansi

# Set environment variables
ENV PYTHONPATH=/app \
  PYTHONUNBUFFERED=1 \
  PORT=8000

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"] 