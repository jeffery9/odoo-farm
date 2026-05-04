#!/bin/bash

# Enhanced Automated Release Script for Odoo Farm Dev
# This script automates the release process from dev to 19.0 branch following the SOP
# It cherry-picks non-documentation commits while excluding documentation files
# AND maintains tracking of which commits have been processed

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Function to validate current state
validate_state() {
    print_status "Validating current state..."

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi

    # Check if dev branch exists
    if ! git rev-parse --verify dev > /dev/null 2>&1; then
        print_error "dev branch does not exist"
        exit 1
    fi

    # Check if 19.0 branch exists
    if ! git rev-parse --verify 19.0 > /dev/null 2>&1; then
        print_error "19.0 branch does not exist"
        exit 1
    fi

    # Check if current branch is dev
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "dev" ]; then
        print_warning "You are not on the dev branch. Current branch: $current_branch"
        read -p "Do you want to continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    print_status "Validation completed successfully"
}

# Function to get documentation commits (those that only touch .md files or docs/ directory)
get_doc_commits() {
    local base_branch=${1:-"19.0"}
    local commits_file="doc_commits.tmp"

    print_status "Identifying documentation commits..."

    # Get commits that only touch documentation files (md files or docs/ directory)
    git log --format="%H" "$base_branch..dev" | while read -r commit; do
        # Check what files were changed in this commit
        files_changed=$(git show --name-only --format="" "$commit" 2>/dev/null | grep -E '\.md$|docs/|^docs/' || true)
        files_total=$(git show --name-only --format="" "$commit" 2>/dev/null | wc -l || echo "0")

        # If all changed files are documentation files, this is a doc commit
        if [ -n "$files_changed" ] && [ "$(echo "$files_changed" | wc -l)" -eq "$files_total" ] && [ "$files_total" -gt 0 ]; then
            echo "$commit"
        fi
    done > "$commits_file"

    echo "$commits_file"
}

# Function to get non-documentation commits
get_code_commits() {
    local base_branch=${1:-"19.0"}
    local doc_commits_file=$2
    local commits_file="code_commits.tmp"

    print_status "Identifying code commits..."

    # Get all commits from base branch to dev
    git log --format="%H" "$base_branch..dev" > all_commits.tmp

    # Remove documentation commits to get only code commits
    if [ -f "$doc_commits_file" ]; then
        comm -23 <(sort all_commits.tmp) <(sort "$doc_commits_file") > "$commits_file"
    else
        cp all_commits.tmp "$commits_file"
    fi

    rm -f all_commits.tmp
    echo "$commits_file"
}

# Function to create a mapping file to track original commit IDs
create_cherry_pick_mapping() {
    local code_commits_file=$1
    local mapping_file="cherry_pick_mapping.txt"

    print_status "Creating commit mapping for tracking..."

    > "$mapping_file"  # Clear the file

    # Create mapping of original commit to its commit message
    while read -r commit; do
        if [ -n "$commit" ]; then
            commit_message=$(git show -s --format="%s" "$commit" 2>/dev/null || echo "Unknown commit")
            echo "$commit|$commit_message" >> "$mapping_file"
        fi
    done < "$code_commits_file"

    echo "$mapping_file"
}

# Function to validate commit integrity after cherry-pick
validate_commit_integrity() {
    local commit_hash=$1

    print_status "Validating commit integrity for: $commit_hash"

    # Check if the commit has any issues with file types
    files_changed=$(git show --name-only --format="" "$commit_hash" 2>/dev/null || true)

    # Check if any .md files or docs/ directory were accidentally included
    doc_files=$(echo "$files_changed" | grep -E '\.md$|docs/|^docs/' || true)

    if [ -n "$doc_files" ]; then
        print_warning "Documentation files found in code commit $commit_hash:"
        echo "$doc_files"
        read -p "Do you want to proceed with this commit? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Reverting this commit from current branch..."
            git reset --hard HEAD~1
            return 1
        fi
    fi

    return 0
}

