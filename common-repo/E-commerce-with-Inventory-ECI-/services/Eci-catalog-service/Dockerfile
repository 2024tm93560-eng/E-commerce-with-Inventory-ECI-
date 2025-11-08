FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc default-libmysqlclient-dev pkg-config curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# deps first (cache-friendly)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy everything (this will include entrypoint.sh with CRLF)
COPY . /app

# convert CRLF -> LF and make executable (do this AFTER the bulk copy)
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

EXPOSE 8000

# call via bash to avoid shebang problems
CMD ["bash", "/app/entrypoint.sh"]
