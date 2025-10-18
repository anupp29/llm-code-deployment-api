@echo off
setlocal

if "%1"=="" (
    echo Usage: upload-to-github.bat [GITHUB_USERNAME] [REPO_NAME]
    echo Example: upload-to-github.bat anupp29 llm-code-deployment-api
    exit /b 1
)

if "%2"=="" (
    echo Usage: upload-to-github.bat [GITHUB_USERNAME] [REPO_NAME]
    echo Example: upload-to-github.bat anupp29 llm-code-deployment-api
    exit /b 1
)

set GITHUB_USERNAME=%1
set REPO_NAME=%2

echo 🐙 Uploading to GitHub Repository...
echo Username: %GITHUB_USERNAME%
echo Repository: %REPO_NAME%

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    exit /b 1
)

REM Initialize git repository
echo 📁 Initializing git repository...
git init

REM Add remote origin
set REPO_URL=https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
echo 🔗 Adding remote origin: %REPO_URL%
git remote add origin %REPO_URL%

REM Create .gitignore if it doesn't exist
if not exist .gitignore (
    echo # Python
    echo __pycache__/
    echo *.pyc
    echo .env
    echo *.db
    echo .vercel
    echo temp-hf-space/
) > .gitignore

echo 📦 Adding files...
git add .

echo 📝 Committing files...
git commit -m "Initial commit: LLM Code Deployment API"

echo 📤 Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo ❌ Failed to push to GitHub
    echo Make sure:
    echo 1. Repository exists: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo 2. You have push permissions
    echo 3. Git credentials are configured
    exit /b 1
)

echo 🎉 Successfully uploaded to GitHub!
echo 🌐 Repository URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo 📖 View your code: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%

echo.
echo 🔧 Next steps:
echo 1. Make sure repository is PUBLIC before deadline
echo 2. Add a good README.md description
echo 3. Submit this URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
