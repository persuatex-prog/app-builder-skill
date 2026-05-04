# 🚀 App Builder Skill - Complete Package

**Fully Automatic Full-Stack App Development System**

---

## 📦 What's Included

```
app-builder.skill (12 KB)
├── SKILL.md                    # Skill definition & triggers
└── scripts/
    ├── build_crew.py           # AI agent orchestration (Gensee LLM)
    ├── github_push.py          # GitHub deployment via Composio
    └── kaggle_train.py         # ML notebook generator (optional)
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Agents** | 3-agent team: Architect, Developer, QA Engineer |
| 💰 **100% Free** | No API keys, no payments, no credits |
| 🌐 **Full-Stack** | Frontend, Backend, Database, APIs |
| 📦 **Auto-Deploy** | GitHub repo creation & file upload |
| 🧪 **Auto-Testing** | QA agent writes tests automatically |
| 🎯 **Smart Code** | Production-ready, well-structured code |
| 🤖 **ML Support** | Kaggle integration for ML apps |

---

## 🚀 Quick Start

### Step 1: Install the Skill

```bash
# Copy the .skill file to your skills directory
cp app-builder.skill ~/.openclaw/workspace/skills/

# Unzip it
cd ~/.openclaw/workspace/skills/
unzip app-builder.skill

# Or manually extract to:
# ~/.openclaw/workspace/skills/app-builder/
```

### Step 2: Verify Installation

```bash
ls -la ~/.openclaw/workspace/skills/app-builder/
# Should show:
# - SKILL.md
# - scripts/build_crew.py
# - scripts/github_push.py
# - scripts/kaggle_train.py
```

### Step 3: Start Building Apps!

Just say:
```
"build app [your app idea]"
```

Examples:
- `"build app a todo list with React and Node.js"`
- `"build app Instagram clone with Django"`
- `"build app weather dashboard with API"`
- `"build app personal portfolio website"`
- `"build app chat application with WebSocket"`

---

## 🔧 How It Works

```
┌─────────────────────────────────────────────────────────┐
│  User: "build app [app description]"                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  1. PARSE REQUEST                                       │
│     - Extract app name (slug)                           │
│     - Extract features/description                      │
│     - Create apps/<app-slug>/ folder                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2. ARCHITECT AGENT (Gensee LLM)                        │
│     - Tech stack recommendation                         │
│     - Folder structure                                  │
│     - Database schema                                   │
│     - API endpoints                                     │
│     Output: ARCHITECT_PLAN.md                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  3. DEVELOPER AGENT (Gensee LLM)                        │
│     - Write ALL source code files                       │
│     - Frontend components                               │
│     - Backend routes                                    │
│     - Config files (package.json, requirements.txt)     │
│     - Dockerfile (if needed)                            │
│     Output: src/ folder with complete code              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  4. QA AGENT (Gensee LLM)                               │
│     - Code review                                       │
│     - Write unit tests                                  │
│     - Write integration tests                           │
│     - Suggest improvements                              │
│     Output: QA_REVIEW.md                                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  5. GITHUB DEPLOYMENT                                   │
│     - Create new repository (via browser)               │
│     - Upload all files via Composio API                 │
│     - Commit to main branch                             │
│     Output: GitHub repo URL                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  6. FINAL REPORT                                        │
│     - App name                                          │
│     - GitHub URL                                        │
│     - Tech stack summary                                │
│     - Setup instructions                                │
│     - Next steps                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technical Details

### LLM: Gensee/Qwen3.5-397B
- **Provider:** OpenClaw built-in
- **Cost:** FREE
- **API Key:** Auto-detected (GENSEE_INTERNAL_KEY)
- **Context:** 262K tokens
- **Speed:** Fast inference

### GitHub Integration
- **Method:** Composio API
- **Auth:** Already connected (persuatex-prog)
- **Repo:** Public by default (free tier)
- **Upload:** File-by-file via Contents API

### Agent Framework
- **Library:** CrewAI
- **Agents:** 3 (Architect, Developer, QA)
- **Process:** Sequential
- **Verbose:** Yes (detailed logs)

---

## 📁 Project Structure (Generated)

```
apps/<app-slug>/
├── ARCHITECT_PLAN.md      # Technical design document
├── README.md              # Auto-generated setup guide
├── QA_REVIEW.md           # Code review & tests
├── src/                   # Source code
│   ├── frontend/          # React/Vue/HTML files
│   ├── backend/           # Python/Node.js server
│   └── ...                # All generated files
├── package.json           # Node dependencies (if applicable)
├── requirements.txt       # Python dependencies (if applicable)
└── Dockerfile            # Container config (if applicable)
```

---

## 🎯 Example Apps Built

| App | Tech Stack | Status |
|-----|------------|--------|
| test-flask-app | Flask, REST API | ✅ Built & Deployed |
| (your next app!) | Your choice | 🚀 Ready |

---

## ⚠️ Limitations

1. **GitHub Repo Creation:** Requires browser automation (manual step if API fails)
2. **Large Apps:** May hit token limits for very complex projects
3. **ML Training:** Kaggle notebook generated, but manual upload may be needed
4. **Rate Limits:** Gensee API has implicit rate limits

---

## 🐛 Troubleshooting

### "GENSEE_INTERNAL_KEY not found"
```bash
# Check if running in OpenClaw environment
echo $GENSEE_INTERNAL_KEY
# Should return a long encrypted string
```

### "GitHub upload failed"
```bash
# Verify Composio connection
python3 -c "import json; print(json.load(open('~/.composio/config.json')))"
# Should show api_key and user_id
```

### "Files not generated"
```bash
# Check build output
cat apps/<app-slug>/ARCHITECT_PLAN.md
# Should contain technical plan
```

---

## 📞 Support

- **Skill Location:** `skills/app-builder/`
- **Memory Log:** `memory/2026-05-04-app-builder-skill.md`
- **Test App:** https://github.com/persuatex-prog/test-flask-app

---

## 🎉 Ready to Build!

Just say: **"build app [your idea]"**

And watch the magic happen! ✨

---

**Created:** 2026-05-04  
**Version:** 1.0.0  
**Author:** AI App Builder Skill  
**License:** FREE for personal & commercial use
