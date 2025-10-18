# PowerShell script to deploy to Hugging Face Spaces
param(
    [Parameter(Mandatory=$true)]
    [string]$HFUsername,
    
    [string]$SpaceName = "llm-code-deployment-api"
)

Write-Host "🤗 Deploying to Hugging Face Spaces..." -ForegroundColor Green
Write-Host "Username: $HFUsername" -ForegroundColor Yellow
Write-Host "Space: $SpaceName" -ForegroundColor Yellow

# Check if git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Clone the space repository
$spaceUrl = "https://huggingface.co/spaces/$HFUsername/$SpaceName"
Write-Host "📥 Cloning space from $spaceUrl" -ForegroundColor Blue

try {
    git clone $spaceUrl temp-hf-space
    Set-Location temp-hf-space
    
    # Copy files (excluding git and temp directories)
    Write-Host "📁 Copying files..." -ForegroundColor Blue
    
    $excludePatterns = @(
        ".git",
        "temp-hf-space",
        "__pycache__",
        "*.pyc",
        ".env",
        "evaluation_data.db",
        ".vercel"
    )
    
    Get-ChildItem -Path ".." -Recurse | Where-Object {
        $item = $_
        $shouldExclude = $false
        foreach ($pattern in $excludePatterns) {
            if ($item.Name -like $pattern -or $item.FullName -like "*$pattern*") {
                $shouldExclude = $true
                break
            }
        }
        -not $shouldExclude
    } | Copy-Item -Destination . -Recurse -Force
    
    # Rename files for Hugging Face
    if (Test-Path "README_HF.md") {
        Move-Item "README_HF.md" "README.md" -Force
        Write-Host "✅ Renamed README_HF.md to README.md" -ForegroundColor Green
    }
    
    if (Test-Path "Dockerfile.hf") {
        Move-Item "Dockerfile.hf" "Dockerfile" -Force
        Write-Host "✅ Renamed Dockerfile.hf to Dockerfile" -ForegroundColor Green
    }
    
    # Add and commit files
    Write-Host "📤 Committing and pushing..." -ForegroundColor Blue
    git add .
    git commit -m "Deploy LLM Code Deployment API to Hugging Face Spaces"
    git push
    
    Write-Host "🎉 Successfully deployed!" -ForegroundColor Green
    Write-Host "🌐 Your API will be available at: https://$HFUsername-$SpaceName.hf.space" -ForegroundColor Cyan
    Write-Host "📖 Documentation: https://$HFUsername-$SpaceName.hf.space/docs" -ForegroundColor Cyan
    
    # Clean up
    Set-Location ..
    Remove-Item temp-hf-space -Recurse -Force
    
}
catch {
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Set-Location ..
    if (Test-Path temp-hf-space) {
        Remove-Item temp-hf-space -Recurse -Force
    }
    exit 1
}

Write-Host ""
Write-Host "🔧 Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://huggingface.co/spaces/$HFUsername/$SpaceName/settings" -ForegroundColor White
Write-Host "2. Add your environment variables in Variables and secrets" -ForegroundColor White
Write-Host "3. Wait for the build to complete (3-5 minutes)" -ForegroundColor White
Write-Host "4. Test your API!" -ForegroundColor White