# Function to cherry-pick commits individually and handle conflicts
cherry_pick_commits() {
    local commits_file=$1
    local conflict_handling=${2:-"dev"}  # Default to using dev version on conflict
    local mapping_file=$3  # File to track the mapping

    print_status "Starting cherry-pick process..."

    # Create a tracking file to record what we're doing
    tracking_file="cherry_pick_tracking.log"
    echo "# Cherry-pick tracking log" > "$tracking_file"
    echo "# Original commit -> New commit mapping" >> "$tracking_file"
    echo "# Date: $(date)" >> "$tracking_file"
    echo "" >> "$tracking_file"

    # Read commits from the file in reverse order (oldest first)
    # We use git log directly here to ensure order is maintained
    tac "$commits_file" | while read -r original_commit; do
        if [ -n "$original_commit" ]; then
            print_status "Processing commit: $original_commit"

            # Get commit message for reference
            commit_message=$(git show -s --format="%s" "$original_commit" 2>/dev/null || echo "Unknown commit")
            print_status "Commit message: $commit_message"

            # Record the attempt in tracking log
            echo "# Attempting cherry-pick of $original_commit - $(date)" >> "$tracking_file"

            # Store HEAD before cherry-pick to detect if commit was added
            original_head=$(git rev-parse HEAD)

            # Perform cherry-pick
            if ! git cherry-pick "$original_commit" 2>/dev/null; then
                print_warning "Conflict occurred in commit: $original_commit"
                print_warning "Files in conflict:"
                git status --porcelain | grep "^UU\|^AA\|^DD" || echo "No specific conflict markers found"

                if [ "$conflict_handling" = "dev" ]; then
                    print_status "Using dev branch version for conflict resolution..."
                    # Get list of conflicting files
                    conflicting_files=$(git status --porcelain | grep "^U" | cut -c4- || true)

                    # For each conflicting file, use the dev version (ours)
                    for file in $conflicting_files; do
                        if [ -f "$file" ]; then
                            git checkout --ours "$file"
                            git add "$file"
                        fi
                    done

                    # For binary files with conflicts, explicitly check them out
                    git checkout --ours .

                    # Complete the cherry-pick
                    if ! git commit --no-edit 2>/dev/null; then
                        print_error "Failed to complete cherry-pick for commit: $original_commit"
                        echo "FAILED: $original_commit - $commit_message" >> "$tracking_file"
                        continue
                    fi
                else
                    print_error "Manual conflict resolution required for commit: $original_commit"
                    echo "FAILED: $original_commit - $commit_message" >> "$tracking_file"
                    continue
                fi
            fi

            # Get new commit hash (HEAD after cherry-pick)
            new_head=$(git rev-parse HEAD)

            # Validate the commit integrity
            validate_commit_integrity "$new_head" || {
                print_warning "Skipping commit due to validation failure: $original_commit"
                echo "SKIPPED: $original_commit - $commit_message" >> "$tracking_file"
                continue
            }

            # Record successful cherry-pick
            echo "$original_commit -> $new_head: $commit_message" >> "$tracking_file"
            print_status "Successfully processed and mapped: $original_commit -> $new_head"
            print_status "Commit message: $commit_message"
        fi
    done
}

# Function to clean documentation files from 19.0 branch
clean_documentation() {
    print_status "Cleaning documentation files from current branch..."

    # Find and remove all .md files (but not the scripts directory)
    find . -name "*.md" -type f -not -path "./scripts/*" -not -name "cherry_pick_tracking.log" -not -name "*tracking*" -delete 2>/dev/null || true

    # Remove docs/ directory if it exists
    if [ -d "docs/" ]; then
        rm -rf docs/
    fi

    # Find any remaining documentation-related files
    doc_files=$(find . -name "*.md" -type f 2>/dev/null | grep -v "./scripts/" || true)
    if [ -n "$doc_files" ]; then
        echo "$doc_files" | xargs rm -f 2>/dev/null || true
    fi

    # Stage any changes
    git add . 2>/dev/null || true

    # Check if there are changes to commit
    if ! git diff --cached --quiet 2>/dev/null; then
        print_status "Documentation files cleaned, committing changes..."
        git commit -m "chore: remove documentation files from release branch

Remove all documentation files (.md) as per release SOP.
Documentation should be maintained separately from code releases." 2>/dev/null || {
            print_warning "No documentation files to clean"
        }
    else
        print_status "No documentation files found to clean"
    fi
}

