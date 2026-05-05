#!/bin/bash
# ==============================================================================
# Odoo Farm OSS Auto-Publisher
# ------------------------------------------------------------------------------
# Workflow: dev (local) -> temporary clean branch -> git-filter-repo -> github:odoo-farm:19.0
# ==============================================================================

set -e

# 1. Configuration
ORIG_REPO_DIR=$(pwd)
OSS_REMOTE="github"             # 公开发布库的 git remote 名
DEV_REMOTE="dev-remote"         # 内研全量库的 git remote 名
RELEASE_BRANCH="19.0"           # 目标分支名
TEMP_SYNC_BRANCH="tmp-oss-sync"

echo "🚀 Starting OSS Release Process..."

# 2. Safety Checks
if [ "$(git rev-parse --abbrev-ref HEAD)" != "dev" ]; then
    echo "❌ Error: You must be on 'dev' branch to publish."
    exit 1
fi

if ! git diff-index --quiet HEAD --; then
    echo "❌ Error: You have uncommitted changes. Please commit or stash first."
    exit 1
fi

# 3. Create a temporary branch based on local dev
echo "📦 Creating temporary sync branch..."
git branch -D $TEMP_SYNC_BRANCH 2>/dev/null || true
git checkout -b $TEMP_SYNC_BRANCH

# 4. Critical: Wipe internal history and files
echo "🧼 Cleaning history (Removing docs/, .learnings/, etc.)..."
git filter-repo \
  --path docs/ \
  --path .learnings/ \
  --path .claude/ \
  --path AGENTS.md \
  --path matrix_summary.txt \
  --path final_healing_fix.py \
  --path heal_misalignment.py \
  --path test.png \
  --invert-paths --force

# 5. Push to Open Source Repository
echo "📤 Pushing cleaned history to Open Source Repository ($OSS_REMOTE)..."
git push $OSS_REMOTE HEAD:$RELEASE_BRANCH --force

# 6. Synchronize the clean 19.0 branch back to Internal Dev Repository
echo "🔄 Updating 19.0 branch in Internal Repository ($DEV_REMOTE)..."
git push $DEV_REMOTE HEAD:$RELEASE_BRANCH --force

# 7. Cleanup and Return
echo "🧹 Cleaning up local temporary branches..."
git checkout dev
git branch -D $TEMP_SYNC_BRANCH 2>/dev/null || true

echo "=============================================================================="
echo "✅ SUCCESS! Odoo Farm has been safely published to OSS."
echo "Public: https://github.com/jeffery9/odoo-farm"
echo "=============================================================================="
