#!/usr/bin/env bash
set -euo pipefail

echo "=== Boot: $(date -u) ==="

if [[ -n "${DB_HOST:-}" && -n "${DB_PORT:-}" ]]; then
  echo "Waiting for DB ${DB_HOST}:${DB_PORT} - db ${DB_NAME} - username: ${DB_USER}..."
  for i in {1..60}; do
    if nc -z "${DB_HOST}" "${DB_PORT}" 2>/dev/null; then
      echo "DB is up."
      break
    fi
    echo "DB not ready yet... retry $i/60"
    sleep 2
    if [[ $i -eq 60 ]]; then
      echo "ERROR: Database connection timeout after 60 attempts"
      exit 1
    fi
  done
else
  echo "DB_HOST or DB_PORT not set, skipping database wait..."
fi

if [[ "${RUN_MIGRATIONS:-true}" == "true" ]]; then
  echo "Creating database if it doesn't exist..."
  # Create database if it doesn't exist
  export PGPASSWORD="${DB_PASSWORD}"
  
  # Check if database exists, if not create it
  if ! psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres -lqt | cut -d \| -f 1 | grep -qw "${DB_NAME}"; then
    echo "Database ${DB_NAME} does not exist. Creating..."
    psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres -c "CREATE DATABASE \"${DB_NAME}\""
    echo "Database ${DB_NAME} created successfully."
  else
    echo "Database ${DB_NAME} already exists."
  fi
  
  echo "Running Alembic migrations..."
  poetry run alembic upgrade head
  echo "Migrations complete."
else
  echo "RUN_MIGRATIONS=false → skipping migrations."
fi

echo "Starting application: $*"
exec "$@"
