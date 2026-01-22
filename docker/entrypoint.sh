#!/usr/bin/env bash
set -euo pipefail

# Minimal entrypoint for a personal Docker setup using Postgres + Flask-Migrate + Gunicorn

: "${DATABASE_URL:?DATABASE_URL must be set}"
: "${FLASK_APP:=main}"
: "${PORT:=5002}"

cd /app || exit 1

echo "[entrypoint] FLASK_APP=${FLASK_APP} PORT=${PORT}"

# 1) Wait for the database to accept connections (simple psycopg2 loop)
python - <<'PY'
import os, time, sys
import psycopg2

dsn = os.environ.get("DATABASE_URL")
if not dsn:
    print("DATABASE_URL not set", file=sys.stderr)
    sys.exit(2)

for i in range(60):           # wait up to ~60 seconds
    try:
        conn = psycopg2.connect(dsn)
        conn.close()
        print("Database reachable")
        sys.exit(0)
    except Exception:
        time.sleep(1)
print("Timed out waiting for database", file=sys.stderr)
sys.exit(1)
PY

# 2) Apply migrations (assumes migrations/ committed to repo)
echo "[entrypoint] applying migrations"
python -m flask --app "${FLASK_APP}" db migrate -m "Initial migration"
python -m flask --app "${FLASK_APP}" db upgrade

# 3) Launch Gunicorn (exec so it receives signals)
echo "[entrypoint] starting Gunicorn"
exec gunicorn --bind "0.0.0.0:${PORT}" --workers 2 "${FLASK_APP}:app"
