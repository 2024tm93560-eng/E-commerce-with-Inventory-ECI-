# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=5090

# (optional) faster installs
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements first (better layer cache)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# App
COPY . /app

# If you use a .env, copy it during build only if it contains NON-SECRETS.
# Otherwise mount it at runtime or set env via K8s Secret/ConfigMap.
# COPY .env /app/.env

EXPOSE 5090
# Use gunicorn for production serving
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5090", "app:app"]
