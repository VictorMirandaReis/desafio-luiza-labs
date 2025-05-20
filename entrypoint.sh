#!/bin/bash
set -e

until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting DB ..."
  sleep 2
done

echo "Creating DB structure..."
PYTHONPATH=/app python src/db/migrate.py

echo "Starting Server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
