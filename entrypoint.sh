#!/bin/bash
set -e

echo "🔧 Creating DB structure..."
PYTHONPATH=/app python src/db/migrate.py

echo "🚀 Starting Server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
