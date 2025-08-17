# SMART WORKSPACE Professional - Development Makefile

.PHONY: help install install-dev test launch demo

help:
	@echo "SMART WORKSPACE Professional - Development Commands"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev   - Install development dependencies"
	@echo "  test          - Run tests"
	@echo "  launch        - Launch SMART WORKSPACE"
	@echo "  demo          - Run project management demo"

install:
	@echo "Installing production dependencies..."
	pip install -r requirements.txt

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt

test:
	@echo "Running tests..."
	pytest tests/ -v

launch:
	@echo "Launching SMART WORKSPACE Professional..."
	python launch_workspace.py

demo:
	@echo "Running project management demo..."
	python demo_project_management.py
