#!/bin/bash
# ==============================================================================
# Odoo Farm OSS Auto-Publisher (Safe Cherry-pick Style)
# ------------------------------------------------------------------------------
# Strategy: Path-based incremental sync from dev to 19.0
# No force push. No history rewriting. No docs/ leaked.
# ==============================================================================

set -e

OSS_REMOTE="github"
RELEASE_BRANCH="19.0"
SOURCE_BRANCH="dev"

echo "🍒 Starting incremental sync to $RELEASE_BRANCH..."

# 1. 确保当前在 dev 分支且工作区干净
if [ "$(git rev-parse --abbrev-ref HEAD)" != "$SOURCE_BRANCH" ]; then
    echo "❌ Error: Please switch to '$SOURCE_BRANCH' first."
    exit 1
fi

if ! git diff-index --quiet HEAD --; then
    echo "❌ Error: Working tree not clean. Commit your changes in '$SOURCE_BRANCH' first."
    exit 1
fi

# 2. 切换到 19.0 分支
echo "📦 Switching to $RELEASE_BRANCH..."
git checkout $RELEASE_BRANCH

# 3. 从 dev 分支抓取所有非文档类的源代码和资源
# 我们列出所有需要同步的根目录和文件（排除 docs, .learnings 等）
echo "🚚 Pulling latest source code changes from $SOURCE_BRANCH..."

# 自动获取所有以 farm_, agri_, precision_ 开头的模块，以及核心配置文件
SYNC_TARGETS=$(ls -d farm_* agri_* precision_* config mosquitto Dockerfile docker-compose.yml LICENSE README.md CLA.md CONTRIBUTORS.txt DEVELOPER_GUIDE.md 2>/dev/null)

for target in $SYNC_TARGETS; do
    git checkout $SOURCE_BRANCH -- "$target"
done

# 4. 检查是否有变化需要提交
if git diff --cached --quiet; then
    echo "ℹ️ No new changes detected between $SOURCE_BRANCH and $RELEASE_BRANCH."
else
    echo "💾 Committing new changes..."
    # 自动生成包含当前 dev 分支最后一次提交信息的说明
    DEV_LAST_MSG=$(git log $SOURCE_BRANCH -1 --pretty=%B)
    git commit -m "sync: incremental update from $SOURCE_BRANCH" -m "Source Commit: $DEV_LAST_MSG"
    
    # 5. 推送到公开发布库 (正常 Push，非 Force)
    echo "📤 Pushing to $OSS_REMOTE..."
    git push $OSS_REMOTE $RELEASE_BRANCH
fi

# 6. 切回 dev 分支
echo "🧹 Returning to $SOURCE_BRANCH..."
git checkout $SOURCE_BRANCH

echo "=============================================================================="
echo "✅ SYNC COMPLETE! $RELEASE_BRANCH is now up-to-date with $SOURCE_BRANCH."
echo "=============================================================================="
