@echo off
setlocal

if "%1"=="" (
    echo Usage: deploy-hf.bat [HF_USERNAME]
    echo Example: deploy-hf.bat zeolite29
    exit /b 1
)

set HF_USERNAME=%1
set SPACE_NAME=llm-code-deployment-api

echo 🤗 Deploying to Hugging Face Spaces...
echo Username: %HF_USERNAME%
echo Space: %SPACE_NAME%

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    exit /b 1
)

REM Clone the space repository
set SPACE_URL=https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%
echo 📥 Cloning space from %SPACE_URL%

git clone %SPACE_URL% temp-hf-space
if errorlevel 1 (
    echo ❌ Failed to clone space. Make sure the space exists at %SPACE_URL%
    exit /b 1
)

cd temp-hf-space

echo 📁 Copying files...

REM Copy essential files
copy ..\app.py . >nul
copy ..\requirements.txt . >nul
copy ..\runtime.txt . >nul
copy ..\README_HF.md README.md >nul
copy ..\Dockerfile.hf Dockerfile >nul
copy ..\.gitattributes . >nul
copy ..\.gitignore . >nul

REM Copy app directory
xcopy ..\app app\ /E /I /Y >nul

REM Copy evaluation directory  
xcopy ..\evaluation evaluation\ /E /I /Y >nul

REM Copy api directory
xcopy ..\api api\ /E /I /Y >nul

echo ✅ Files copied successfully

echo 📤 Committing and pushing...
git add .
git commit -m "Deploy LLM Code Deployment API to Hugging Face Spaces"
git push

if errorlevel 1 (
    echo ❌ Failed to push to repository
    cd ..
    rmdir /s /q temp-hf-space
    exit /b 1
)

echo 🎉 Successfully deployed!
echo 🌐 Your API will be available at: https://%HF_USERNAME%-%SPACE_NAME%.hf.space
echo 📖 Documentation: https://%HF_USERNAME%-%SPACE_NAME%.hf.space/docs

REM Clean up
cd ..
rmdir /s /q temp-hf-space

echo.
echo 🔧 Next steps:
echo 1. Go to https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%/settings
echo 2. Add your environment variables in Variables and secrets
echo 3. Wait for the build to complete (3-5 minutes)
echo 4. Test your API!

echo.
echo 🔑 Environment variables to add:
echo USER_SECRET = TDS DEDLY
echo GITHUB_TOKEN = your_github_token_here
echo GITHUB_USERNAME = your_github_username
echo OPENAI_API_KEY = your_openai_api_key
echo OPENAI_BASE_URL = https://aipipe.org/openai/v1
