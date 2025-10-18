# 🤗 Deploy to Hugging Face Spaces

**Hugging Face Spaces is PERFECT for your LLM Code Deployment API!**

## 🎯 Why Hugging Face Spaces?

- ✅ **FREE** hosting for public spaces
- ✅ **No timeout limits** (unlike Vercel)
- ✅ **Background tasks** supported
- ✅ **Persistent storage** available
- ✅ **Perfect for AI apps** 
- ✅ **Easy environment variables**
- ✅ **Docker support**
- ✅ **Auto-scaling**

## 🚀 Deployment Steps

### **Step 1: Create a New Space**

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Space name**: `llm-code-deployment-api`
   - **License**: `MIT`
   - **SDK**: `Docker`
   - **Hardware**: `CPU basic` (free)
   - **Visibility**: `Public` (for free tier)

### **Step 2: Upload Your Code**

You have two options:

#### **Option A: Git Upload (Recommended)**

```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/llm-code-deployment-api
cd llm-code-deployment-api

# Copy your files (from your current directory)
cp -r ../tds-project-1-main/* .

# Rename files for Hugging Face
mv README_HF.md README.md
mv Dockerfile.hf Dockerfile

# Add, commit and push
git add .
git commit -m "Initial deployment of LLM Code Deployment API"
git push
```

#### **Option B: Web Upload**

1. Go to your space page
2. Click "Files" → "Upload files"
3. Upload all your project files
4. Rename `README_HF.md` to `README.md`
5. Rename `Dockerfile.hf` to `Dockerfile`

### **Step 3: Set Environment Variables**

1. Go to your Space settings
2. Click "Variables and secrets"
3. Add these environment variables:

```bash
USER_SECRET = TDS DEDLY
GITHUB_TOKEN = your_github_token_here
GITHUB_USERNAME = your_github_username
OPENAI_API_KEY = your_openai_api_key
OPENAI_BASE_URL = https://aipipe.org/openai/v1
```

### **Step 4: Wait for Build**

- Your space will automatically build and deploy
- Check the "Logs" tab for build progress
- Build typically takes 3-5 minutes

## 🧪 Testing Your Deployed API

Once deployed, your API will be available at:
`https://YOUR_USERNAME-llm-code-deployment-api.hf.space`

### **Health Check**
```bash
curl https://YOUR_USERNAME-llm-code-deployment-api.hf.space/health
```

### **API Documentation**
Visit: `https://YOUR_USERNAME-llm-code-deployment-api.hf.space/docs`

### **Test Request**
```bash
curl -X POST https://YOUR_USERNAME-llm-code-deployment-api.hf.space/api-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "email": "23f2003212@ds.study.iitm.ac.in",
    "secret": "TDS DEDLY",
    "task": "demo-task",
    "round": 1,
    "nonce": "unique-id",
    "brief": "Create a simple Bootstrap webpage",
    "checks": ["Has MIT license"],
    "evaluation_url": "https://httpbin.org/post"
  }'
```

## 🎯 Advantages over Vercel

| Feature | Hugging Face | Vercel |
|---------|--------------|---------|
| **Timeout** | ✅ No limits | ❌ 60s max |
| **Background Tasks** | ✅ Supported | ❌ Limited |
| **Cost** | ✅ Free | ✅ Free (limited) |
| **AI Focus** | ✅ Perfect | ⚠️ Generic |
| **Docker** | ✅ Full support | ❌ Limited |
| **Persistent Storage** | ✅ Available | ❌ No |
| **Community** | ✅ AI-focused | ⚠️ General |

## 🔧 Advanced Configuration

### **Custom Domain**
- Available on Pro plan ($9/month)
- Point your domain to the Space

### **Private Spaces**
- Available on Pro plan
- Keep your API private

### **GPU Support**
- Available for compute-intensive tasks
- Not needed for your current API

### **Persistent Storage**
- Available for databases
- Useful for evaluation data

## 🚀 Quick Deploy Script

Save this as `deploy-to-hf.sh`:

```bash
#!/bin/bash
echo "🤗 Deploying to Hugging Face Spaces..."

# Set your Hugging Face username
HF_USERNAME="your-username"
SPACE_NAME="llm-code-deployment-api"

# Clone the space
git clone https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME
cd $SPACE_NAME

# Copy files
cp -r ../tds-project-1-main/* .
mv README_HF.md README.md
mv Dockerfile.hf Dockerfile

# Deploy
git add .
git commit -m "Deploy LLM Code Deployment API"
git push

echo "✅ Deployed! Check: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
```

## 🎉 Benefits of Hugging Face Deployment

1. **🔄 Better for Background Tasks**: No timeout issues
2. **💾 Persistent Data**: Can store evaluation results
3. **🤖 AI Community**: Perfect audience for your API
4. **📊 Usage Analytics**: Built-in metrics
5. **🔒 Environment Variables**: Secure secret management
6. **📖 Auto Documentation**: FastAPI docs work perfectly
7. **🌐 Global CDN**: Fast worldwide access

---

**🚀 Hugging Face Spaces is the BEST choice for your LLM Code Deployment API!**

Much better than Vercel for this type of application. No timeouts, full Docker support, and perfect for AI applications! 🎯
