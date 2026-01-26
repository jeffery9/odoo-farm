# Release Scripts Policy

## Overview
This document explains the policy for release scripts and how to properly maintain separation between development tools and product releases.

## Release Scripts Policy

### Where Release Scripts Are Stored
- **Development branch (`dev`)**: ✅ Release scripts are stored here
- **Release branch (`19.0`)**: ❌ Release scripts are NOT present here

### Purpose
- Release scripts are development tools used for managing the release process
- They are NOT part of the core product code
- They should not be included in product releases to keep the release branch clean

### Process
1. Release scripts are created and maintained in the `dev` branch
2. When preparing releases, scripts and other non-code files are filtered out
3. The `19.0` branch contains only core product code
4. Release scripts ensure that only code commits (not documentation/tools) are transferred

### Verification
To verify that release scripts are properly excluded from releases, ensure:
- Release scripts exist in `dev` branch
- Release scripts AND their history are absent from `19.0` branch
- The `19.0` branch contains only core product files

### Workflow
1. Development happens in `dev` branch (including release script improvements)
2. When releasing, use the automated release script to cherry-pick only code commits
3. The release branch (`19.0`) remains clean of development tools
4. Documentation and tools stay in development branch only

### Commit Tracking
The enhanced release script maintains tracking of which commits were processed and which remain unprocessed, providing visibility during the cherry-pick process.