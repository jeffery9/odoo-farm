# Enhanced Automated Release Script

This script automates the release process from the `dev` branch to the `19.0` branch according to the release SOP. It cherry-picks only non-documentation commits while excluding documentation files, and maintains tracking of which commits have been processed.

## Purpose

The script ensures that:
1. Only code commits (not documentation) are transferred from `dev` to `19.0` branch
2. Documentation files (`.md` files and `docs/` directory) are excluded from the release branch
3. Conflicts are resolved by using the `dev` branch version (as per SOP requirement)
4. The release branch maintains clean separation between code and documentation
5. Commit tracking is maintained to know which commits have been processed and which remain

## Prerequisites

- The `dev` and `19.0` branches must exist
- You should be on the `dev` branch or willing to switch to it
- Ensure all changes are committed before running the script

## Usage

```bash
# Run the enhanced script (with tracking)
./scripts/enhanced_automated_release.sh

# Or use the simple wrapper
./release.sh

# The script will guide you through the process with confirmations
```

## What the script does

1. **Validation**: Checks that required branches exist and validates current state
2. **Commit Classification**: Identifies documentation commits (only touching `.md` files or `docs/` directory) vs code commits
3. **Cherry-picking**: Selectively cherry-picks only code commits to the 19.0 branch
4. **Commit Tracking**: Maintains mapping of original commits to new cherry-picked commits
5. **Conflict Resolution**: On conflicts, uses the `dev` branch version as per SOP
6. **Documentation Cleanup**: Removes any documentation files that might have been introduced
7. **Tracking Report**: Generates a report showing which commits were processed and which remain
8. **Verification**: Shows the final state and can optionally push to remote

## Tracking Features

The enhanced script provides:
- **Commit Mapping**: Records the relationship between original commits and cherry-picked commits
- **Processing Log**: Tracks which commits were successfully processed, failed, or skipped
- **Unprocessed Report**: Shows which commits remain unprocessed after the operation
- **Documentation Tracking**: Lists commits that were intentionally skipped as documentation

## Configuration

The script defaults to using the `dev` branch version in case of conflicts. Parameters can be configured in `release_config.conf`.

## Notes

- The script creates temporary files (`doc_commits.tmp`, `code_commits.tmp`, `cherry_pick_mapping.txt`, `cherry_pick_tracking.log`) which are automatically cleaned up
- After running, the script returns to the original branch you were on
- Documentation files are completely removed from the 19.0 branch as per SOP
- The tracking log (`cherry_pick_tracking.log`) shows the mapping of original commits to cherry-picked commits