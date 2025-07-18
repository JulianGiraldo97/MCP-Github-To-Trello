"""
Test script for the MCP GitHub Repository Analyzer

This script demonstrates how to use the MCP server with a simple example.
"""

import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_mcp_server():
    """Test the MCP server with a simple example."""
    
    print("🚀 MCP GitHub Repository Analyzer Test")
    print("=" * 50)
    
    # Check if environment variables are set
    github_token = os.getenv("GITHUB_TOKEN")
    trello_api_key = os.getenv("TRELLO_API_KEY")
    trello_token = os.getenv("TRELLO_TOKEN")
    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    
    print(f"GitHub Token: {'✅ Set' if github_token else '❌ Not set'}")
    print(f"Trello API Key: {'✅ Set' if trello_api_key else '❌ Not set'}")
    print(f"Trello Token: {'✅ Set' if trello_token else '❌ Not set'}")
    print(f"Trello Board ID: {'✅ Set' if trello_board_id else '❌ Not set'}")
    print()
    
    if not github_token:
        print("⚠️  GitHub token not set. Some features will not work.")
        print("   To set it up:")
        print("   1. Go to https://github.com/settings/tokens")
        print("   2. Generate a new token with 'repo' permissions")
        print("   3. Add it to your .env file as GITHUB_TOKEN=your_token")
        print()
    
    if not all([trello_api_key, trello_token, trello_board_id]):
        print("⚠️  Trello credentials not set. Trello integration will not work.")
        print("   To set it up:")
        print("   1. Go to https://trello.com/app-key")
        print("   2. Get your API key and token")
        print("   3. Create a board and get its ID from the URL")
        print("   4. Add them to your .env file")
        print()
    
    print("📋 Available Tools:")
    print("1. analyze_repository - Analyze a GitHub repository and create Trello tasks")
    print("2. list_repositories - List repositories for a GitHub user/organization")
    print("3. get_repository_info - Get detailed information about a repository")
    print("4. create_trello_card - Create a single Trello card")
    print()
    
    # Example usage
    print("💡 Example Usage:")
    print()
    print("1. Analyze a repository:")
    print("   python mcp_server.py")
    print("   Then call: analyze_repository with repository_url='owner/repo'")
    print()
    print("2. List repositories for a user:")
    print("   Call: list_repositories with username='github_username'")
    print()
    print("3. Get repository info:")
    print("   Call: get_repository_info with repository_url='owner/repo'")
    print()
    print("4. Create a Trello card:")
    print("   Call: create_trello_card with title='Task title'")
    print()
    
    # Test repository suggestions
    print("🎯 Suggested Test Repositories:")
    print("- microsoft/vscode (large, well-documented)")
    print("- facebook/react (popular, good for testing)")
    print("- django/django (Python project)")
    print("- nodejs/node (JavaScript project)")
    print()
    
    print("🔧 To run the MCP server:")
    print("   python mcp_server.py")
    print()
    print("🔗 To connect with an MCP client:")
    print("   Use an MCP-compatible client and connect to this server")
    print("   The server will be available via stdio")
    print()
    
    print("✨ Happy testing!")


if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 