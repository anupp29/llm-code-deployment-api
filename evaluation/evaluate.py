#!/usr/bin/env python3
"""
Evaluation script - evaluates submitted repositories
"""

import requests
import base64
import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
from evaluation.database import init_database, get_repos, add_result
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def check_mit_license(repo_url: str, commit_sha: str) -> tuple[float, str]:
    """Check if repository has MIT license"""
    try:
        # Extract owner/repo from URL
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            return 0.0, "Invalid repository URL format"
        
        owner, repo = match.groups()
        
        # Check for LICENSE file
        license_url = f"https://api.github.com/repos/{owner}/{repo}/contents/LICENSE"
        
        response = requests.get(license_url)
        if response.status_code != 200:
            return 0.0, "No LICENSE file found in repository root"
        
        # Get license content
        content_data = response.json()
        license_content = base64.b64decode(content_data['content']).decode('utf-8')
        
        # Check if it's MIT license
        mit_indicators = [
            "MIT License",
            "Permission is hereby granted, free of charge",
            "THE SOFTWARE IS PROVIDED \"AS IS\""
        ]
        
        mit_score = sum(1 for indicator in mit_indicators if indicator in license_content)
        
        if mit_score >= 2:
            return 1.0, "Valid MIT license found"
        else:
            return 0.3, f"License file exists but may not be MIT (score: {mit_score}/3)"
            
    except Exception as e:
        return 0.0, f"Error checking license: {str(e)}"

def evaluate_readme_quality(repo_url: str, commit_sha: str) -> tuple[float, str]:
    """Evaluate README.md quality using LLM"""
    try:
        # Extract owner/repo from URL
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            return 0.0, "Invalid repository URL format"
        
        owner, repo = match.groups()
        
        # Get README content
        readme_url = f"https://api.github.com/repos/{owner}/{repo}/contents/README.md"
        
        response = requests.get(readme_url)
        if response.status_code != 200:
            return 0.0, "No README.md file found"
        
        content_data = response.json()
        readme_content = base64.b64decode(content_data['content']).decode('utf-8')
        
        # Use LLM to evaluate README quality
        prompt = f"""
        Evaluate the quality of this README.md file for a web application project.
        
        README Content:
        {readme_content}
        
        Rate the README on a scale of 0.0 to 1.0 based on:
        - Clarity and professionalism
        - Completeness (setup, usage, description)
        - Structure and formatting
        - Code explanation (if applicable)
        
        Respond with just a number between 0.0 and 1.0, followed by a brief explanation.
        Format: SCORE: 0.X - Explanation here
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a technical documentation evaluator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        result = response.choices[0].message.content.strip()
        
        # Extract score and explanation
        if "SCORE:" in result:
            parts = result.split("SCORE:", 1)[1].strip()
            score_part = parts.split("-", 1)[0].strip()
            explanation = parts.split("-", 1)[1].strip() if "-" in parts else "LLM evaluation"
            
            try:
                score = float(score_part)
                return max(0.0, min(1.0, score)), explanation
            except ValueError:
                return 0.5, f"Could not parse LLM score: {result}"
        else:
            return 0.5, f"Unexpected LLM response format: {result}"
            
    except Exception as e:
        return 0.0, f"Error evaluating README: {str(e)}"

def evaluate_code_quality(repo_url: str, commit_sha: str) -> tuple[float, str]:
    """Evaluate code quality using LLM"""
    try:
        # Extract owner/repo from URL
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            return 0.0, "Invalid repository URL format"
        
        owner, repo = match.groups()
        
        # Get repository contents
        contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        response = requests.get(contents_url)
        
        if response.status_code != 200:
            return 0.0, "Could not access repository contents"
        
        contents = response.json()
        
        # Find and analyze main code files
        code_files = []
        for item in contents:
            if item['name'].endswith(('.html', '.js', '.css', '.py')) and item['type'] == 'file':
                file_response = requests.get(item['download_url'])
                if file_response.status_code == 200:
                    code_files.append({
                        'name': item['name'],
                        'content': file_response.text[:2000]  # Limit content length
                    })
        
        if not code_files:
            return 0.0, "No code files found"
        
        # Prepare code for LLM evaluation
        code_summary = "\n\n".join([
            f"File: {f['name']}\n{f['content']}" for f in code_files[:3]  # Limit to 3 files
        ])
        
        prompt = f"""
        Evaluate the quality of this web application code.
        
        Code Files:
        {code_summary}
        
        Rate the code on a scale of 0.0 to 1.0 based on:
        - Code structure and organization
        - Functionality and completeness
        - Best practices and standards
        - Error handling
        
        Respond with just a number between 0.0 and 1.0, followed by a brief explanation.
        Format: SCORE: 0.X - Explanation here
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code quality evaluator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        result = response.choices[0].message.content.strip()
        
        # Extract score and explanation
        if "SCORE:" in result:
            parts = result.split("SCORE:", 1)[1].strip()
            score_part = parts.split("-", 1)[0].strip()
            explanation = parts.split("-", 1)[1].strip() if "-" in parts else "LLM evaluation"
            
            try:
                score = float(score_part)
                return max(0.0, min(1.0, score)), explanation
            except ValueError:
                return 0.5, f"Could not parse LLM score: {result}"
        else:
            return 0.5, f"Unexpected LLM response format: {result}"
            
    except Exception as e:
        return 0.0, f"Error evaluating code: {str(e)}"

