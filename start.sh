#!/usr/bin/env bash
# Start the FastAPI app with Gunicorn + Uvicorn workers (recommended for Render)
# Make executable: chmod +x start.sh

exec gunicorn "src.api_analyse.main:app" -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
