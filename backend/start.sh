#!/bin/bash
# Production startup script for the backend (Render/PaaS deployment)
# Optimized for low-latency deployment with Uvicorn + Gunicorn

set -e

echo "Starting Hackathon Backend in Production Mode"

# Set production environment variables
export PYTHONUNBUFFERED=1
export ENVIRONMENT=production

# Number of workers (auto-detected based on available CPU cores)
export WEB_CONCURRENCY=${WEB_CONCURRENCY:-4}

# Run database migrations if alembic is configured
echo "Running database migrations..."
if [ -d "alembic" ]; then
    alembic upgrade head || echo "Migration failed or not needed"
else
    echo "No alembic directory found, skipping migrations"
fi

# Start server with Gunicorn + Uvicorn workers
echo "Starting Gunicorn with $WEB_CONCURRENCY Uvicorn workers..."
exec gunicorn src.main:app \
    -c gunicorn_conf.py \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers $WEB_CONCURRENCY \
    --bind 0.0.0.0:${PORT:-8000} \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --timeout 120 \
    --graceful-timeout 30 \
    --keep-alive 5
