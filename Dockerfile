FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools (useful if packages need compilation)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# If a requirements.txt file exists, install dependencies
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Ensure src is on PYTHONPATH
ENV PYTHONPATH=/app/src

# Default command: run uvicorn app. Can be overridden by docker-compose or docker run.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Docker healthcheck will query the HTTP /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl -f http://127.0.0.1:8000/health || exit 1
