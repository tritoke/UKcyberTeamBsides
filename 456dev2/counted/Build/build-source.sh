#!/bin/bash

# This script expects to be run from <challenge-root>/Build/
cd "$(dirname "$0")" || exit 1

mkdir -p artifacts

rm -f artifacts/app.zip

# collect challenge source into app.zip for sharing.
pushd ../Source || exit 1
7zz a -stl ../Build/artifacts/app.zip app/main.py app/Dockerfile app/requirements.txt

echo "Created artifacts/app.zip with public challenge source."