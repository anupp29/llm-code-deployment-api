#!/usr/bin/env python3
"""
Vercel-compatible version of the main app
This version processes requests synchronously to work within Vercel's timeout limits
"""

from fastapi import FastAPI, Request
import os, json, base64
from dotenv import load_dotenv
from app.llm_generator import generate_app_code, decode_attachments
from app.github_utils import (
    create_repo,
    create_or_update_file,
    enable_pages,
    generate_mit_license,
)
from app.notify import notify_evaluation_server
from app.github_utils import create_or_update_binary_file

load_dotenv()
USER_SECRET = os.getenv("USER_SECRET")
USERNAME = os.getenv("GITHUB_USERNAME")

app = FastAPI(title="LLM Code Deployment API (Vercel)", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "LLM Code Deployment API (Vercel)", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    config_status = {
        "user_secret": bool(USER_SECRET),
        "github_username": bool(USERNAME),
        "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
        "github_token": bool(os.getenv("GITHUB_TOKEN"))
    }
    
    all_configured = all(config_status.values())
    
    return {
        "status": "healthy" if all_configured else "configuration_incomplete",
        "configuration": config_status,
        "platform": "vercel"
    }

def process_request_sync(data):
    """Synchronous version of request processing for Vercel"""
    round_num = data.get("round", 1)
    task_id = data["task"]
    print(f"⚙ Processing task {task_id} (round {round_num}) synchronously")
    
    try:
        attachments = data.get("attachments", [])
        saved_attachments = decode_attachments(attachments)
        print("Attachments saved:", saved_attachments)

        # Optional: fetch previous README for round 2
        prev_readme = None
        if round_num == 2:
            try:
                repo = create_repo(task_id, description=f"Auto-generated app for task: {data['brief']}")
                readme = repo.get_contents("README.md")
                prev_readme = readme.decoded_content.decode("utf-8", errors="ignore")
                print("📖 Loaded previous README for round 2 context.")
            except Exception:
                prev_readme = None

        gen = generate_app_code(
            data["brief"],
            attachments=attachments,
            checks=data.get("checks", []),
            round_num=round_num,
            prev_readme=prev_readme
        )

        files = gen.get("files", {})
        saved_info = gen.get("attachments", [])

        # Step 1: Get or create repo
        repo = create_repo(task_id, description=f"Auto-generated app for task: {data['brief']}")

        # Step 2: Round-specific logic
        if round_num == 1:
            print("🏗 Round 1: Building fresh repo...")
            # Add attachments
            for att in saved_info:
                path = att["name"]
                try:
                    with open(att["path"], "rb") as f:
                        content_bytes = f.read()
                    if att["mime"].startswith("text") or att["name"].endswith((".md", ".csv", ".json", ".txt")):
                        text = content_bytes.decode("utf-8", errors="ignore")
                        create_or_update_file(repo, path, text, f"Add attachment {path}")
                    else:
                        create_or_update_binary_file(repo, path, content_bytes, f"Add binary {path}")
                        b64 = base64.b64encode(content_bytes).decode("utf-8")
                        create_or_update_file(repo, f"attachments/{att['name']}.b64", b64, f"Backup {att['name']}.b64")
                except Exception as e:
                    print("⚠ Attachment commit failed:", e)
        else:
            print("🔁 Round 2: Revising existing repo...")

        # Step 3: Common steps for both rounds
        for fname, content in files.items():
            create_or_update_file(repo, fname, content, f"Add/Update {fname}")

        mit_text = generate_mit_license()
        create_or_update_file(repo, "LICENSE", mit_text, "Add MIT license")

        # Step 6: Handle GitHub Pages enablement
        if data["round"] == 1:
            pages_ok = enable_pages(task_id)
            pages_url = f"https://{USERNAME}.github.io/{task_id}/" if pages_ok else None
        else:
            pages_ok = True
            pages_url = f"https://{USERNAME}.github.io/{task_id}/"

        try:
            commit_sha = repo.get_commits()[0].sha
        except Exception:
            commit_sha = None

        payload = {
            "email": data["email"],
            "task": data["task"],
            "round": round_num,
            "nonce": data["nonce"],
            "repo_url": repo.html_url,
            "commit_sha": commit_sha,
            "pages_url": pages_url,
        }

        # Send notification synchronously
        notify_evaluation_server(data["evaluation_url"], payload)

        print(f"✅ Finished round {round_num} for {task_id}")
        return payload
        
    except Exception as e:
        print(f"❌ Error processing request for task {task_id}: {e}")
        # Still try to notify with error status
        error_payload = {
            "email": data["email"],
            "task": data["task"],
            "round": round_num,
            "nonce": data["nonce"],
            "error": str(e),
            "repo_url": None,
            "commit_sha": None,
            "pages_url": None,
        }
        try:
            notify_evaluation_server(data["evaluation_url"], error_payload)
        except Exception as notify_error:
            print(f"❌ Failed to notify evaluation server about error: {notify_error}")
        
        raise e

@app.post("/api-endpoint")
async def receive_request(request: Request):
    """Synchronous version for Vercel compatibility"""
    try:
        data = await request.json()
        print("📩 Received request:", data)
    except Exception as e:
        print(f"❌ Failed to parse JSON: {e}")
        return {"error": "Invalid JSON format"}

    # Validate required fields
    required_fields = ["email", "secret", "task", "round", "nonce", "brief", "evaluation_url"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        print(f"❌ Missing required fields: {missing_fields}")
        return {"error": f"Missing required fields: {missing_fields}"}

    # Verify secret
    if not USER_SECRET:
        print("❌ USER_SECRET not configured")
        return {"error": "Server configuration error"}
    
    if data.get("secret") != USER_SECRET:
        print("❌ Invalid secret received.")
        return {"error": "Invalid secret"}

    try:
        # Process synchronously for Vercel
        result = process_request_sync(data)
        return {
            "status": "completed", 
            "note": f"processing round {data['round']} completed",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "note": "Processing failed"
        }