# Function to show tracking report of what was cherry-picked
generate_tracking_report() {
    local tracking_file="cherry_pick_tracking.log"
    local original_branch=${1:-"dev"}
    local target_branch=${2:-"19.0"}

    print_status "Generating tracking report..."

    if [ -f "$tracking_file" ]; then
        print_status "Cherry-pick tracking results:"
        echo "=================================="
        cat "$tracking_file"
        echo "=================================="
    fi

    # Generate a report showing which commits are still not in the target branch
    print_status "Calculating unprocessed commits..."

    # Get all commits in dev branch since target branch
    all_dev_commits=$(git log --format="%H" "$target_branch..$original_branch")

    # Get documentation commits that were intentionally not processed
    doc_commits_file=$(get_doc_commits "$target_branch")

    # Get commits that were actually cherry-picked (from tracking file)
    cherry_picked_origins=""
    if [ -f "$tracking_file" ]; then
        cherry_picked_origins=$(grep " -> " "$tracking_file" | cut -d' ' -f1 || true)
    fi

    # Find commits that were NOT cherry-picked (excluding documentation commits)
    all_dev_array=($all_dev_commits)
    doc_array=($(cat "$doc_commits_file" 2>/dev/null || true))
    cherry_picked_array=($cherry_picked_origins)

    # Create a temporary file to store all commits for comparison
    echo "$all_dev_commits" > temp_all_commits.tmp
    if [ -f "$doc_commits_file" ]; then
        cat "$doc_commits_file" >> temp_all_commits.tmp
    fi
    if [ -n "$cherry_picked_origins" ]; then
        echo "$cherry_picked_origins" >> temp_all_commits.tmp
    fi

    # Find commits that are not documentation and not cherry-picked
    # First get all non-doc commits
    if [ -f "$doc_commits_file" ]; then
        non_doc_commits=$(comm -23 <(sort temp_all_commits.tmp) <(sort "$doc_commits_file"))
    else
        non_doc_commits=$(sort temp_all_commits.tmp)
    fi

    # Then remove the ones that were cherry-picked
    if [ -n "$cherry_picked_origins" ]; then
        unprocessed_commits=$(comm -23 <(echo "$non_doc_commits" | sort) <(sort <<< "$cherry_picked_origins"))
    else
        unprocessed_commits="$non_doc_commits"
    fi

    # Clean up
    rm -f temp_all_commits.tmp

    print_status "Unprocessed commits (not cherry-picked to target branch):"
    if [ -n "$unprocessed_commits" ]; then
        while read -r commit; do
            if [ -n "$commit" ]; then
                commit_msg=$(git show -s --format="%s" "$commit" 2>/dev/null || echo "Unknown commit")
                echo "  $commit - $commit_msg"
            fi
        done <<< "$unprocessed_commits"
    else
        print_status "No unprocessed commits - all non-documentation commits have been cherry-picked!"
    fi

    # Show documentation commits that were intentionally skipped
    if [ -f "$doc_commits_file" ]; then
        print_status "Documentation commits intentionally skipped:"
        while read -r commit; do
            if [ -n "$commit" ]; then
                commit_msg=$(git show -s --format="%s" "$commit" 2>/dev/null || echo "Unknown commit")
                echo "  $commit - $commit_msg"
            fi
        done < "$doc_commits_file"
    fi

    # Clean up temporary file
    if [ -f "$doc_commits_file" ]; then
        rm -f "$doc_commits_file"
    fi
}

