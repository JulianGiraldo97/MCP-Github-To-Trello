# MCP GitHub Repository Analyzer

This project demonstrates the Model Context Protocol (MCP) by creating a server that can analyze GitHub repositories, identify potential issues, and create tasks in Trello.

## Use Case

The system performs the following workflow:
1. Connects to a GitHub repository
2. Analyzes the codebase for potential issues (missing documentation, security vulnerabilities, code quality issues)
3. Creates Trello cards for identified issues with appropriate labels and descriptions

## Features

- **GitHub Integration**: Fetches repository information, code files, and issues
- **AI-Powered Code Analysis**: Uses OpenAI GPT-4 and Anthropic Claude for intelligent code review
- **Advanced Security Analysis**: Detects vulnerabilities, security issues, and best practices
- **Code Quality Assessment**: Evaluates maintainability, performance, and architecture
- **Trello Integration**: Creates organized tasks with proper categorization
- **MCP Server**: Exposes functionality through the Model Context Protocol

## Setup

### 1. Set Up Virtual Environment (Recommended)

It's highly recommended to use a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Or use the provided script:
./activate_venv.sh
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file with your API keys:

```bash
# GitHub API Token
GITHUB_TOKEN=your_github_token_here

# Trello API Keys
TRELLO_API_KEY=your_trello_api_key
TRELLO_TOKEN=your_trello_token
TRELLO_BOARD_ID=your_trello_board_id

# AI API Keys (Optional - for enhanced analysis)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Get API Keys

**GitHub Token:**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `repo` permissions

**Trello API:**
1. Go to https://trello.com/app-key
2. Get your API key and token
3. Create a board and note its ID from the URL

**AI APIs (Optional - for enhanced analysis):**
1. **OpenAI**: Get API key from https://platform.openai.com/api-keys
2. **Anthropic**: Get API key from https://console.anthropic.com/

### 4. Run the MCP Server

```bash
# Using the main script
python main.py server

# Or using make
make run-server
```

## Usage

### Quick Start

```bash
# Run the full workflow on your repository
python main.py workflow

# Or use make
make run-workflow

# Run a quick test
python main.py test

# Set up Trello board
python main.py setup-trello
```

### Available Commands

- `python main.py server` - Start the MCP server
- `python main.py workflow [repo]` - Run full workflow analysis
- `python main.py test` - Run quick test
- `python main.py setup-trello` - Set up Trello board
- `python main.py ai-test` - Test AI analysis functionality

### MCP Server Tools

The MCP server provides the following tools:

- `analyze_repository`: Analyzes a GitHub repository and creates Trello tasks
- `list_repositories`: Lists repositories for a GitHub user/organization
- `get_repository_info`: Gets detailed information about a specific repository
- `create_trello_card`: Create a single Trello card

## Project Structure

```
mcp_tests/
├── src/                   # Source code
│   ├── analyzers/         # Analysis modules
│   │   ├── github_analyzer.py
│   │   └── ai_analyzer.py
│   ├── managers/          # External service managers
│   │   └── trello_manager.py
│   ├── utils/             # Utility functions
│   └── mcp_server.py      # Main MCP server
├── tests/                 # Test files
│   ├── quick_test.py
│   ├── direct_test.py
│   └── test_my_repo.py
├── examples/              # Example scripts
│   ├── run_full_mcp_workflow.py
│   ├── setup_trello_board.py
│   └── example_client.py
├── docs/                  # Documentation
├── main.py               # Main entry point
├── config.py             # Configuration settings
├── Makefile              # Build and development tasks
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## Example Workflow

1. Start the MCP server
2. Use an MCP client to connect to the server
3. Call `analyze_repository` with a GitHub repository URL
4. The system will:
   - Fetch repository data
   - Analyze code for issues
   - Create Trello cards for each identified issue
   - Return a summary of actions taken

## MCP Protocol

This server implements the MCP protocol, allowing AI assistants and other tools to interact with GitHub and Trello through a standardized interface. The server exposes tools that can be called by MCP clients to perform repository analysis and task management. 