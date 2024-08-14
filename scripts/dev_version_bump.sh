#!/bin/bash

# Increment patch version and set version with development release segment
VERSION=$(poetry version -s)
MAJOR=$(echo $VERSION | cut -d. -f1)
MINOR=$(echo $VERSION | cut -d. -f2)
PATCH=$(echo $VERSION | cut -d. -f3)
NEW_PATCH=$((PATCH + 1))
BUILD_NUMBER=${GITHUB_RUN_NUMBER}
NEW_VERSION="${MAJOR}.${MINOR}.${NEW_PATCH}.dev${BUILD_NUMBER}"
poetry version $NEW_VERSION

# Export the new version for use in subsequent steps
echo "NEW_VERSION=$NEW_VERSION" >> $GITHUB_ENV
