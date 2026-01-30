#!/bin/bash
# Script to sync non-document commits from clean-dev branch to 19.0 branch
# Maintains chronological order and preserves original commit IDs

set -e

echo "Starting sync from clean-dev to 19.0 branch..."

# Ensure we're on the 19.0 branch
git checkout 19.0

# Reset 19.0 branch to the release tag point
echo "Resetting 19.0 branch to release tag..."
git reset --hard release-point-f6d9b7c

# Get clean-dev branch commits in chronological order (after tag)
echo "Getting commits from clean-dev branch..."
git log --format="%H" --no-merges release-point-f6d9b7c..clean-dev --reverse > /tmp/clean_dev_commits.txt

total_commits=$(wc -l < /tmp/clean_dev_commits.txt)
echo "Found $total_commits commits to process"

count=0
while IFS= read -r commit; do
    if [ -z "$commit" ]; then
        continue
    fi
    
    count=$((count + 1))
    echo "Processing commit ($count/$total_commits): $commit"
    
    # Get commit subject to check if it's documentation
    commit_subject=$(git -C . log --format="%s" -n 1 $commit)
    
    # Check if it's a documentation commit
    if echo "$commit_subject" | grep -E -q "(docs:|docs |\.md|README|Documentation|algorithm documentation files|update.*MODULE_PLAN|publish.*spec|update.*product strategy|establish.*mandate|add EPIC|update.*implementation status|update.*module plans|update.*governance hierarchy|update.*business governance)"; then
        echo "  Skipping documentation commit: $commit_subject"
        continue
    fi
    
    # Cherry-pick the commit
    if git cherry-pick $commit; then
        # Add original commit ID to the commit message
        original_msg=$(git log --format="%s" -n 1 HEAD)
        new_commit_msg="${original_msg}

Original-commit: $commit"
        git commit --amend -m "$new_commit_msg" --no-edit
        echo "  Successfully processed: $commit_subject"
    else
        echo "  Conflict occurred for: $commit_subject"
        echo "  Skipping this commit and continuing..."
        git cherry-pick --skip
    fi
done < /tmp/clean_dev_commits.txt

echo "Sync completed successfully!"
echo "Total commits processed: $count"
rm -f /tmp/clean_dev_commits.txt
