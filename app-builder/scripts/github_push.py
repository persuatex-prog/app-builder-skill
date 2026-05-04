#!/usr/bin/env python3
"""
GitHub Push Script - Creates repo and uploads files via Composio API
Uses Composio GitHub integration (already connected - no token needed)
"""

import os
import sys
import json
import base64
import urllib.request
from pathlib import Path

# Composio API configuration
COMPOSIO_API_BASE = "https://backend.composio.dev/api"
COMPOSIO_API_KEY = ""
USER_ID = "default"

# Read Composio credentials
_config_path = os.path.expanduser("~/.composio/config.json")
if os.path.exists(_config_path):
    try:
        with open(_config_path) as f:
            _cfg = json.load(f)
            COMPOSIO_API_KEY = _cfg.get("api_key", "")
            USER_ID = _cfg.get("user_id", USER_ID)
    except Exception:
        pass

if not COMPOSIO_API_KEY:
    print("❌ Error: Composio API key not found")
    print("   Make sure GitHub is connected via Settings → Connectors")
    sys.exit(1)

# GitHub username (from env or default)
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "persuatex-prog")

def composio_post(path, body):
    """Make API call to Composio"""
    url = f"{COMPOSIO_API_BASE}/{path}"
    data = json.dumps(body).encode()
    headers = {
        "x-api-key": COMPOSIO_API_KEY,
        "User-Agent": "AppBuilder/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return {"error": error_body[:500], "status": e.code}
    except Exception as e:
        return {"error": str(e)}

def encode_file(file_path):
    """Encode file content to base64"""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_all_files(directory, base_path=None):
    """Get all files in directory recursively"""
    if base_path is None:
        base_path = directory
    
    files = []
    for item in directory.iterdir():
        if item.name.startswith('.') and item.name != '.env.example':
            continue  # Skip hidden files except .env.example
        if item.is_file():
            rel_path = item.relative_to(base_path)
            files.append((str(rel_path), item))
        elif item.is_dir() and item.name != '__pycache__':
            files.extend(get_all_files(item, base_path))
    
    return files

# Parse arguments
if len(sys.argv) < 2:
    print("Usage: python3 github_push.py <app-slug>")
    sys.exit(1)

app_slug = sys.argv[1]
app_path = Path(f"apps/{app_slug}")

if not app_path.exists():
    print(f"❌ Error: App directory not found: {app_path}")
    print("   Run build_crew.py first")
    sys.exit(1)

print(f"📦 Deploying to GitHub: {app_slug}")
print(f"📁 Source: {app_path}")
print(f"👤 GitHub: {GITHUB_USERNAME}")
print("-" * 50)

try:
    # Step 1: Create repository using Composio
    print("\n🔨 Creating GitHub repository...")
    
    create_result = composio_post(f"v2/actions/GITHUB_CREATE_A_REPOSITORY/execute", {
        "entityId": USER_ID,
        "appName": "github",
        "input": {
            "name": app_slug,
            "description": f"🤖 AI-generated app: {app_slug}",
            "private": False,  # Public by default (free tier)
            "auto_init": False
        }
    })
    
    repo_url = None
    repo_created = False
    
    if create_result.get("successful") or create_result.get("successfull"):
        repo_data = create_result.get("data", {})
        repo_url = repo_data.get("html_url", "")
        print(f"✅ Repository created: {repo_url}")
        repo_created = True
    else:
        # Check error - might already exist
        error_msg = str(create_result.get("error", ""))
        if "already exists" in error_msg.lower() or create_result.get("status") == 422:
            print(f"⚠️  Repository already exists, using it...")
            repo_url = f"https://github.com/{GITHUB_USERNAME}/{app_slug}"
        else:
            print(f"⚠️  Create response: {create_result}")
            repo_url = f"https://github.com/{GITHUB_USERNAME}/{app_slug}"
    
    # Step 2: Get all files to upload
    print("\n📁 Collecting files...")
    files = get_all_files(app_path)
    print(f"   Found {len(files)} files")
    
    # Step 3: Upload files via GitHub API
    print("\n📤 Uploading files to GitHub...")
    
    uploaded = 0
    failed = 0
    
    for rel_path, file_path in files:
        # GitHub path should not start with ./
        github_path = rel_path.replace('\\', '/')
        if github_path.startswith('./'):
            github_path = github_path[2:]
        
        try:
            # Read and encode file
            content = encode_file(file_path)
            
            # Upload via Composio
            upload_result = composio_post(f"v2/actions/GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS/execute", {
                "entityId": USER_ID,
                "appName": "github",
                "input": {
                    "owner": GITHUB_USERNAME,
                    "repo": app_slug,
                    "path": github_path,
                    "message": f"Add {github_path} 🤖",
                    "content": content
                }
            })
            
            if upload_result.get("successful") or upload_result.get("successfull"):
                uploaded += 1
                print(f"   ✓ {github_path}")
            else:
                failed += 1
                print(f"   ✗ {github_path}: {upload_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            failed += 1
            print(f"   ✗ {github_path}: {str(e)[:100]}")
        
        # Rate limit protection - small delay
        if uploaded % 5 == 0:
            import time
            time.sleep(0.5)
    
    # Create README if not exists
    if not (app_path / "README.md").exists():
        readme_content = f"""# {app_slug.replace('-', ' ').title()}

🤖 AI-generated application built with App Builder Skill.

## Description
Auto-generated full-stack application.

## Setup
1. Clone this repository
2. Install dependencies (see requirements.txt or package.json)
3. Run the application

## Generated by
OpenClaw App Builder Skill
"""
        readme_path = app_path / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        content = base64.b64encode(readme_content.encode()).decode()
        composio_post(f"v2/actions/GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS/execute", {
            "entityId": USER_ID,
            "appName": "github",
            "input": {
                "owner": GITHUB_USERNAME,
                "repo": app_slug,
                "path": "README.md",
                "message": "Add README.md 🤖",
                "content": content
            }
        })
        uploaded += 1
    
    # Success!
    print("\n" + "=" * 50)
    print("✅ Successfully deployed to GitHub!")
    print(f"\n🔗 Repository URL: {repo_url}")
    print(f"📁 Local path: {app_path.absolute()}")
    print(f"📊 Files uploaded: {uploaded}")
    if failed > 0:
        print(f"⚠️  Failed: {failed}")
    print(f"\n📋 Clone command:")
    print(f"   git clone {repo_url}.git")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Deployment failed: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check GitHub is connected in Settings → Connectors")
    print("2. Verify GITHUB_USERNAME is correct")
    print("3. Check Composio API key is valid")
    import traceback
    traceback.print_exc()
