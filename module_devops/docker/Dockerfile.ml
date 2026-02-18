# module_devops/docker/Dockerfile.ml
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY module_ml/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY module_ml/ .
COPY module_utils/ /module_utils/

# Create directory for models
RUN mkdir -p /app/models

# Environment variables
ENV PYTHONPATH=/app:/module_utils
ENV PYTHONUNBUFFERED=1

# Run ML service
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]