#!/usr/bin/env bash
# Start the FastAPI app with Gunicorn + Uvicorn workers on Render
# This script is executed automatically by Render when the service starts.
# The PORT environment variable is set by Render.

# Ensure PORT is set (Render always provides it, but default to 8000 for local testing)
PORT=${PORT:-8000}

# Start gunicorn with uvicorn workers optimized for Render
# - workers: 2 (suitable for small/medium Render instances; adjust based on plan)
# - threads: 2 per worker (total 4 threads for concurrent requests)
# - bind: 0.0.0.0:$PORT (listen on all interfaces, use Render's dynamically assigned PORT)
# - timeout: 120s (allows time for model inference without timeout)
# - access-logfile: - (log to stdout for Render's log viewer)
# - error-logfile: - (error logs to stdout)
# - log-level: info (informative logging)

exec gunicorn "src.api_analyse.main:app" \
  -k "uvicorn.workers.UvicornWorker" \
  --workers 2 \
  --threads 2 \
  --bind "0.0.0.0:${PORT}" \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
