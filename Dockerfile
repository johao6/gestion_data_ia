FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc curl \
    && rm -rf /var/lib/apt/lists/*


COPY . /app


RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi


ENV PYTHONPATH=/app/src


CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]


HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://127.0.0.1:${PORT:-8000}/health || exit 1
