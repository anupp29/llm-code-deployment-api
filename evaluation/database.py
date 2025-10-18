#!/usr/bin/env python3
"""
Database management for the evaluation system
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("evaluation_data.db")

def init_database():
    """Initialize the evaluation database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tasks table - for tracking sent tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            email TEXT NOT NULL,
            task TEXT NOT NULL,
            round INTEGER NOT NULL,
            nonce TEXT NOT NULL,
            brief TEXT NOT NULL,
            attachments TEXT,  -- JSON string
            checks TEXT,       -- JSON string
            evaluation_url TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            statuscode INTEGER,
            secret TEXT,
            UNIQUE(email, task, round, nonce)
        )
    """)
    
    # Repos table - for tracking submitted repositories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            email TEXT NOT NULL,
            task TEXT NOT NULL,
            round INTEGER NOT NULL,
            nonce TEXT NOT NULL,
            repo_url TEXT NOT NULL,
            commit_sha TEXT,
            pages_url TEXT,
            UNIQUE(email, task, round, nonce)
        )
    """)
    
    # Results table - for tracking evaluation results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            email TEXT NOT NULL,
            task TEXT NOT NULL,
            round INTEGER NOT NULL,
            repo_url TEXT NOT NULL,
            commit_sha TEXT,
            pages_url TEXT,
            check_name TEXT NOT NULL,
            score REAL NOT NULL,
            reason TEXT,
            logs TEXT
        )
    """)
    
    # Submissions table - for tracking student submissions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            email TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            secret TEXT NOT NULL,
            UNIQUE(email)
        )
    """)
    
    conn.commit()
    conn.close()

def add_task(email: str, task_data: dict, endpoint: str, status_code: int = None):
    """Add a task to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO tasks 
            (timestamp, email, task, round, nonce, brief, attachments, checks, 
             evaluation_url, endpoint, statuscode, secret)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            email,
            task_data["task"],
            task_data["round"],
            task_data["nonce"],
            task_data["brief"],
            json.dumps(task_data["attachments"]),
            json.dumps(task_data["checks"]),
            task_data["evaluation_url"],
            endpoint,
            status_code,
            task_data["secret"]
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding task: {e}")
        return False
    finally:
        conn.close()

def add_repo(repo_data: dict):
    """Add a repository submission to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO repos 
            (timestamp, email, task, round, nonce, repo_url, commit_sha, pages_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            repo_data["email"],
            repo_data["task"],
            repo_data["round"],
            repo_data["nonce"],
            repo_data["repo_url"],
            repo_data.get("commit_sha"),
            repo_data.get("pages_url")
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding repo: {e}")
        return False
    finally:
        conn.close()

def add_result(email: str, task: str, round_num: int, repo_url: str, commit_sha: str, 
               pages_url: str, check_name: str, score: float, reason: str = None, logs: str = None):
    """Add an evaluation result to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO results 
            (timestamp, email, task, round, repo_url, commit_sha, pages_url, 
             check_name, score, reason, logs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            email,
            task,
            round_num,
            repo_url,
            commit_sha,
            pages_url,
            check_name,
            score,
            reason,
            logs
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding result: {e}")
        return False
    finally:
        conn.close()

def get_tasks(email: str = None, round_num: int = None):
    """Get tasks from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if email:
        query += " AND email = ?"
        params.append(email)
    
    if round_num:
        query += " AND round = ?"
        params.append(round_num)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_repos(email: str = None, round_num: int = None):
    """Get repositories from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM repos WHERE 1=1"
    params = []
    
    if email:
        query += " AND email = ?"
        params.append(email)
    
    if round_num:
        query += " AND round = ?"
        params.append(round_num)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_results(email: str = None, task: str = None):
    """Get evaluation results from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM results WHERE 1=1"
    params = []
    
    if email:
        query += " AND email = ?"
        params.append(email)
    
    if task:
        query += " AND task = ?"
        params.append(task)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return results

def add_submission(email: str, endpoint: str, secret: str):
    """Add a student submission to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO submissions 
            (timestamp, email, endpoint, secret)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.utcnow().isoformat(),
            email,
            endpoint,
            secret
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding submission: {e}")
        return False
    finally:
        conn.close()

def get_submissions():
    """Get all student submissions"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM submissions")
    results = cursor.fetchall()
    conn.close()
    
    return results

def task_exists(email: str, task: str, round_num: int) -> bool:
    """Check if a task already exists for the given parameters"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) FROM tasks 
        WHERE email = ? AND task LIKE ? AND round = ? AND statuscode = 200
    """, (email, f"{task}%", round_num))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0

def repo_exists(email: str, task: str, round_num: int) -> bool:
    """Check if a repo submission exists for the given parameters"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) FROM repos 
        WHERE email = ? AND task LIKE ? AND round = ?
    """, (email, f"{task}%", round_num))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0
