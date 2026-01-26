# Automated Release System

## Overview
This system provides an automated way to release code from the `dev` branch to the `19.0` branch following the established SOP. The system ensures that only code commits are included in the release branch, while documentation files are excluded. The enhanced version also maintains tracking of commit processing to know which commits have been cherry-picked and which remain.

## Components

### 1. Enhanced Main Release Script (`scripts/enhanced_automated_release.sh`)
- Primary script that handles the entire release process
- Identifies documentation vs code commits
- Performs selective cherry-picking
- Handles conflict resolution
- Cleans documentation files from the target branch
- Maintains commit tracking and generates reports

### 2. Simple Wrapper (`release.sh`)
- Easy-to-use wrapper around the enhanced script
- Provides a simple entry point to the release system

### 3. Configuration File (`scripts/release_config.conf`)
- Configurable parameters for the release process
- Allows customization of branch names and behavior

### 4. Documentation (`scripts/README.md`)
- Complete documentation on how to use the release system
- Explains the purpose and workflow

## Features

- **Selective Cherry-picking**: Only code commits are transferred, documentation commits are filtered out
- **Commit Tracking**: Maintains mapping of original commits to cherry-picked commits
- **Conflict Resolution**: Automatic handling of conflicts using dev branch version as per SOP
- **Documentation Exclusion**: Automatic removal of .md files and docs/ directory from release branch
- **Processing Reports**: Generates reports showing which commits were processed and which remain
- **Validation**: Verification steps to ensure the release branch integrity
- **Safety**: Comprehensive checks and user confirmations before making changes
- **Reversibility**: Returns to original branch after completion

## Usage

To run the automated release:

```bash
./release.sh
```

Or for more control:

```bash
./scripts/enhanced_automated_release.sh
```

## SOP Compliance

This system strictly follows the release SOP by:
- Separating code and documentation commits
- Keeping documentation in the dev branch only
- Ensuring the 19.0 branch contains only code required for the release
- Using dev branch version in case of conflicts
- Providing traceability of which commits were processed

## Tracking Capabilities

The enhanced system addresses your concern about commit tracking by:
- Creating a mapping file that shows original commit IDs and their cherry-picked counterparts
- Generating a tracking log that records the processing of each commit
- Showing which commits remain unprocessed after the operation
- Listing documentation commits that were intentionally skipped