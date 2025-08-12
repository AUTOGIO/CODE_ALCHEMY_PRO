#!/bin/bash

# CODE_ALCHEMY_PRO - Testing Tools
# Test execution script

set -e

echo "🧪 Running CODE_ALCHEMY_PRO test suite..."

# Default values
TEST_TYPE="all"
COVERAGE=true
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit)
            TEST_TYPE="unit"
            shift
            ;;
        --integration)
            TEST_TYPE="integration"
            shift
            ;;
        --performance)
            TEST_TYPE="performance"
            shift
            ;;
        --no-coverage)
            COVERAGE=false
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --unit          Run only unit tests"
            echo "  --integration   Run only integration tests"
            echo "  --performance   Run only performance tests"
            echo "  --no-coverage   Disable coverage reporting"
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

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest is not installed. Please install it first."
    exit 1
fi

# Build pytest command
PYTEST_CMD="pytest"

if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=src --cov-report=term-missing --cov-report=html"
fi

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Run tests based on type
case $TEST_TYPE in
    "unit")
        echo "🔬 Running unit tests..."
        $PYTEST_CMD tests/unit/ -m "unit"
        ;;
    "integration")
        echo "🔗 Running integration tests..."
        $PYTEST_CMD tests/integration/ -m "integration"
        ;;
    "performance")
        echo "⚡ Running performance tests..."
        $PYTEST_CMD tests/performance/ -m "performance"
        ;;
    "all")
        echo "🚀 Running all tests..."
        $PYTEST_CMD tests/
        ;;
esac

echo "✅ Test suite completed successfully!"
