# MCP GitHub Repository Analyzer - Setup Guide

This guide will walk you through setting up and using the MCP GitHub Repository Analyzer project.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Step 1: Set Up Virtual Environment

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

## Step 2: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

## Step 3: Set Up API Keys

### GitHub API Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "MCP Repository Analyzer")
4. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `read:org` (Read organization data)
5. Click "Generate token"
6. Copy the token (you won't see it again!)

### Trello API Keys

1. Go to [Trello App Key](https://trello.com/app-key)
2. Copy your API Key
3. Click on "Token" to generate a token
4. Copy the generated token
5. Create a new Trello board or use an existing one
6. Get the board ID from the URL: `https://trello.com/b/BOARD_ID/board-name`

## Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# GitHub API Token
GITHUB_TOKEN=your_github_token_here

# Trello API Keys
TRELLO_API_KEY=your_trello_api_key
TRELLO_TOKEN=your_trello_token
TRELLO_BOARD_ID=your_trello_board_id

# Optional: Default repository to analyze
DEFAULT_REPO=owner/repository_name
```

Replace the placeholder values with your actual API keys.

## Step 5: Test the Setup

Run the test script to verify everything is configured correctly:

```bash
python test_mcp_server.py
```

This will check if all environment variables are set and provide helpful information about what's missing.

## Step 6: Run the MCP Server

Start the MCP server:

```bash
python mcp_server.py
```

The server will start and wait for connections via stdio.

## Step 7: Use the MCP Server

### Option A: Use with an MCP Client

Connect to the server using an MCP-compatible client. The server exposes these tools:

1. **analyze_repository** - Analyze a GitHub repository and create Trello tasks
2. **list_repositories** - List repositories for a GitHub user/organization
3. **get_repository_info** - Get detailed information about a repository
4. **create_trello_card** - Create a single Trello card

### Option B: Use the Example Client

Run the example client to see how the server works:

```bash
python example_client.py
```

This will:
- Start the MCP server
- List available tools
- Get information about the Microsoft VSCode repository
- List Microsoft's repositories
- Stop the server

## Example Workflows

### 1. Analyze a Repository and Create Trello Tasks

```python
# Call the analyze_repository tool
result = await client.call_tool("analyze_repository", {
    "repository_url": "microsoft/vscode",
    "create_trello_tasks": True,
    "max_files_to_analyze": 50
})
```

This will:
- Fetch repository information
- Analyze code quality
- Identify potential issues
- Create Trello cards for each issue
- Create a summary card

### 2. List User Repositories

```python
# Call the list_repositories tool
result = await client.call_tool("list_repositories", {
    "username": "microsoft"
})
```

### 3. Get Repository Information

```python
# Call the get_repository_info tool
result = await client.call_tool("get_repository_info", {
    "repository_url": "facebook/react"
})
```

### 4. Create a Custom Trello Card

```python
# Call the create_trello_card tool
result = await client.call_tool("create_trello_card", {
    "title": "Review security vulnerabilities",
    "description": "Check for potential security issues in the codebase",
    "list_name": "High Priority",
    "labels": ["security", "review"]
})
```

## Understanding the Analysis

The system analyzes repositories for:

### Code Quality Issues
- Missing README files
- Missing license files
- Missing dependency management files
- Missing test directories
- TODO/FIXME comments
- Debug statements in production code

### Security Issues
- Hardcoded passwords or API keys
- Use of dangerous functions (eval, exec)
- System command execution

### Performance Issues
- Nested loops
- Infinite loops
- Wildcard imports

### Repository Structure
- Presence of essential files (README, LICENSE, requirements.txt)
- Test directory structure
- CI/CD configuration

## Trello Integration

When Trello integration is enabled, the system will:

1. **Create Analysis Cards**: One card for each identified issue
2. **Create Issue Cards**: Cards for existing GitHub issues
3. **Create Summary Card**: Overview of the analysis results
4. **Organize by Lists**: Cards are placed in appropriate lists based on severity
5. **Add Labels**: Cards are tagged with relevant labels for easy filtering

## Troubleshooting

### Common Issues

1. **"GitHub token not configured"**
   - Make sure you've set the `GITHUB_TOKEN` environment variable
   - Verify the token has the correct permissions

2. **"Trello credentials not configured"**
   - Check that all Trello environment variables are set
   - Verify the board ID is correct

3. **"Could not access repository"**
   - Ensure the repository URL is correct
   - Check if the repository is private and your token has access

4. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (requires 3.8+)

### Getting Help

- Check the console output for detailed error messages
- Verify your API keys are working by testing them separately
- Ensure your Trello board exists and is accessible

## Advanced Configuration

### Customizing Analysis

You can modify the analysis by editing:
- `code_analyzer.py` - Add new patterns and rules
- `github_analyzer.py` - Customize repository analysis
- `trello_manager.py` - Modify Trello card creation logic

### Environment Variables

Additional environment variables you can set:
- `DEFAULT_REPO` - Default repository to analyze
- `MAX_FILES_TO_ANALYZE` - Maximum number of files to analyze (default: 50)

## Next Steps

Once you have the basic setup working:

1. **Explore different repositories** to see how the analysis varies
2. **Customize the analysis rules** to match your team's standards
3. **Integrate with your workflow** by connecting to your existing Trello boards
4. **Extend the functionality** by adding new analysis patterns or integrations

## Contributing

Feel free to extend this project by:
- Adding new analysis patterns
- Supporting additional file types
- Integrating with other project management tools
- Improving the code quality detection

Happy analyzing! 🚀 