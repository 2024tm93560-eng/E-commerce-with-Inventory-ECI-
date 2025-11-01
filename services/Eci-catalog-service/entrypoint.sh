#!/usr/bin/env bash
set -e

echo "Waiting for DB at ${DB_HOST:-db}:${DB_PORT:-3306} ..."
until python - <<'PY'
import os, socket, sys
h=os.getenv("DB_HOST","db"); p=int(os.getenv("DB_PORT","3306"))
s=socket.socket()
try:
    s.connect((h,p)); print("DB reachable")
except Exception as e:
    print("DB not ready:", e); sys.exit(1)
PY
do sleep 2; done

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting Django on 0.0.0.0:8000"
python manage.py runserver 0.0.0.0:8000
