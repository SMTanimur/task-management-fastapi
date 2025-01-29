FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Configure poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Create versions directory for alembic
RUN mkdir -p alembic/versions

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 