#!/bin/bash

# CODE_ALCHEMY_PRO - Code Formatting Tools
# Code formatting script using Black and isort

set -e

echo "🎨 Formatting CODE_ALCHEMY_PRO codebase..."

# Check if required tools are installed
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    fi
}

check_tool "black"
check_tool "isort"

# Default values
CHECK_ONLY=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            CHECK_ONLY=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --check         Check formatting without making changes"
            echo "  -v, --verbose   Verbose output"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build command flags
BLACK_FLAGS=""
ISORT_FLAGS=""

if [ "$CHECK_ONLY" = true ]; then
    BLACK_FLAGS="--check"
    ISORT_FLAGS="--check-only"
fi

if [ "$VERBOSE" = true ]; then
    BLACK_FLAGS="$BLACK_FLAGS --verbose"
    ISORT_FLAGS="$ISORT_FLAGS --verbose"
fi

echo "📝 Running isort..."
isort $ISORT_FLAGS src/ tests/ examples/

echo "🎨 Running Black..."
black $BLACK_FLAGS src/ tests/ examples/

if [ "$CHECK_ONLY" = true ]; then
    echo "✅ Code formatting check completed - all files are properly formatted!"
else
    echo "✅ Code formatting completed successfully!"
fi
