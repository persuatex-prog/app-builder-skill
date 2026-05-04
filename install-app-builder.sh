#!/bin/bash
# App Builder Skill - Installation Script
# Run this to install the app-builder skill

set -e

SKILL_FILE="/mnt/data/openclaw/workspace/.openclaw/workspace/skills/app-builder.skill"
INSTALL_DIR="/mnt/data/openclaw/workspace/.openclaw/workspace/skills/app-builder"

echo "🚀 App Builder Skill - Installation"
echo "===================================="
echo ""

# Check if skill file exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "❌ Error: app-builder.skill not found at $SKILL_FILE"
    exit 1
fi

echo "✅ Found: $SKILL_FILE"
echo ""

# Create installation directory
echo "📁 Creating installation directory..."
mkdir -p "$INSTALL_DIR"

# Extract skill
echo "📦 Extracting skill..."
cd /mnt/data/openclaw/workspace/.openclaw/workspace/skills/
python3 -c "
import zipfile
with zipfile.ZipFile('$SKILL_FILE', 'r') as z:
    z.extractall('.')
print('✅ Extracted successfully')
"

# Verify installation
echo ""
echo "🔍 Verifying installation..."
if [ -f "$INSTALL_DIR/SKILL.md" ]; then
    echo "✅ SKILL.md found"
else
    echo "❌ SKILL.md missing!"
    exit 1
fi

if [ -f "$INSTALL_DIR/scripts/build_crew.py" ]; then
    echo "✅ build_crew.py found"
else
    echo "❌ build_crew.py missing!"
    exit 1
fi

if [ -f "$INSTALL_DIR/scripts/github_push.py" ]; then
    echo "✅ github_push.py found"
else
    echo "❌ github_push.py missing!"
    exit 1
fi

if [ -f "$INSTALL_DIR/scripts/kaggle_train.py" ]; then
    echo "✅ kaggle_train.py found"
else
    echo "❌ kaggle_train.py missing!"
    exit 1
fi

echo ""
echo "===================================="
echo "✅ Installation Complete!"
echo "===================================="
echo ""
echo "📍 Installed to: $INSTALL_DIR"
echo ""
echo "🎯 Usage:"
echo '   Just say: "build app [your app idea]"'
echo ""
echo "📚 Examples:"
echo '   - "build app todo list with React"'
echo '   - "build app Instagram clone"'
echo '   - "build app weather dashboard"'
echo ""
echo "🎉 Ready to build apps!"
echo ""
