#!/bin/bash
# Simple wrapper to run the enhanced automated release script with default settings

echo "This script runs the enhanced automated release from dev to 19.0 branch."
echo "It follows the SOP to cherry-pick only code commits and exclude documentation."
echo "It also provides tracking of which commits have been processed."

# Check if we're in the right directory
if [ ! -f "scripts/enhanced_automated_release.sh" ]; then
    echo "Error: enhanced_automated_release.sh not found in scripts/ directory"
    exit 1
fi

# Run the main script
./scripts/enhanced_automated_release.sh "$@"