# 🎯 LLM Code Deployment API

**Production-ready API for automated code generation, GitHub deployment, and evaluation.**
## 🚀 **Live Demo**

- **API Endpoint**: `https://your-deployed-url.com/api-endpoint`
- **Health Check**: `https://your-deployed-url.com/health`
- **Documentation**: `https://your-deployed-url.com/docs`

## ✨ **Features**

- 🤖 **AI-Powered Code Generation** using OpenAI GPT-4
- 🐙 **Automated GitHub Repository Creation** and deployment
- 📄 **GitHub Pages Integration** for instant hosting
- 🔄 **Multi-Round Support** for iterative development
- 📊 **Comprehensive Evaluation System** with automated scoring
- 🔒 **Secure Authentication** with secret validation
- ⚡ **Background Processing** for non-blocking operations

## 🎮 **Quick Start**

### **1. Deploy Instantly**

Click the Railway button above or:

```bash
# Clone and deploy to Railway
git clone <your-repo>
cd llm-deployment-api
railway up
```

### **2. Set Environment Variables**

```bash
USER_SECRET="TDS DEDLY"
GITHUB_TOKEN="your_github_token"
GITHUB_USERNAME="your_username"
OPENAI_API_KEY="your_openai_key"
OPENAI_BASE_URL="https://aipipe.org/openai/v1"
```

### **3. Test the API**

```bash
curl -X POST https://your-app.railway.app/api-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "TDS DEDLY",
    "task": "demo-task",
    "round": 1,
    "nonce": "unique-id",
    "brief": "Create a Bootstrap dashboard",
    "checks": ["Has MIT license", "Professional README"],
    "evaluation_url": "https://httpbin.org/post"
  }'
```

## 📋 **API Reference**

### **POST /api-endpoint**

Main endpoint for code generation and deployment requests.

**Request Body:**
```json
{
  "email": "student@example.com",
  "secret": "your_secret",
  "task": "unique-task-id",
  "round": 1,
  "nonce": "unique-nonce",
  "brief": "Detailed description of what to build",
  "checks": ["List of evaluation criteria"],
  "evaluation_url": "https://evaluation-server.com/notify",
  "attachments": [{"name": "file.csv", "url": "data:text/csv;base64,..."}]
}
```

**Response:**
```json
{
  "status": "accepted",
  "note": "processing round 1 started"
}
```

### **GET /health**

Health check endpoint with configuration status.

### **GET /**

API information and version.

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Student API   │───▶│   LLM Generator  │───▶│  GitHub Pages   │
│   (FastAPI)     │    │   (OpenAI GPT-4) │    │   (Deployment)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Evaluation     │    │   Background     │    │   Notification  │
│   Server        │    │   Processing     │    │    System       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 **Local Development**

```bash
# Clone repository
git clone <your-repo>
cd llm-deployment-api

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run locally
uvicorn app.main:app --reload
```

## 📊 **Monitoring & Analytics**

- **Health Monitoring**: Built-in health checks
- **Request Logging**: Comprehensive request/response logging
- **Error Tracking**: Detailed error reporting
- **Performance Metrics**: Response time and success rate tracking

## 🔒 **Security**

- ✅ Secret-based authentication
- ✅ Input validation and sanitization
- ✅ Rate limiting ready
- ✅ No sensitive data in logs
- ✅ Secure environment variable handling

## 📈 **Production Features**

- ⚡ **Async Processing**: Non-blocking background tasks
- 🔄 **Retry Logic**: Exponential backoff for external APIs
- 📝 **Comprehensive Logging**: Detailed operation tracking
- 🛡️ **Error Handling**: Graceful failure recovery
- 🎯 **Health Checks**: Built-in monitoring endpoints

## 🤝 **Contributing**

This is a production-ready implementation of the LLM Code Deployment project. The system handles:

1. **Code Generation**: AI-powered application creation
2. **GitHub Integration**: Automated repository and Pages deployment
3. **Evaluation Pipeline**: Comprehensive testing and scoring
4. **Multi-Round Support**: Iterative development workflow

## 📄 **License**

MIT License - see LICENSE file for details.

---

**🚀 Ready for production deployment!** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.


