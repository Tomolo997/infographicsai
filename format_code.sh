#!/bin/bash

# Format Python code with black, isort, and autoflake
# Usage: ./format_code.sh [file_or_directory]

TARGET="${1:-app}"

echo "🧹 Removing unused imports with autoflake..."
env/bin/autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive "$TARGET"

echo "📦 Sorting imports with isort..."
env/bin/isort "$TARGET"

echo "🎨 Formatting code with black..."
env/bin/black "$TARGET"

echo "✅ Done! Your code is formatted."

