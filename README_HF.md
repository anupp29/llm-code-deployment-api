---
title: LLM Code Deployment API
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🎯 LLM Code Deployment API

**AI-powered code generation and GitHub deployment service**

This Space provides an API that:
- 🤖 Generates web applications using OpenAI GPT-4
- 🐙 Creates GitHub repositories automatically
- 📄 Deploys to GitHub Pages
- 🔄 Supports multi-round development
- 📊 Integrates with evaluation systems

## 🚀 API Endpoints

### POST /api-endpoint
Main endpoint for code generation requests

### GET /health
Health check and configuration status

### GET /docs
Interactive API documentation

## 🔧 Environment Variables Required

Set these in your Space settings:
- `USER_SECRET`: Authentication secret
- `GITHUB_TOKEN`: GitHub Personal Access Token
- `GITHUB_USERNAME`: Your GitHub username  
- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_BASE_URL`: OpenAI API base URL

## 📋 Usage

```bash
curl -X POST https://your-space.hf.space/api-endpoint \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "your_secret",
    "task": "demo-task",
    "round": 1,
    "nonce": "unique-id",
    "brief": "Create a Bootstrap dashboard",
    "evaluation_url": "https://httpbin.org/post"
  }'
```

## 🎯 Features

- ⚡ Fast API responses
- 🔄 Background processing
- 🛡️ Secure authentication
- 📊 Comprehensive logging
- 🌐 CORS enabled
- 📖 Auto-generated docs