def run_playwright_checks(pages_url: str, checks: list) -> list:
    """Run dynamic checks using Playwright"""
    results = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to the page
            try:
                page.goto(pages_url, timeout=30000)
                page.wait_for_load_state('networkidle', timeout=10000)
            except Exception as e:
                browser.close()
                return [{"check": "page_load", "score": 0.0, "reason": f"Failed to load page: {str(e)}"}]
            
            # Run each check
            for i, check in enumerate(checks):
                check_name = f"check_{i+1}"
                
                try:
                    if check.startswith("js:"):
                        # JavaScript check
                        js_code = check[3:].strip()
                        result = page.evaluate(js_code)
                        
                        if result is True:
                            results.append({"check": check_name, "score": 1.0, "reason": "Check passed"})
                        elif result is False:
                            results.append({"check": check_name, "score": 0.0, "reason": "Check failed"})
                        else:
                            # Treat truthy/falsy values
                            score = 1.0 if result else 0.0
                            results.append({"check": check_name, "score": score, "reason": f"Result: {result}"})
                    else:
                        # Other types of checks can be added here
                        results.append({"check": check_name, "score": 0.0, "reason": "Unknown check type"})
                        
                except Exception as e:
                    results.append({"check": check_name, "score": 0.0, "reason": f"Check error: {str(e)}"})
            
            browser.close()
            
    except Exception as e:
        results.append({"check": "playwright_setup", "score": 0.0, "reason": f"Playwright error: {str(e)}"})
    
    return results

def evaluate_repository(repo_data: tuple) -> list:
    """Evaluate a single repository submission"""
    # repo_data structure: (id, timestamp, email, task, round, nonce, repo_url, commit_sha, pages_url)
    repo_id, timestamp, email, task, round_num, nonce, repo_url, commit_sha, pages_url = repo_data
    
    print(f"\n🔍 Evaluating {email} - {task} (Round {round_num})")
    print(f"   Repo: {repo_url}")
    print(f"   Pages: {pages_url}")
    
    results = []
    
    # 1. Check MIT License
    print("   📄 Checking MIT license...")
    license_score, license_reason = check_mit_license(repo_url, commit_sha)
    results.append({
        "check": "mit_license",
        "score": license_score,
        "reason": license_reason
    })
    
    # 2. Evaluate README quality
    print("   📖 Evaluating README quality...")
    readme_score, readme_reason = evaluate_readme_quality(repo_url, commit_sha)
    results.append({
        "check": "readme_quality",
        "score": readme_score,
        "reason": readme_reason
    })
    
    # 3. Evaluate code quality
    print("   💻 Evaluating code quality...")
    code_score, code_reason = evaluate_code_quality(repo_url, commit_sha)
    results.append({
        "check": "code_quality",
        "score": code_score,
        "reason": code_reason
    })
    
    # 4. Run dynamic checks if pages_url is available
    if pages_url:
        print("   🌐 Running dynamic checks...")
        
        # For now, we'll run basic page load and structure checks
        # In a real implementation, you'd get the original task checks from the database
        basic_checks = [
            "js: document.title.length > 0",
            "js: document.body.children.length > 0",
            "js: !!document.querySelector('html')"
        ]
        
        dynamic_results = run_playwright_checks(pages_url, basic_checks)
        results.extend(dynamic_results)
    else:
        results.append({
            "check": "pages_availability",
            "score": 0.0,
            "reason": "No pages URL provided"
        })
    
    # Store results in database
    for result in results:
        add_result(
            email=email,
            task=task,
            round_num=round_num,
            repo_url=repo_url,
            commit_sha=commit_sha,
            pages_url=pages_url,
            check_name=result["check"],
            score=result["score"],
            reason=result["reason"]
        )
    
    # Calculate overall score
    total_score = sum(r["score"] for r in results) / len(results) if results else 0.0
    print(f"   📊 Overall score: {total_score:.2f}")
    
    return results

def main():
    """Main evaluation function"""
    print("=" * 60)
    print("🔍 LLM Code Deployment - Repository Evaluation")
    print("=" * 60)
    
    # Initialize database
    init_database()
    
    # Get all repositories to evaluate
    repos = get_repos()
    
    if not repos:
        print("📭 No repositories found to evaluate")
        return
    
    print(f"📋 Found {len(repos)} repositories to evaluate")
    
    evaluated_count = 0
    
    for repo_data in repos:
        try:
            results = evaluate_repository(repo_data)
            evaluated_count += 1
            
        except Exception as e:
            email = repo_data[2]
            task = repo_data[3]
            print(f"❌ Error evaluating {email} - {task}: {e}")
    
    print(f"\n📊 Evaluation Summary:")
    print(f"   Total repositories: {len(repos)}")
    print(f"   Successfully evaluated: {evaluated_count}")
    print(f"   Failed evaluations: {len(repos) - evaluated_count}")
    
    print(f"\n🏁 Evaluation completed!")

if __name__ == "__main__":
    main()
