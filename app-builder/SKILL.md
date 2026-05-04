---
name: app-builder
description: Automates full-stack app creation using Antigravity, Gemini API, CrewAI, GitHub and Kaggle. Triggers when user mentions building an app, creating a software project, or asks to generate code for a specific application idea.
version: 1.0.0
user-invocable: true
metadata: {"openclaw": {"requires": {"env": ["GITHUB_USERNAME"], "bins": ["python3", "git", "curl"]}, "primaryEnv": "GITHUB_USERNAME", "uses_composio": true}}
---

# App Builder Skill

## Purpose

This Skill enables fully autonomous app development. The agent will receive an app description, set up a CrewAI team (Architect, Developer, QA), generate the entire codebase, and push it to GitHub. For ML tasks, it will offload training to Kaggle.

## Triggers

Activate this skill when the user says:
- "build a [app type]"
- "create an app for [description]"
- "I need an application that [features]"
- "generate a full-stack project for [idea]"
- `build app [description]`
- "make a [tech] application"
- "create website for [purpose]"

## Pre-requisites (Environment Setup)

Before first use, ensure the following:

### 1. Working Directory
Work inside the Antigravity IDE terminal or any directory with Python3 access.

### 2. Python Environment
Install required dependencies:

```bash
pip install crewai gitpython PyGithub
```

### 3. Environment Variables
Set via `export`:

```bash
export GEMINI_API_KEY="your-key-here"      # Free from Google AI Studio
export GITHUB_TOKEN="your-token-here"       # Personal access token with repo scope
export GITHUB_USERNAME="your-username"      # Your GitHub username
```

**Optional for ML apps:**
```bash
export KAGGLE_USERNAME="your-kaggle-username"
export KAGGLE_KEY="your-kaggle-key"
```

If any are missing, the agent should pause and ask the user to provide them before proceeding.

## App Building Workflow

Follow this sequence for every app request.

### Step 1: Parse User Request

1. Extract the app name (convert to slug: lowercase, hyphens, no special chars)
2. Extract detailed description of features
3. If description is too vague, ask clarifying questions:
   - What's the main purpose?
   - Who are the users?
   - Any specific features must-have?
   - Preferred tech stack?
4. Create project folder: `apps/<app-slug>/`

### Step 2: Assemble the AI Team (CrewAI)

Execute the build script:

```bash
python3 skills/app-builder/scripts/build_crew.py "<app-slug>" "<full-description>"
```

This creates three CrewAI agents:
- **Architect**: Plans tech stack, folder structure, database schema, API endpoints
- **Developer**: Writes all source code (frontend, backend, configs, Dockerfile)
- **QA Engineer**: Writes tests, runs them, fixes failures autonomously

All agents use Gemini API (`gemini/gemini-pro` or `gemini/gemini-1.5-pro`).

Output goes to `apps/<app-slug>/src/` with full project scaffold.

### Step 3: GitHub Repository Creation and Push

Execute the GitHub push script:

```bash
python3 skills/app-builder/scripts/github_push.py "<app-slug>"
```

This will:
1. Create a new private repository named `<app-slug>` on GitHub
2. Initialize local git repo in the app folder
3. Commit all files with message "Initial commit by AI App Builder"
4. Push to GitHub main branch
5. Output the repository URL

### Step 4: Optional Kaggle Integration (ML Apps Only)

If the Architect's plan mentions ML/model training:

1. Check if `KAGGLE_USERNAME` and `KAGGLE_KEY` are set
2. If yes, execute:
   ```bash
   python3 skills/app-builder/scripts/kaggle_train.py "<app-slug>"
   ```
3. This generates a ready-to-run Kaggle notebook and pushes it
4. If no Kaggle credentials, save notebook to `apps/<app-slug>/kaggle_notebook.ipynb` and inform user to upload manually

### Step 5: Final Report

Provide a summary to the user:

```
✅ App Built Successfully!

📦 App Name: <app-name>
🔗 GitHub Repo: https://github.com/<username>/<app-slug>
📁 Local Path: /workspace/apps/<app-slug>/
🚀 Tech Stack: <list from architect plan>
📊 ML Training: <Kaggle link or "Not required">

Next steps:
- Clone the repo: git clone <repo-url>
- Install dependencies: cd <app-slug> && npm install / pip install -r requirements.txt
- Start the app: npm start / python app.py
```

## Error Handling

| Error | Action |
|-------|--------|
| GEMINI_API_KEY missing/invalid | Ask user to get free key from Google AI Studio |
| GITHUB_TOKEN invalid | Guide user to regenerate token with repo scope |
| CrewAI execution fails | Check internet, retry with verbose logging |
| GitHub rate limit | Wait 60 seconds and retry |
| Kaggle API fails | Save notebook locally, inform user |

## Testing

After creating this Skill, test immediately:

```bash
# Test with a simple Flask app
python3 skills/app-builder/scripts/build_crew.py "hello-flask" "A simple Flask REST API with one endpoint /hello that returns JSON message"
```

Verify:
- [ ] CrewAI executes without errors
- [ ] Code files are generated in apps/hello-flask/
- [ ] GitHub repo is created and pushed
- [ ] User receives clear summary with repo link

## File Structure

```
skills/app-builder/
├── SKILL.md                    # This file
└── scripts/
    ├── build_crew.py           # CrewAI agent orchestration
    ├── github_push.py          # GitHub repo creation & push
    └── kaggle_train.py         # Optional ML notebook generation
```

## Notes

- Always work autonomously - if one approach fails, try another
- Never ask the user for help unless absolutely stuck (missing credentials, etc.)
- Log all steps verbosely for debugging
- Keep the user informed with progress updates
- Default to private repos unless user specifies public
