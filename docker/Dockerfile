# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy application code
COPY . /app/

# Expose port
EXPOSE 8000

# Run application
CMD ["poetry", "run", "uvicorn", "usersnack.main:app", "--host", "0.0.0.0", "--port", "8000"]