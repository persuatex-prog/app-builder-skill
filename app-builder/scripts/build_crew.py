#!/usr/bin/env python3
"""
CrewAI App Builder - Orchestrates AI agents to build full-stack apps
Uses Gensee API (OpenClaw's built-in LLM) - FREE, no API key needed
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

# Gensee API configuration (OpenClaw's built-in free LLM)
GENSEE_BASE_URL = "http://forwarder.staging.svc.cluster.local:9105/forward/gensee-397b/v1"
GENSEE_API_KEY = os.environ.get("GENSEE_INTERNAL_KEY", "")

# GitHub username (required)
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "")
if not GITHUB_USERNAME:
    # Try to detect from composio or default
    GITHUB_USERNAME = "persuatex-prog"  # Default from connected Composio account
    print(f"⚠️  GITHUB_USERNAME not set, using default: {GITHUB_USERNAME}")

# Parse arguments
if len(sys.argv) < 3:
    print("Usage: python3 build_crew.py <app-slug> '<app-description>'")
    sys.exit(1)

app_slug = sys.argv[1]
app_description = sys.argv[2]

# Create output directory
output_dir = Path(f"apps/{app_slug}")
output_dir.mkdir(parents=True, exist_ok=True)
src_dir = output_dir / "src"
src_dir.mkdir(exist_ok=True)

print(f"🚀 Building app: {app_slug}")
print(f"📝 Description: {app_description}")
print(f"📁 Output: {output_dir}")
print(f"🤖 LLM: Gensee (Free, built-in)")
print("-" * 50)

def call_llm(prompt, system_prompt="You are a helpful AI assistant."):
    """Call Gensee LLM API"""
    url = f"{GENSEE_BASE_URL}/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GENSEE_API_KEY}"
    }
    
    body = {
        "model": "Gensee/Qwen3.5-397B",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error calling LLM: {str(e)}"

def extract_code_blocks(text):
    """Extract code blocks from LLM response"""
    import re
    blocks = re.findall(r'```(\w+)?\n(.*?)```', text, re.DOTALL)
    return blocks

def save_file_from_block(lang, code, base_path):
    """Save a code block to file, trying to determine the path"""
    # Try to find file path in the code or comments
    lines = code.strip().split('\n')
    file_path = None
    
    # Look for path hints
    for line in lines[:5]:
        if line.startswith('# Path:') or line.startswith('// Path:'):
            file_path = line.split(':', 1)[1].strip()
            break
        if line.startswith('# File:') or line.startswith('// File:'):
            file_path = line.split(':', 1)[1].strip()
            break
    
    if not file_path:
        # Generate path based on language
        extensions = {
            'python': '.py', 'javascript': '.js', 'jsx': '.jsx', 
            'typescript': '.ts', 'tsx': '.tsx', 'html': '.html',
            'css': '.css', 'json': '.json', 'yaml': '.yaml',
            'yml': '.yml', 'markdown': '.md', 'md': '.md',
            'shell': '.sh', 'bash': '.sh', 'dockerfile': 'Dockerfile',
            'txt': '.txt', '': '.txt'
        }
        ext = extensions.get(lang.lower() if lang else '', '.txt')
        file_path = f"src/generated{ext}"
    
    # Make path relative to base
    if not file_path.startswith('/'):
        full_path = base_path / file_path
    else:
        full_path = Path(file_path)
    
    # Create parent directories
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    with open(full_path, 'w') as f:
        f.write(code)
    
    return full_path

# Define agent personas
ARCHITECT_SYSTEM = """You are a System Architect with 15+ years of experience.
Your job is to create detailed technical plans for web applications.

For each app request, provide:
1. Tech stack recommendation (frontend, backend, database)
2. Complete folder structure
3. Database schema (if needed)
4. API endpoints with examples
5. Environment variables needed
6. Dependencies list

Be specific and practical. Prefer simple, working solutions over complex ones."""

DEVELOPER_SYSTEM = """You are a Full-Stack Developer expert in modern web technologies.
Your job is to write complete, working code based on the architect's plan.

