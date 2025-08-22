@echo off
REM ==== Activate virtual environment (Windows) ====
call venv\Scripts\activate

REM ==== Run FastAPI backend with restricted reload (avoid watching data outputs) ====
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app --reload-dir llm --reload-exclude data --reload-exclude venv
