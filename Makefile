# MCP GitHub Repository Analyzer - Makefile

.PHONY: help install test run-server run-workflow setup-trello clean

# Default target
help:
	@echo "MCP GitHub Repository Analyzer - Available commands:"
	@echo ""
	@echo "  install        - Install dependencies"
	@echo "  test           - Run quick test"
	@echo "  run-server     - Start the MCP server"
	@echo "  run-workflow   - Run full workflow analysis"
	@echo "  setup-trello   - Set up Trello board"
	@echo "  clean          - Clean up temporary files"
	@echo "  help           - Show this help message"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Run quick test
test:
	@echo "🧪 Running quick test..."
	python main.py test

# Run MCP server
run-server:
	@echo "🚀 Starting MCP server..."
	python main.py server

# Run full workflow
run-workflow:
	@echo "🚀 Running full MCP workflow..."
	python main.py workflow

# Set up Trello board
setup-trello:
	@echo "🔧 Setting up Trello board..."
	python main.py setup-trello

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete

# Development helpers
dev-install:
	@echo "🔧 Setting up development environment..."
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

activate:
	@echo "🔧 Activating virtual environment..."
	@echo "Run: source venv/bin/activate"

# Project structure
structure:
	@echo "📁 Project structure:"
	@tree -I 'venv|__pycache__|*.pyc' -a

# Run all tests
test-all:
	@echo "🧪 Running all tests..."
	python tests/quick_test.py
	python tests/direct_test.py
	python tests/test_my_repo.py 