For each file:
1. Start with a comment showing the file path: # Path: src/file.js
2. Write complete, production-ready code
3. Include error handling
4. Add helpful comments

Generate ALL files needed for the app to run."""

QA_SYSTEM = """You are a QA Engineer focused on testing and quality.
Your job is to:
1. Review the generated code for issues
2. Write unit tests for critical functions
3. Provide testing instructions
4. Suggest improvements

Be thorough but practical."""

print("\n📋 Step 1: Architect Planning...\n")

architect_prompt = f"""Create a technical plan for this application:

{app_description}

Provide:
1. Tech stack (keep it simple and free)
2. Folder structure
3. Key files to create
4. Dependencies (package.json or requirements.txt)
5. Setup instructions

Format your response in markdown."""

architect_plan = call_llm(architect_prompt, ARCHITECT_SYSTEM)
print(architect_plan[:500] + "..." if len(architect_plan) > 500 else architect_plan)

# Save architect plan
plan_file = output_dir / "ARCHITECT_PLAN.md"
with open(plan_file, 'w') as f:
    f.write(architect_plan)
print(f"\n✅ Plan saved to: {plan_file}")

print("\n📝 Step 2: Developer Coding...\n")

developer_prompt = f"""Based on this plan, write ALL the source code files:

{architect_plan}

For EACH file:
1. Start with: # Path: relative/path/to/file.ext
2. Then write the complete file contents
3. Separate each file with a clear header

Generate the complete application code."""

developer_code = call_llm(developer_prompt, DEVELOPER_SYSTEM)

# Extract and save code blocks
code_blocks = extract_code_blocks(developer_code)
saved_files = []

for lang, code in code_blocks:
    try:
        saved_path = save_file_from_block(lang, code, output_dir)
        saved_files.append(str(saved_path))
        print(f"  → Saved: {saved_path}")
    except Exception as e:
        print(f"  ⚠️  Could not save block: {e}")

# If no blocks found, save the whole response
if not saved_files:
    code_file = src_dir / "generated_code.md"
    with open(code_file, 'w') as f:
        f.write(developer_code)
    saved_files.append(str(code_file))
    print(f"  → Saved raw output to: {code_file}")

print(f"\n✅ Generated {len(saved_files)} files")

print("\n🧪 Step 3: QA Review...\n")

qa_prompt = f"""Review this generated code and provide:
1. Any critical issues found
2. Test files that should be added
3. Setup and run instructions

Code generated:
{developer_code[:3000]}"""  # Truncate for context

qa_review = call_llm(qa_prompt, QA_SYSTEM)
print(qa_review[:500] + "..." if len(qa_review) > 500 else qa_review)

# Save QA review
qa_file = output_dir / "QA_REVIEW.md"
with open(qa_file, 'w') as f:
    f.write(qa_review)

print(f"\n✅ QA review saved to: {qa_file}")

# Create README
readme_content = f"""# {app_slug.replace('-', ' ').title()}

AI-generated application built with App Builder Skill.

## Description
{app_description}

## Quick Start

1. Install dependencies (check package.json or requirements.txt)
2. Set up environment variables (see .env.example)
3. Run the app (see setup instructions below)

## Generated Files
{chr(10).join(['- ' + f for f in saved_files[:10]])}

## Notes
- Generated by AI App Builder
- Review code before deploying to production
- Check QA_REVIEW.md for testing recommendations
"""

readme_file = output_dir / "README.md"
with open(readme_file, 'w') as f:
    f.write(readme_content)

print(f"\n✅ README created: {readme_file}")

# Summary
print("\n" + "=" * 50)
print(f"✅ App {app_slug} built successfully!")
print(f"\n📁 Output directory: {output_dir.absolute()}")
print(f"📄 Files generated: {len(saved_files)}")
print(f"📋 Next: Run github_push.py to deploy")
print("=" * 50)
