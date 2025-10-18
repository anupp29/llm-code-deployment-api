# 🚀 LLM Code Deployment - Deployment Guide

## 📋 Pre-Deployment Checklist

- ✅ Codebase cleaned and optimized
- ✅ Dependencies streamlined
- ✅ Environment variables configured
- ✅ Deployment configurations created

## 🌐 Deployment Options

### **Option 1: Railway (Recommended)**

Railway is perfect for Python applications with background tasks.

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables**:
   ```bash
   railway variables set USER_SECRET="TDS DEDLY"
   railway variables set GITHUB_TOKEN="your_github_token"
   railway variables set GITHUB_USERNAME="your_username"
   railway variables set OPENAI_API_KEY="your_openai_key"
   railway variables set OPENAI_BASE_URL="https://aipipe.org/openai/v1"
   ```

### **Option 2: Vercel**

Good for API endpoints, but may have limitations with long-running tasks.

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

3. **Set Environment Variables** in Vercel dashboard or CLI:
   ```bash
   vercel env add USER_SECRET
   vercel env add GITHUB_TOKEN
   vercel env add GITHUB_USERNAME
   vercel env add OPENAI_API_KEY
   vercel env add OPENAI_BASE_URL
   ```

### **Option 3: Docker (Any Platform)**

Deploy using Docker on any cloud provider.

1. **Build Image**:
   ```bash
   docker build -t llm-deployment .
   ```

2. **Run Container**:
   ```bash
   docker-compose up -d
   ```

### **Option 4: Render**

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in dashboard

## 🔧 Environment Variables Required

```bash
USER_SECRET="TDS DEDLY"
GITHUB_TOKEN="ghp_your_github_token"
GITHUB_USERNAME="your_github_username"
OPENAI_API_KEY="your_openai_api_key"
OPENAI_BASE_URL="https://aipipe.org/openai/v1"
```

## 🧪 Testing Deployed API

Once deployed, test your API:

```bash
# Health check
curl https://your-app-url.com/health

# Test endpoint
curl -X POST https://your-app-url.com/api-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "email": "23f2003212@ds.study.iitm.ac.in",
    "secret": "TDS DEDLY",
    "task": "test-task-123",
    "round": 1,
    "nonce": "test-nonce",
    "brief": "Create a simple web page",
    "checks": ["Page loads successfully"],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
  }'
```

## 📊 Monitoring

- **Health Check**: `/health` endpoint
- **Logs**: Check platform-specific logging
- **GitHub**: Monitor repository creation
- **OpenAI**: Monitor API usage

## 🔒 Security Notes

- Never commit `.env` file
- Use platform environment variables
- Rotate tokens regularly
- Monitor API usage

## 🎯 Production Considerations

- **Rate Limiting**: Consider adding rate limits
- **Database**: For production, use PostgreSQL instead of SQLite
- **Caching**: Add Redis for caching
- **Monitoring**: Set up application monitoring
- **Backup**: Regular backup of evaluation data

---

**Your LLM Code Deployment API is ready for production!** 🚀
