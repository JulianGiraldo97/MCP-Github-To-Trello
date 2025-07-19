"""
Configuration settings for the MCP GitHub Repository Analyzer.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
EXAMPLES_DIR = PROJECT_ROOT / "examples"
DOCS_DIR = PROJECT_ROOT / "docs"

# Environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

# AI API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Default settings
DEFAULT_REPO = "JulianGiraldo97/practica-docker-microservices"
MAX_FILES_TO_ANALYZE = 50
MAX_ISSUES_TO_FETCH = 10
MAX_COMMITS_TO_FETCH = 10

# Analysis settings
QUALITY_SCORES = {
    "missing_readme": -10,
    "missing_license": -5,
    "missing_dependencies": -15,
    "missing_tests": -10,
    "missing_ci_cd": -5
}

# Trello settings
TRELLO_LISTS = [
    "To Do",
    "Bugs", 
    "Enhancements",
    "High Priority",
    "Critical",
    "Suggestions",
    "Summary"
]

TRELLO_LABELS = [
    ("security", "red"),
    ("bug", "red"),
    ("enhancement", "blue"),
    ("documentation", "green"),
    ("testing", "yellow"),
    ("performance", "orange"),
    ("code-quality", "purple"),
    ("suggestion", "sky"),
    ("summary", "lime"),
    ("mcp", "black")
]

# File patterns to analyze
ANALYZABLE_EXTENSIONS = [
    '.py', '.js', '.jsx', '.ts', '.tsx', '.java', 
    '.cpp', '.c', '.h', '.cs', '.go', '.rs', '.php'
]

# Security patterns to check
SECURITY_PATTERNS = [
    r"password\s*=\s*['\"][^'\"]+['\"]",
    r"api_key\s*=\s*['\"][^'\"]+['\"]",
    r"secret\s*=\s*['\"][^'\"]+['\"]",
    r"eval\s*\(",
    r"exec\s*\(",
    r"os\.system\s*\(",
    r"subprocess\.call\s*\(",
]

# Code quality patterns
CODE_QUALITY_PATTERNS = [
    r"TODO:",
    r"FIXME:",
    r"XXX:",
    r"HACK:",
    r"print\s*\(",
    r"debugger;",
    r"console\.log\s*\(",
]

# Performance patterns
PERFORMANCE_PATTERNS = [
    r"for\s+.*\s+in\s+.*:\s*\n.*\s+for\s+.*\s+in\s+.*:",
    r"while\s+True:",
    r"import\s+\*",
] 