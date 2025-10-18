@echo off
echo 🧹 Clean upload to GitHub...

REM Initialize fresh git repo
git init
git branch -M main

REM Add remote
git remote add origin https://github.com/anupp29/llm-code-deployment-api.git

REM Add files (excluding sensitive ones)
git add .

REM Commit
git commit -m "Initial commit - LLM Code Deployment API"

REM Force push to overwrite history
git push -f origin main

echo ✅ Clean upload completed!
echo 🌐 Repository: https://github.com/anupp29/llm-code-deployment-api
