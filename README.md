# MCP GitHub Repository Analyzer

This project demonstrates the Model Context Protocol (MCP) by creating a server that can analyze GitHub repositories, identify potential issues, and create tasks in Trello.

## Use Case

The system performs the following workflow:
1. Connects to a GitHub repository
2. Analyzes the codebase for potential issues (missing documentation, security vulnerabilities, code quality issues)
3. Creates Trello cards for identified issues with appropriate labels and descriptions

## Features

- **GitHub Integration**: Fetches repository information, code files, and issues
- **Code Analysis**: Identifies potential problems in the codebase
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
```

### 3. Get API Keys

**GitHub Token:**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `repo` permissions

**Trello API:**
1. Go to https://trello.com/app-key
2. Get your API key and token
3. Create a board and note its ID from the URL

### 4. Run the MCP Server

```bash
python mcp_server.py
```

## Usage

The MCP server provides the following tools:

- `analyze_repository`: Analyzes a GitHub repository and creates Trello tasks
- `list_repositories`: Lists repositories for a GitHub user/organization
- `get_repository_info`: Gets detailed information about a specific repository

## Project Structure

```
mcp_tests/
├── mcp_server.py          # Main MCP server implementation
├── github_analyzer.py     # GitHub repository analysis logic
├── trello_manager.py      # Trello task creation and management
├── code_analyzer.py       # Code quality and issue detection
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
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