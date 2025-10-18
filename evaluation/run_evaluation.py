#!/usr/bin/env python3
"""
Complete evaluation runner - orchestrates the entire evaluation process
"""

import time
import argparse
from datetime import datetime
from evaluation.round1 import send_round1_tasks
from evaluation.round2 import send_round2_tasks
from evaluation.evaluate import main as run_evaluation
from evaluation.database import init_database, get_repos, get_results

def wait_for_submissions(timeout_minutes: int = 15):
    """Wait for student submissions to come in"""
    print(f"⏳ Waiting {timeout_minutes} minutes for student submissions...")
    
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60
    
    while time.time() - start_time < timeout_seconds:
        repos = get_repos()
        if repos:
            print(f"📦 Found {len(repos)} submissions so far...")
        
        time.sleep(30)  # Check every 30 seconds
    
    final_repos = get_repos()
    print(f"⏰ Timeout reached. Final count: {len(final_repos)} submissions")
    return final_repos

def print_evaluation_summary():
    """Print a comprehensive evaluation summary"""
    print("\n" + "=" * 60)
    print("📊 EVALUATION SUMMARY")
    print("=" * 60)
    
    # Get all data
    repos = get_repos()
    results = get_results()
    
    if not repos:
        print("📭 No submissions found")
        return
    
    # Group by student
    students = {}
    for repo in repos:
        email = repo[2]
        round_num = repo[4]
        
        if email not in students:
            students[email] = {"round1": None, "round2": None, "scores": {}}
        
        students[email][f"round{round_num}"] = {
            "task": repo[3],
            "repo_url": repo[6],
            "pages_url": repo[8],
            "timestamp": repo[1]
        }
    
    # Add scores
    for result in results:
        email = result[1]
        round_num = result[3]
        check_name = result[7]
        score = result[8]
        
        if email in students:
            round_key = f"round{round_num}"
            if round_key not in students[email]["scores"]:
                students[email]["scores"][round_key] = {}
            students[email]["scores"][round_key][check_name] = score
    
    # Print summary for each student
    for email, data in students.items():
        print(f"\n👤 {email}")
        print("-" * 40)
        
        # Round 1
        if data["round1"]:
            r1 = data["round1"]
            print(f"  🚀 Round 1: {r1['task']}")
            print(f"     Repo: {r1['repo_url']}")
            print(f"     Pages: {r1['pages_url']}")
            
            if "round1" in data["scores"]:
                scores = data["scores"]["round1"]
                avg_score = sum(scores.values()) / len(scores) if scores else 0
                print(f"     Score: {avg_score:.2f} ({len(scores)} checks)")
                for check, score in scores.items():
                    print(f"       {check}: {score:.2f}")
        else:
            print("  ❌ Round 1: Not completed")
        
        # Round 2
        if data["round2"]:
            r2 = data["round2"]
            print(f"  🔄 Round 2: {r2['task']}")
            print(f"     Repo: {r2['repo_url']}")
            print(f"     Pages: {r2['pages_url']}")
            
            if "round2" in data["scores"]:
                scores = data["scores"]["round2"]
                avg_score = sum(scores.values()) / len(scores) if scores else 0
                print(f"     Score: {avg_score:.2f} ({len(scores)} checks)")
                for check, score in scores.items():
                    print(f"       {check}: {score:.2f}")
        else:
            print("  ⚠️ Round 2: Not completed")
    
    # Overall statistics
    print(f"\n📈 OVERALL STATISTICS")
    print("-" * 40)
    print(f"Total students: {len(students)}")
    print(f"Round 1 completed: {sum(1 for s in students.values() if s['round1'])}")
    print(f"Round 2 completed: {sum(1 for s in students.values() if s['round2'])}")
    print(f"Total repositories: {len(repos)}")
    print(f"Total evaluation results: {len(results)}")

def main():
    """Main evaluation orchestrator"""
    parser = argparse.ArgumentParser(description="LLM Code Deployment Evaluation System")
    parser.add_argument("--round1", action="store_true", help="Run Round 1 task distribution")
    parser.add_argument("--round2", action="store_true", help="Run Round 2 task distribution")
    parser.add_argument("--evaluate", action="store_true", help="Run repository evaluation")
    parser.add_argument("--full", action="store_true", help="Run complete evaluation cycle")
    parser.add_argument("--summary", action="store_true", help="Show evaluation summary")
    parser.add_argument("--wait", type=int, default=10, help="Minutes to wait between rounds (default: 10)")
    parser.add_argument("--eval-url", default="http://localhost:8001/notify", help="Evaluation server URL")
    
    args = parser.parse_args()
    
    # Initialize database
    init_database()
    
    print("🎯 LLM Code Deployment Evaluation System")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if args.full:
        # Complete evaluation cycle
        print("\n🚀 Starting complete evaluation cycle...")
        
        # Round 1
        print("\n" + "="*40)
        print("ROUND 1: Initial Task Distribution")
        print("="*40)
        send_round1_tasks(args.eval_url)
        
        # Wait for submissions
        print(f"\n⏳ Waiting {args.wait} minutes for Round 1 submissions...")
        wait_for_submissions(args.wait)
        
        # Evaluate Round 1
        print("\n" + "="*40)
        print("EVALUATION: Round 1 Results")
        print("="*40)
        run_evaluation()
        
        # Round 2
        print("\n" + "="*40)
        print("ROUND 2: Follow-up Task Distribution")
        print("="*40)
        send_round2_tasks(args.eval_url)
        
        # Wait for Round 2 submissions
        print(f"\n⏳ Waiting {args.wait} minutes for Round 2 submissions...")
        wait_for_submissions(args.wait)
        
        # Evaluate Round 2
        print("\n" + "="*40)
        print("EVALUATION: Round 2 Results")
        print("="*40)
        run_evaluation()
        
        # Final summary
        print_evaluation_summary()
        
    else:
        # Individual operations
        if args.round1:
            print("\n🚀 Running Round 1 task distribution...")
            send_round1_tasks(args.eval_url)
        
        if args.round2:
            print("\n🔄 Running Round 2 task distribution...")
            send_round2_tasks(args.eval_url)
        
        if args.evaluate:
            print("\n🔍 Running repository evaluation...")
            run_evaluation()
        
        if args.summary:
            print_evaluation_summary()
        
        if not any([args.round1, args.round2, args.evaluate, args.summary]):
            print("\nNo action specified. Use --help for options.")
            print("\nQuick start:")
            print("  --full          Run complete evaluation cycle")
            print("  --round1        Send Round 1 tasks")
            print("  --evaluate      Evaluate submitted repositories")
            print("  --summary       Show evaluation summary")

if __name__ == "__main__":
    main()
