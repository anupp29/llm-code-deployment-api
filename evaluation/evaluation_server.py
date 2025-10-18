#!/usr/bin/env python3
"""
Evaluation server - receives notifications from student APIs
"""

from fastapi import FastAPI, Request, HTTPException
import uvicorn
from datetime import datetime
from evaluation.database import init_database, add_repo, get_tasks

app = FastAPI(title="LLM Code Deployment Evaluation Server", version="1.0.0")

# Store notifications for inspection
notifications_log = []

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_database()

@app.get("/")
async def root():
    return {
        "message": "LLM Code Deployment Evaluation Server",
        "notifications_received": len(notifications_log)
    }

@app.get("/notifications")
async def get_notifications():
    """Get all received notifications"""
    return {
        "notifications": notifications_log,
        "count": len(notifications_log)
    }

@app.post("/notify")
async def receive_notification(request: Request):
    """
    Receive notification from student API
    
    Expected payload:
    {
        "email": "student@example.com",
        "task": "task-id",
        "round": 1,
        "nonce": "uuid",
        "repo_url": "https://github.com/user/repo",
        "commit_sha": "abc123",
        "pages_url": "https://user.github.io/repo/"
    }
    """
    try:
        data = await request.json()
        
        # Validate required fields
        required_fields = ["email", "task", "round", "nonce"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields: {missing_fields}"
            )
        
        # Check if this notification matches a sent task
        email = data["email"]
        task = data["task"]
        round_num = data["round"]
        nonce = data["nonce"]
        
        # Query database to verify this is a valid task
        tasks = get_tasks(email=email, round_num=round_num)
        valid_task = False
        
        for task_row in tasks:
            # task_row structure: (id, timestamp, email, task, round, nonce, brief, attachments, checks, evaluation_url, endpoint, statuscode, secret)
            if task_row[3] == task and task_row[5] == nonce:  # task and nonce match
                valid_task = True
                break
        
        if not valid_task:
            print(f"⚠️ Invalid notification received: {email}, {task}, round {round_num}, nonce {nonce}")
            raise HTTPException(
                status_code=400,
                detail="Invalid task/nonce combination"
            )
        
        # Add notification to log
        notification = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        notifications_log.append(notification)
        
        # Add to repos database if repo_url is provided
        if "repo_url" in data:
            success = add_repo(data)
            if success:
                print(f"✅ Added repo to database: {data['repo_url']}")
            else:
                print(f"⚠️ Failed to add repo to database")
        
        print(f"📩 Received valid notification #{len(notifications_log)}:")
        print(f"   Email: {email}")
        print(f"   Task: {task}")
        print(f"   Round: {round_num}")
        print(f"   Repo: {data.get('repo_url', 'Not provided')}")
        print(f"   Pages: {data.get('pages_url', 'Not provided')}")
        
        return {
            "status": "received",
            "notification_id": len(notifications_log),
            "message": "Notification processed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing notification: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/notifications")
async def clear_notifications():
    """Clear all notifications (for testing)"""
    global notifications_log
    count = len(notifications_log)
    notifications_log = []
    return {"message": f"Cleared {count} notifications"}

@app.get("/stats")
async def get_stats():
    """Get evaluation statistics"""
    from evaluation.database import get_repos, get_results
    
    repos = get_repos()
    results = get_results()
    
    # Group by email and round
    stats = {}
    
    for repo in repos:
        # repo structure: (id, timestamp, email, task, round, nonce, repo_url, commit_sha, pages_url)
        email = repo[2]
        round_num = repo[4]
        
        if email not in stats:
            stats[email] = {"round1": False, "round2": False, "repos": [], "results_count": 0}
        
        if round_num == 1:
            stats[email]["round1"] = True
        elif round_num == 2:
            stats[email]["round2"] = True
        
        stats[email]["repos"].append({
            "task": repo[3],
            "round": round_num,
            "repo_url": repo[6],
            "pages_url": repo[8]
        })
    
    # Count results
    for result in results:
        email = result[1]  # email is at index 1
        if email in stats:
            stats[email]["results_count"] += 1
    
    return {
        "total_students": len(stats),
        "round1_complete": sum(1 for s in stats.values() if s["round1"]),
        "round2_complete": sum(1 for s in stats.values() if s["round2"]),
        "total_repos": len(repos),
        "total_results": len(results),
        "students": stats
    }

if __name__ == "__main__":
    print("🎯 Starting LLM Code Deployment Evaluation Server...")
    print("This server receives notifications from student APIs")
    print("Available endpoints:")
    print("  GET  /           - Status")
    print("  GET  /notifications - View all notifications")
    print("  POST /notify     - Receive notifications (used by student APIs)")
    print("  GET  /stats      - View evaluation statistics")
    print("  DELETE /notifications - Clear all notifications")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
