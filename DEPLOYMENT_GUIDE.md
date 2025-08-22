# 🚀 AI HR Agent - Fly.io Deployment Guide

This guide will help you deploy your FastAPI backend to Fly.io and connect it with your Streamlit frontend.

## 📋 Prerequisites

1. **Fly.io CLI installed**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Docker Desktop** (optional, but recommended)
   - Download from: https://www.docker.com/products/docker-desktop/

3. **Git repository** with your code pushed

## 🔧 Backend Deployment (FastAPI)

### Step 1: Login to Fly.io
```bash
flyctl auth login
```

### Step 2: Initialize Fly App
```bash
# From your project root directory
flyctl launch --no-deploy
```

**Answer the prompts:**
- App name: `ai-hr-agent-api` (or your preferred name)
- Region: Choose closest to you (e.g., `sin` for Singapore)
- Use existing Dockerfile: `Yes`

### Step 3: Set Environment Variables (Secrets)
```bash
# Set your Azure OpenAI credentials
flyctl secrets set AZURE_OPENAI_API_KEY="your-api-key-here"
flyctl secrets set AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
flyctl secrets set AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
flyctl secrets set AZURE_OPENAI_API_VERSION="2024-02-15-preview"

# Optional: Set other environment variables
flyctl secrets set SKIP_LLM_SUMMARY="true"
```

### Step 4: Deploy
```bash
flyctl deploy
```

### Step 5: Verify Deployment
```bash
# Check app status
flyctl status

# View logs
flyctl logs

# Open the app
flyctl open
```

Your API will be available at: `https://your-app-name.fly.dev`

## 🌐 Frontend Deployment (Streamlit)

### Option 1: Streamlit Cloud (Recommended)

1. **Push your code to GitHub**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub repository**
4. **Set the main file path:** `app/streamlit_app.py`
5. **Add secrets in Streamlit Cloud:**
   ```
   FASTAPI_BASE_URL = "https://your-app-name.fly.dev"
   ```

### Option 2: Deploy Streamlit to Fly.io

Create a separate `Dockerfile.streamlit`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install streamlit requests

COPY app/streamlit_app.py .
COPY requirements.txt .

ENV PORT=8501
EXPOSE 8501

CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port ${PORT} --server.address 0.0.0.0"]
```

Then deploy:
```bash
# Create a new Fly app for Streamlit
flyctl launch --no-deploy --name ai-hr-agent-frontend

# Set environment variables
flyctl secrets set FASTAPI_BASE_URL="https://your-backend-app-name.fly.dev"

# Deploy
flyctl deploy
```

## 🔗 Connect Frontend to Backend

### In Streamlit Cloud:
1. Go to your app settings
2. Add secret: `FASTAPI_BASE_URL = "https://your-backend-app-name.fly.dev"`

### In Local Development:
Set environment variable:
```bash
# Windows
set FASTAPI_BASE_URL=https://your-backend-app-name.fly.dev

# macOS/Linux
export FASTAPI_BASE_URL=https://your-backend-app-name.fly.dev
```

## 🧪 Testing Your Deployment

### Test Backend Health
```bash
curl https://your-app-name.fly.dev/health
```

### Test API Endpoints
1. Open: `https://your-app-name.fly.dev/docs`
2. Test the `/upload` endpoint with sample files
3. Check `/tailored_cvs` and download endpoints

### Test Frontend
1. Open your Streamlit app
2. Upload test resumes and JDs
3. Verify the pipeline runs successfully
4. Download generated files

## 🔧 Troubleshooting

### Common Issues:

1. **"No module named 'openai'"**
   - Ensure `openai>=1.14.0` is in `requirements.txt`

2. **CORS errors**
   - Backend has CORS middleware configured
   - Check if frontend URL is in allowed origins

3. **Timeout errors**
   - Pipeline can take 2-5 minutes
   - Increase timeout in Streamlit: `REQUEST_TIMEOUT=600`

4. **Port issues**
   - Backend uses port 8080 (Fly.io standard)
   - Frontend uses port 8501 (Streamlit standard)

5. **Memory issues**
   - Increase VM memory in `fly.toml`:
   ```toml
   [[vm]]
     memory_mb = 2048  # Increase from 1024
   ```

### View Logs:
```bash
# Backend logs
flyctl logs

# Real-time logs
flyctl logs --follow
```

### Restart App:
```bash
flyctl restart
```

## 📊 Monitoring

### Check App Status:
```bash
flyctl status
flyctl apps list
```

### Monitor Resources:
```bash
flyctl dashboard
```

## 🔄 Updates

To update your deployment:

1. **Update code and push to Git**
2. **Redeploy:**
   ```bash
   flyctl deploy
   ```

3. **Check logs:**
   ```bash
   flyctl logs
   ```

## 🎯 Production Considerations

1. **Remove wildcard CORS** in production:
   ```python
   origins = [
       "https://your-streamlit-app.streamlit.app",
       "https://your-frontend-domain.com"
   ]
   ```

2. **Set up monitoring** and alerts

3. **Consider scaling** for higher traffic:
   ```toml
   [http_service]
     min_machines_running = 2
   ```

4. **Backup your data** regularly

## 📞 Support

- **Fly.io Docs:** https://fly.io/docs/
- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

**Your AI HR Agent is now ready for production! 🎉**
