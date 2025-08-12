#!/bin/bash

# CODE_ALCHEMY_PRO - Code Quality Tools
# Linting and formatting script

set -e

echo "🔍 Running code quality checks..."

# Check if required tools are installed
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    fi
}

check_tool "black"
check_tool "flake8"
check_tool "mypy"

echo "📝 Formatting code with Black..."
black --check src/ tests/ examples/

echo "🔍 Running Flake8 linting..."
flake8 src/ tests/ examples/ --max-line-length=88 --extend-ignore=E203,W503

echo "🔍 Running MyPy type checking..."
mypy src/ --ignore-missing-imports

echo "✅ All code quality checks passed!"
