#!/bin/bash

# Script to cherry-pick non-documentation commits from dev to 19.0 branch
# Documentation commits are those that start with "docs:"

echo "Switching to 19.0 branch..."
git checkout 19.0

echo "Identifying non-documentation commits from dev..."
# Get the commits that are on dev but not on 19.0 branch
commits_to_process=$(git log 19.0..dev --oneline --no-merges | grep -v "^.* docs:" | grep -v "^.* cleanup" | grep -v "^.* refactor(ui)" | grep -v "^.* style:" | grep -v "^.* perf:" | grep -v "^.* chore:" | awk '{print $1}')

echo "Found commits to cherry-pick:"
git log 19.0..dev --oneline --no-merges | grep -v "^.* docs:" | grep -v "^.* cleanup" | grep -v "^.* refactor(ui)" | grep -v "^.* style:" | grep -v "^.* perf:" | grep -v "^.* chore:"

echo "Starting cherry-pick process..."
for commit in $commits_to_process; do
    echo "Cherry-picking commit: $commit"
    git cherry-pick "$commit"
    if [ $? -ne 0 ]; then
        echo "Conflict occurred at commit $commit, please resolve manually"
        echo "After resolving, run: git cherry-pick --continue"
        exit 1
    fi
done

echo "All non-documentation commits have been cherry-picked to 19.0 branch"
echo "Current status:"
git log --oneline -10