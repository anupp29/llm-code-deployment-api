#!/usr/bin/env python3
"""
Round 2 evaluation script - sends follow-up tasks to students
"""

import requests
import random
from evaluation.database import init_database, get_repos, add_task, task_exists
from evaluation.task_templates import TASK_TEMPLATES, create_task_from_template

def send_round2_tasks(evaluation_url: str = "http://localhost:8001/notify"):
    """Send Round 2 tasks to students who completed Round 1"""
    print("🔄 Starting Round 2 task distribution...")
    
    # Initialize database
    init_database()
    
    # Get all Round 1 repositories
    round1_repos = get_repos(round_num=1)
    
    if not round1_repos:
        print("📭 No Round 1 repositories found")
        return []
    
    print(f"📋 Found {len(round1_repos)} Round 1 submissions")
    
    results = []
    
    for repo_data in round1_repos:
        # repo_data structure: (id, timestamp, email, task, round, nonce, repo_url, commit_sha, pages_url)
        repo_id, timestamp, email, task, round_num, nonce, repo_url, commit_sha, pages_url = repo_data
        
        print(f"\n👤 Processing Round 2 for {email}")
        print(f"   Original task: {task}")
        
        # Check if Round 2 task already sent successfully
        if task_exists(email, task.split('-')[0], 2):  # Check by template prefix
            print(f"⚠️ Round 2 task already sent successfully for {email}")
            continue
        
        # Extract template ID from original task
        template_id = task.split('-')[0]  # e.g., "sum-of-sales-abc123" -> "sum-of-sales"
        
        if template_id not in TASK_TEMPLATES:
            print(f"⚠️ Unknown template ID: {template_id}")
            continue
        
        print(f"🎯 Using template: {template_id}")
        
        # Get student endpoint from database (we need to store this)
        # For now, we'll use the same endpoint as Round 1
        endpoint = "http://localhost:8000/api-endpoint"  # This should come from the database
        
        try:
            # Create Round 2 task from template
            task_data = create_task_from_template(
                template_id=template_id,
                email=email,
                round_num=2,
                evaluation_url=evaluation_url
            )
            
            print(f"📝 Generated Round 2 task: {task_data['task']}")
            print(f"📄 Brief: {task_data['brief'][:100]}...")
            
            # Send task to student endpoint
            headers = {"Content-Type": "application/json"}
            
            print(f"📤 Sending Round 2 task to {endpoint}")
            response = requests.post(endpoint, json=task_data, headers=headers, timeout=30)
            
            status_code = response.status_code
            print(f"📨 Response: {status_code} - {response.text[:200]}")
            
            # Log task to database
            add_task(email, task_data, endpoint, status_code)
            
            results.append({
                "email": email,
                "original_task": task,
                "round2_task": task_data["task"],
                "template": template_id,
                "status_code": status_code,
                "success": status_code == 200
            })
            
            if status_code == 200:
                print(f"✅ Round 2 task sent successfully to {email}")
            else:
                print(f"❌ Failed to send Round 2 task to {email}: {status_code}")
                
        except Exception as e:
            print(f"❌ Error processing Round 2 for {email}: {e}")
            results.append({
                "email": email,
                "original_task": task,
                "round2_task": None,
                "template": template_id,
                "status_code": None,
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print(f"\n📊 Round 2 Summary:")
    print(f"   Round 1 submissions: {len(round1_repos)}")
    successful = sum(1 for r in results if r.get("success", False))
    print(f"   Successful Round 2 sends: {successful}")
    print(f"   Failed Round 2 sends: {len(results) - successful}")
    
    return results

def main():
    """Main function for Round 2 script"""
    print("=" * 60)
    print("🔄 LLM Code Deployment - Round 2 Task Distribution")
    print("=" * 60)
    
    # You can customize the evaluation URL here
    evaluation_url = "http://localhost:8001/notify"
    
    results = send_round2_tasks(evaluation_url)
    
    print(f"\n🏁 Round 2 distribution completed!")
    print(f"Check the evaluation database for detailed logs.")

if __name__ == "__main__":
    main()
