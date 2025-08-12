# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    netcat-openbsd \
    ca-certificates \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry==1.8.3

# Copy poetry files
COPY poetry.lock pyproject.toml /app/

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --without dev \
    && rm -rf $POETRY_CACHE_DIR

# Copy application code
COPY . /app/

# Copy entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create non-root user
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
    && chown -R user:user /app
USER user

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run migrations first, then start the app
ENTRYPOINT ["/app/entrypoint.sh"]

# Run application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]