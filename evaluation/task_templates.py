#!/usr/bin/env python3
"""
Task templates for the LLM Code Deployment evaluation system
"""

import base64
import hashlib
import json
from datetime import datetime

# Task templates as defined in the project specification
TASK_TEMPLATES = {
    "sum-of-sales": {
        "id": "sum-of-sales",
        "brief": "Publish a single-page site that fetches data.csv from attachments, sums its sales column, sets the title to \"Sales Summary {seed}\", displays the total inside #total-sales, and loads Bootstrap 5 from jsdelivr.",
        "attachments": [
            {
                "name": "data.csv",
                "generator": "generate_sales_csv"
            }
        ],
        "checks": [
            "js: document.title === `Sales Summary {seed}`",
            "js: !!document.querySelector(\"link[href*='bootstrap']\")",
            "js: Math.abs(parseFloat(document.querySelector(\"#total-sales\").textContent) - {result}) < 0.01"
        ],
        "round2": [
            {
                "brief": "Add a Bootstrap table #product-sales that lists each product with its total sales and keeps #total-sales accurate after render.",
                "checks": [
                    "js: document.querySelectorAll(\"#product-sales tbody tr\").length >= 1",
                    "js: (() => { const rows = [...document.querySelectorAll(\"#product-sales tbody tr td:last-child\")]; const sum = rows.reduce((acc, cell) => acc + parseFloat(cell.textContent), 0); return Math.abs(sum - {result}) < 0.01; })()"
                ]
            },
            {
                "brief": "Introduce a currency select #currency-picker that converts the computed total using rates.json from attachments and mirrors the active currency inside #total-currency.",
                "attachments": [
                    {
                        "name": "rates.json",
                        "generator": "generate_currency_rates"
                    }
                ],
                "checks": [
                    "js: !!document.querySelector(\"#currency-picker option[value='USD']\")",
                    "js: !!document.querySelector(\"#total-currency\")"
                ]
            },
            {
                "brief": "Allow filtering by region via #region-filter, update #total-sales with the filtered sum, and set data-region on that element to the active choice.",
                "checks": [
                    "js: document.querySelector(\"#region-filter\").tagName === \"SELECT\"",
                    "js: document.querySelector(\"#total-sales\").dataset.region !== undefined"
                ]
            }
        ]
    },
    
    "markdown-to-html": {
        "id": "markdown-to-html",
        "brief": "Publish a static page that converts input.md from attachments to HTML with marked, renders it inside #markdown-output, and loads highlight.js for code blocks.",
        "attachments": [
            {
                "name": "input.md",
                "generator": "generate_markdown_content"
            }
        ],
        "checks": [
            "js: !!document.querySelector(\"script[src*='marked']\")",
            "js: !!document.querySelector(\"script[src*='highlight.js']\")",
            "js: document.querySelector(\"#markdown-output\").innerHTML.includes(\"<h\")"
        ],
        "round2": [
            {
                "brief": "Add tabs #markdown-tabs that switch between rendered HTML in #markdown-output and the original Markdown in #markdown-source while keeping content in sync.",
                "checks": [
                    "js: document.querySelectorAll(\"#markdown-tabs button\").length >= 2",
                    "js: document.querySelector(\"#markdown-source\").textContent.trim().length > 0"
                ]
            },
            {
                "brief": "Support loading Markdown from a ?url= parameter when present and fall back to the attachment otherwise, showing the active source in #markdown-source-label.",
                "checks": [
                    "js: document.querySelector(\"#markdown-source-label\").textContent.length > 0",
                    "js: !!document.querySelector(\"script\").textContent.includes(\"fetch(\")"
                ]
            },
            {
                "brief": "Display a live word count badge #markdown-word-count that updates after every render and formats numbers with Intl.NumberFormat.",
                "checks": [
                    "js: document.querySelector(\"#markdown-word-count\").textContent.includes(\",\")",
                    "js: !!document.querySelector(\"script\").textContent.includes(\"Intl.NumberFormat\")"
                ]
            }
        ]
    },
    
    "github-user-created": {
        "id": "github-user-created",
        "brief": "Publish a Bootstrap page with form id=\"github-user-{seed}\" that fetches a GitHub username, optionally uses ?token=, and displays the account creation date in YYYY-MM-DD UTC inside #github-created-at.",
        "attachments": [],
        "checks": [
            "js: document.querySelector(\"#github-user-{seed}\").tagName === \"FORM\"",
            "js: document.querySelector(\"#github-created-at\").textContent.includes(\"20\")",
            "js: !!document.querySelector(\"script\").textContent.includes(\"https://api.github.com/users/\")"
        ],
        "round2": [
            {
                "brief": "Show an aria-live alert #github-status that reports when a lookup starts, succeeds, or fails.",
                "checks": [
                    "js: document.querySelector(\"#github-status\").getAttribute(\"aria-live\") === \"polite\"",
                    "js: !!document.querySelector(\"script\").textContent.includes(\"github-status\")"
                ]
            },
            {
                "brief": "Display the account age in whole years inside #github-account-age alongside the creation date.",
                "checks": [
                    "js: parseInt(document.querySelector(\"#github-account-age\").textContent, 10) >= 0",
                    "js: document.querySelector(\"#github-account-age\").textContent.toLowerCase().includes(\"years\")"
                ]
            },
            {
                "brief": "Cache the last successful lookup in localStorage under \"github-user-{seed}\" and repopulate the form on load.",
                "checks": [
                    "js: !!document.querySelector(\"script\").textContent.includes(\"localStorage.setItem(\\\"github-user-{seed}\\\"\")",
                    "js: !!document.querySelector(\"script\").textContent.includes(\"localStorage.getItem(\\\"github-user-{seed}\\\"\")"
                ]
            }
        ]
    }
}

