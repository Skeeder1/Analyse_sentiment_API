# app.py
"""Compatibility wrapper for the FastAPI application.

This file keeps the original module path (`app`) for tests or external imports.
It only re-exports the `app` instance from the package implementation and avoids
importing optional heavy dependencies at module import time.
"""

from src.api_analyse.main import app  # re-export package app for backwards compatibility