# Function to run basic checks
run_checks() {
    print_status "Running basic checks..."

    # Check current branch
    current_branch=$(git branch --show-current)
    print_status "Current branch: $current_branch"

    # List modified files to make sure we don't have unwanted documentation
    print_status "Current changes in working directory:"
    git status --short

    # Show last few commits to verify cherry-pick worked
    print_status "Recent commit history:"
    git log --oneline -10
}

# Main execution
main() {
    print_status "Starting enhanced automated release process from dev to 19.0 branch"
    print_status "This script will:"
    print_status "1. Identify code vs documentation commits"
    print_status "2. Cherry-pick only code commits to 19.0 branch"
    print_status "3. Track original commit IDs for reference"
    print_status "4. Remove any documentation files that may have been included"
    print_status "5. Generate a tracking report of what was processed"
    print_status "6. Validate the release branch state"

    # Ask for confirmation before proceeding
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Aborting release process"
        exit 0
    fi

    validate_state

    # Store original branch to return to
    original_branch=$(git branch --show-current)

    print_status "Switching to 19.0 branch to start release process..."
    git checkout 19.0 || {
        print_error "Failed to switch to 19.0 branch"
        exit 1
    }

    # Refresh 19.0 branch from remote if needed
    print_status "Updating 19.0 branch from remote..."
    git pull origin 19.0 --ff-only 2>/dev/null || {
        print_warning "Could not fast-forward 19.0, continuing"
    }

    # Get documentation commits
    doc_commits_file=$(get_doc_commits "19.0")
    print_status "Documentation commits identified in: $doc_commits_file"
    if [ -f "$doc_commits_file" ]; then
        doc_count=$(wc -l < "$doc_commits_file" 2>/dev/null || echo "0")
        print_status "Number of documentation commits to skip: $doc_count"
    fi

    # Get code commits
    code_commits_file=$(get_code_commits "19.0" "$doc_commits_file")
    print_status "Code commits identified in: $code_commits_file"
    code_count=$(wc -l < "$code_commits_file" 2>/dev/null || echo "0")
    print_status "Number of code commits to process: $code_count"

    echo "Code commits:"
    if [ "$code_count" -gt 0 ]; then
        cat "$code_commits_file"
    else
        print_status "No code commits found to process"
    fi

    # Check if we have any code commits to process
    if [ ! -s "$code_commits_file" ] || [ "$code_count" -eq 0 ]; then
        print_warning "No code commits found to cherry-pick"
        print_status "Release branch is already up to date or all commits were documentation"
        git checkout "$original_branch"
        [ -f "$doc_commits_file" ] && rm -f "$doc_commits_file"
        [ -f "$code_commits_file" ] && rm -f "$code_commits_file"
        exit 0
    fi

    # Create commit mapping for tracking
    mapping_file=$(create_cherry_pick_mapping "$code_commits_file")
    print_status "Commit mapping file created: $mapping_file"

    # Cherry-pick the code commits
    cherry_pick_commits "$code_commits_file" "dev" "$mapping_file"

    # Clean documentation files that might have been introduced
    clean_documentation

    print_status "Cherry-picking completed successfully!"
    print_status "Generating tracking report..."

    # Generate tracking report
    generate_tracking_report "dev" "19.0"

    # Ask if user wants to push to remote
    read -p "Do you want to push the updated 19.0 branch to remote? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Pushing 19.0 branch to remote..."
        git push origin 19.0
        if [ $? -eq 0 ]; then
            print_status "Successfully pushed 19.0 branch to remote"
        else
            print_error "Failed to push 19.0 branch to remote"
            exit 1
        fi
    fi

    # Return to original branch
    git checkout "$original_branch"

    # Clean up temporary files
    rm -f "$doc_commits_file" "$code_commits_file" "$mapping_file"

    print_status "Enhanced automated release process completed successfully!"
    print_status "The 19.0 branch now contains all non-documentation commits from dev branch"
    print_status "Tracking report shows which commits were processed and which remain"
}

# Run the main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi