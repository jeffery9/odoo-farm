# Branch Sync Guide

## Overview
This guide explains how to properly synchronize non-documentation commits from the main development branch (typically `dev`) to the `19.0` release branch.

## Branch Identification
- **Main Development Branch**: Usually `dev` - contains the latest development work
- **Release Branch**: `19.0` - production-ready code for releases
- **Note**: The scripts are designed to work with `dev` as the primary source branch for synchronization

## Scripts

### sync_from_clean_dev.sh
Basic synchronization script that cherry-picks non-documentation commits from the main development branch (typically `dev` or `clean-dev`) to `19.0` branch in chronological order.

### sync_from_clean_dev_isolated.sh
**Recommended approach**: This script copies itself to a temporary directory and executes from there to avoid issues when switching branches during execution. The script automatically identifies and works with the main development branch.

## Usage

### Using the Isolated Script (Recommended)
```bash
./sync_from_clean_dev_isolated.sh
```

This approach prevents issues where branch switching operations might affect script execution.

### Using the Basic Script
```bash
./sync_from_clean_dev.sh
```

## Process

1. Resets `19.0` branch to the `release-point-f6d9b7c` tag
2. Identifies all commits in the main development branch (typically `dev`) after the tag
3. Filters out documentation commits (those matching certain patterns)
4. Cherry-picks remaining commits in chronological order (from early to late)
5. Adds the original commit hash to each new commit message as `Original-commit: <hash>`

## Documentation Commit Patterns (Skipped)
- `docs:*`
- `*.md` files
- `README` files
- Any commit with "Documentation" in the title
- Module plan updates
- Epic status updates
- Business governance documentation

## Best Practices

1. **CRITICAL**: Always run sync scripts from a temporary or isolated location OUTSIDE the repository to prevent branch switching from interrupting script execution. When scripts run from within the repository, branch switches can interrupt access to the script and documentation files.
2. Verify the `release-point-f6d9b7c` tag exists before running the script
3. Ensure the main development branch (typically `dev`) and `19.0` branches are up to date before synchronization
4. Review the synchronization results after completion
5. Use the isolated version (`sync_from_clean_dev_isolated.sh`) as it automatically handles the isolation requirement

## Troubleshooting

If a cherry-pick fails due to conflicts:
- The script will skip the conflicting commit
- Continue monitoring the process
- Manually resolve important conflicts if needed
