# Dockerfile (Eci-order-service) — mysqlclient
FROM python:3.12-slim

# Helpful Python defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Bump this to force a cache bust when apt layers feel sticky
ARG CACHE_BUST=1

# ---- System deps REQUIRED by mysqlclient ----
# On Debian slim, libmariadb-dev(+compat) provides headers libs compatible with mysqlclient.
# If your base resolves default-libmysqlclient-dev, you can use that instead.
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- Install Python deps first for better caching ----
COPY requirements.txt ./
# (Optional but recommended)
RUN python -m pip install --upgrade --no-cache-dir pip setuptools wheel
# Quick sanity check to ensure pkg-config truly exists in this layer
RUN which pkg-config && pkg-config --list-all >/dev/null || true
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app code ----
COPY . .

EXPOSE 8000

# Run DB migrations then start Django
CMD ["sh","-c","python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]