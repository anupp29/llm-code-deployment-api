#!/usr/bin/env python3
"""
Round 1 evaluation script - sends initial tasks to students
"""

import requests
import random
from datetime import datetime
from evaluation.database import init_database, add_task, task_exists, add_submission
from evaluation.task_templates import TASK_TEMPLATES, create_task_from_template

# Sample submissions for testing
SAMPLE_SUBMISSIONS = [
    {
        "email": "23f2003212@ds.study.iitm.ac.in",
        "endpoint": "http://localhost:8000/api-endpoint",
        "secret": "TDS DEDLY"
    }
]

def load_submissions():
    """Load submissions from CSV or use sample data"""
    # In production, this would read from submissions.csv
    # For now, we'll use the sample data and add your actual endpoint
    return SAMPLE_SUBMISSIONS

def send_round1_tasks(evaluation_url: str = "http://localhost:8001/notify"):
    """Send Round 1 tasks to all student submissions"""
    print("🚀 Starting Round 1 task distribution...")
    
    # Initialize database
    init_database()
    
    # Load submissions
    submissions = load_submissions()
    print(f"📋 Found {len(submissions)} submissions")
    
    results = []
    
    for submission in submissions:
        email = submission["email"]
        endpoint = submission["endpoint"]
        secret = submission["secret"]
        
        print(f"\n👤 Processing submission for {email}")
        
        # Add submission to database
        add_submission(email, endpoint, secret)
        
        # Check if Round 1 task already sent successfully
        if task_exists(email, "", 1):  # Empty task means any task for round 1
            print(f"⚠️ Round 1 task already sent successfully for {email}")
            continue
        
        # Pick a random template
        template_ids = list(TASK_TEMPLATES.keys())
        template_id = random.choice(template_ids)
        
        print(f"🎯 Selected template: {template_id}")
        
        try:
            # Create task from template
            task_data = create_task_from_template(
                template_id=template_id,
                email=email,
                round_num=1,
                evaluation_url=evaluation_url
            )
            
            print(f"📝 Generated task: {task_data['task']}")
            print(f"📄 Brief: {task_data['brief'][:100]}...")
            
            # Send task to student endpoint
            headers = {"Content-Type": "application/json"}
            
            print(f"📤 Sending task to {endpoint}")
            response = requests.post(endpoint, json=task_data, headers=headers, timeout=30)
            
            status_code = response.status_code
            print(f"📨 Response: {status_code} - {response.text[:200]}")
            
            # Log task to database
            add_task(email, task_data, endpoint, status_code)
            
            results.append({
                "email": email,
                "task": task_data["task"],
                "template": template_id,
                "status_code": status_code,
                "success": status_code == 200
            })
            
            if status_code == 200:
                print(f"✅ Task sent successfully to {email}")
            else:
                print(f"❌ Failed to send task to {email}: {status_code}")
                
        except Exception as e:
            print(f"❌ Error processing {email}: {e}")
            results.append({
                "email": email,
                "task": None,
                "template": template_id,
                "status_code": None,
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print(f"\n📊 Round 1 Summary:")
    print(f"   Total submissions: {len(submissions)}")
    successful = sum(1 for r in results if r.get("success", False))
    print(f"   Successful sends: {successful}")
    print(f"   Failed sends: {len(results) - successful}")
    
    return results

def main():
    """Main function for Round 1 script"""
    print("=" * 60)
    print("🎯 LLM Code Deployment - Round 1 Task Distribution")
    print("=" * 60)
    
    # You can customize the evaluation URL here
    evaluation_url = "http://localhost:8001/notify"
    
    results = send_round1_tasks(evaluation_url)
    
    print(f"\n🏁 Round 1 distribution completed!")
    print(f"Check the evaluation database for detailed logs.")

if __name__ == "__main__":
    main()