def generate_seed(email: str, timestamp: str = None) -> str:
    """Generate a deterministic seed from email and timestamp"""
    if not timestamp:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H")
    
    seed_input = f"{email}::{timestamp}"
    return hashlib.md5(seed_input.encode()).hexdigest()[:8]

def generate_sales_csv(seed: str) -> str:
    """Generate sample sales CSV data"""
    # Use seed to generate deterministic but varied data
    import random
    random.seed(seed)
    
    products = ["Widget A", "Widget B", "Widget C", "Widget D", "Gadget X", "Gadget Y"]
    regions = ["North", "South", "East", "West", "Central"]
    
    csv_lines = ["product,sales,region"]
    total = 0
    
    for i in range(random.randint(4, 8)):
        product = random.choice(products)
        sales = round(random.uniform(500, 3000), 2)
        region = random.choice(regions)
        csv_lines.append(f"{product},{sales},{region}")
        total += sales
    
    csv_content = "\n".join(csv_lines)
    return csv_content, total

def generate_currency_rates(seed: str) -> str:
    """Generate sample currency rates JSON"""
    import random
    random.seed(seed)
    
    rates = {
        "USD": 1.0,
        "EUR": round(random.uniform(0.8, 0.9), 4),
        "GBP": round(random.uniform(0.7, 0.8), 4),
        "JPY": round(random.uniform(110, 150), 2),
        "CAD": round(random.uniform(1.2, 1.4), 4)
    }
    
    return json.dumps(rates, indent=2)

def generate_markdown_content(seed: str) -> str:
    """Generate sample markdown content"""
    import random
    random.seed(seed)
    
    topics = ["Technology", "Science", "History", "Literature", "Mathematics"]
    topic = random.choice(topics)
    
    markdown = f"""# {topic} Overview

## Introduction

This is a sample markdown document about **{topic.lower()}**. It contains various formatting elements to test the markdown parser.

### Code Example

```python
def hello_world():
    print("Hello, World!")
    return True
```

### List Items

- First item with *italic* text
- Second item with **bold** text
- Third item with `inline code`

### Important Note

> This is a blockquote that contains important information about {topic.lower()}.

## Conclusion

The study of {topic.lower()} continues to evolve and provide new insights.
"""
    
    return markdown

def create_task_from_template(template_id: str, email: str, round_num: int = 1, evaluation_url: str = "http://localhost:8001/notify") -> dict:
    """Create a task request from a template"""
    if template_id not in TASK_TEMPLATES:
        raise ValueError(f"Unknown template: {template_id}")
    
    template = TASK_TEMPLATES[template_id]
    seed = generate_seed(email)
    
    # Generate task ID
    brief_hash = hashlib.md5(template["brief"].encode()).hexdigest()[:5]
    task_id = f"{template_id}-{brief_hash}"
    
    # Generate nonce
    import uuid
    nonce = str(uuid.uuid4())
    
    # Process brief and checks with seed (but don't format yet - wait for result)
    if round_num == 1:
        brief = template["brief"]
        checks = template["checks"]
        attachments_config = template.get("attachments", [])
    else:
        # Round 2 - pick a random round2 task
        import random
        random.seed(seed + str(round_num))
        round2_task = random.choice(template["round2"])
        brief = round2_task["brief"]
        checks = round2_task["checks"]
        attachments_config = round2_task.get("attachments", [])
    
    # Generate attachments
    attachments = []
    result = None
    
    for att_config in attachments_config:
        generator_name = att_config["generator"]
        
        if generator_name == "generate_sales_csv":
            content, total = generate_sales_csv(seed)
            result = total
        elif generator_name == "generate_currency_rates":
            content = generate_currency_rates(seed)
        elif generator_name == "generate_markdown_content":
            content = generate_markdown_content(seed)
        else:
            continue
        
        # Encode as data URI
        b64_content = base64.b64encode(content.encode()).decode()
        mime_type = "text/csv" if att_config["name"].endswith(".csv") else \
                   "application/json" if att_config["name"].endswith(".json") else \
                   "text/markdown"
        
        attachments.append({
            "name": att_config["name"],
            "url": f"data:{mime_type};base64,{b64_content}"
        })
    
    # Format brief and checks with all available variables
    format_vars = {"seed": seed, "result": result if result is not None else 0}
    
    try:
        brief = brief.format(**format_vars)
        checks = [check.format(**format_vars) for check in checks]
    except KeyError as e:
        # If formatting fails, use basic formatting
        print(f"Warning: Template formatting error for {e}, using basic formatting")
        brief = brief.replace("{seed}", seed).replace("{result}", str(format_vars["result"]))
        checks = [check.replace("{seed}", seed).replace("{result}", str(format_vars["result"])) for check in checks]
    
    return {
        "email": email,
        "secret": "TDS DEDLY",  # This should match the student's secret
        "task": task_id,
        "round": round_num,
        "nonce": nonce,
        "brief": brief,
        "checks": checks,
        "evaluation_url": evaluation_url,
        "attachments": attachments,
        "_metadata": {
            "template_id": template_id,
            "seed": seed,
            "result": result
        }
    }
