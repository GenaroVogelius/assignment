#!/bin/sh

# Run the FastAPI application with uvicorn
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000