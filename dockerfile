FROM python:3.11-slim

WORKDIR /app

# System deps (optional but helpful for PDF libs)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fly sets $PORT; default to 8080 if absent
ENV PORT=8080
EXPOSE 8080

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]