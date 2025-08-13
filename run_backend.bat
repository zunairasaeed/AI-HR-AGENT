#!/bin/bash
# ==== Activate virtual environment ====
source venv/bin/activate

# ==== Run FastAPI backend ====
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
