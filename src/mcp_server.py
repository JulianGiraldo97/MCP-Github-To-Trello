"""
MCP GitHub Repository Analyzer Server

This server implements the Model Context Protocol (MCP) to provide tools for
analyzing GitHub repositories and creating Trello tasks.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from .analyzers.github_analyzer import GitHubAnalyzer
from .managers.trello_manager import TrelloManager
from .analyzers.ai_analyzer import AIAnalyzer

# Load environment variables
load_dotenv()

# Initialize components
github_token = os.getenv("GITHUB_TOKEN")
trello_api_key = os.getenv("TRELLO_API_KEY")
trello_token = os.getenv("TRELLO_TOKEN")
trello_board_id = os.getenv("TRELLO_BOARD_ID")

# Initialize analyzers and managers
github_analyzer = None
trello_manager = None
ai_analyzer = AIAnalyzer(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

if github_token:
    github_analyzer = GitHubAnalyzer(github_token)

if trello_api_key and trello_token and trello_board_id:
    trello_manager = TrelloManager(trello_api_key, trello_token, trello_board_id)

# Create MCP server
server = Server("github-trello-analyzer")


@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
    tools = [
        Tool(
            name="analyze_repository",
            description="Analyze a GitHub repository, identify issues, and create Trello tasks",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_url": {
                        "type": "string",
                        "description": "GitHub repository URL (e.g., https://github.com/owner/repo or owner/repo)"
                    },
                    "create_trello_tasks": {
                        "type": "boolean",
                        "description": "Whether to create Trello tasks for identified issues",
                        "default": True
                    },
                    "max_files_to_analyze": {
                        "type": "integer",
                        "description": "Maximum number of files to analyze",
                        "default": 50
                    }
                },
                "required": ["repository_url"]
            }
        ),
        Tool(
            name="list_repositories",
            description="List repositories for a GitHub user or organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "GitHub username or organization name"
                    }
                },
                "required": ["username"]
            }
        ),
        Tool(
            name="get_repository_info",
            description="Get detailed information about a specific GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository_url": {
                        "type": "string",
                        "description": "GitHub repository URL or owner/repo format"
                    }
                },
                "required": ["repository_url"]
            }
        ),
        Tool(
            name="create_trello_card",
            description="Create a single Trello card",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Card title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Card description"
                    },
                    "list_name": {
                        "type": "string",
                        "description": "List name to place the card in",
                        "default": "To Do"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Labels to add to the card"
                    }
                },
                "required": ["title"]
            }
        )
    ]
    
    return ListToolsResult(tools=tools)


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    
    if name == "analyze_repository":
        return await analyze_repository(arguments)
    elif name == "list_repositories":
        return await list_repositories(arguments)
    elif name == "get_repository_info":
        return await get_repository_info(arguments)
    elif name == "create_trello_card":
        return await create_trello_card(arguments)
    else:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )
            ]
        )


async def analyze_repository(arguments: Dict[str, Any]) -> CallToolResult:
    """Analyze a GitHub repository and optionally create Trello tasks."""
    if not github_analyzer:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="GitHub token not configured. Please set GITHUB_TOKEN environment variable."
                )
            ]
        )
    
    repo_url = arguments.get("repository_url")
    create_trello_tasks = arguments.get("create_trello_tasks", True)
    max_files = arguments.get("max_files_to_analyze", 50)
    
    if not repo_url:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Repository URL is required."
                )
            ]
        )
    
    try:
        # Get repository
        repo = github_analyzer.get_repository(repo_url)
        if not repo:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Could not access repository: {repo_url}"
                    )
                ]
            )
        
        # Get repository information
        repo_info = github_analyzer.get_repository_info(repo_url)
        
        # Analyze repository structure
        structure = github_analyzer.analyze_repository_structure(repo)
        
        # Analyze code quality
        code_quality = github_analyzer.analyze_code_quality(repo)
        
        # Perform AI-powered code analysis
        sample_files = []
        contents = repo.get_contents("")
        for content in contents[:max_files]:
            if hasattr(content, 'content'):
                sample_files.append({
                    'path': content.path,
                    'language': content.name.split('.')[-1] if '.' in content.name else 'unknown'
                })
        
        ai_analysis = ai_analyzer.analyze_repository_with_ai(repo, sample_files)
        
        # Get recent issues
        recent_issues = github_analyzer.get_recent_issues(repo, limit=10)
        
        # Combine all analysis results
        combined_analysis = {
            "issues": code_quality.get("issues", []) + ai_analysis.issues,
            "suggestions": code_quality.get("suggestions", []) + ai_analysis.suggestions,
            "score": (code_quality.get("score", 100) + ai_analysis.code_quality_score) // 2
        }
        
        # Create Trello tasks if requested
        trello_results = {}
        if create_trello_tasks and trello_manager:
            # Create cards for analysis issues
            analysis_cards = trello_manager.create_analysis_cards(combined_analysis, repo_info["full_name"])
            
            # Create cards for GitHub issues
            issue_cards = trello_manager.create_issue_cards(recent_issues, repo_info["full_name"])
            
            # Create summary card
            total_cards = len(analysis_cards) + len(issue_cards)
            summary_card = trello_manager.create_summary_card(repo_info, combined_analysis, total_cards)
            
            trello_results = {
                "analysis_cards_created": len(analysis_cards),
                "issue_cards_created": len(issue_cards),
                "summary_card_created": summary_card is not None,
                "total_cards_created": total_cards + (1 if summary_card else 0)
            }
        elif create_trello_tasks and not trello_manager:
            trello_results = {"error": "Trello credentials not configured"}
        
        # Generate summary
        summary = f"""
# Repository Analysis Results

## Repository Information
- **Name:** {repo_info.get('full_name', 'Unknown')}
- **Description:** {repo_info.get('description', 'No description')}
- **Language:** {repo_info.get('language', 'Unknown')}
- **Stars:** {repo_info.get('stars', 0)}
- **Forks:** {repo_info.get('forks', 0)}
- **Open Issues:** {repo_info.get('open_issues', 0)}

## Analysis Results
- **Quality Score:** {combined_analysis.get('score', 0)}/100
- **Issues Found:** {len(combined_analysis.get('issues', []))}
- **Suggestions:** {len(combined_analysis.get('suggestions', []))}
- **Files Analyzed:** {code_analysis.get('analyzed_files', 0)}/{code_analysis.get('total_files_found', 0)}

## Repository Structure
- **Has README:** {structure.get('has_readme', False)}
- **Has License:** {structure.get('has_license', False)}
- **Has Requirements:** {structure.get('has_requirements', False)}
- **Has Tests:** {structure.get('has_tests', False)}
- **Has CI/CD:** {structure.get('has_github_actions', False)}

## Trello Integration
"""
        
        if trello_results.get("error"):
            summary += f"- **Status:** {trello_results['error']}\n"
        else:
            summary += f"- **Analysis Cards Created:** {trello_results.get('analysis_cards_created', 0)}\n"
            summary += f"- **Issue Cards Created:** {trello_results.get('issue_cards_created', 0)}\n"
            summary += f"- **Summary Card Created:** {trello_results.get('summary_card_created', False)}\n"
            summary += f"- **Total Cards Created:** {trello_results.get('total_cards_created', 0)}\n"
        
        # Add detailed issues if any
        if combined_analysis.get("issues"):
            summary += "\n## Issues Found\n"
            for issue in combined_analysis["issues"][:10]:  # Show first 10 issues
                summary += f"- **{issue.get('severity', 'medium').upper()}:** {issue.get('title', 'Unknown issue')}\n"
        
        # Add suggestions if any
        if combined_analysis.get("suggestions"):
            summary += "\n## Suggestions\n"
            for suggestion in combined_analysis["suggestions"][:5]:  # Show first 5 suggestions
                summary += f"- {suggestion.get('title', 'Unknown suggestion')}\n"
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=summary
                )
            ]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error analyzing repository: {str(e)}"
                )
            ]
        )


async def list_repositories(arguments: Dict[str, Any]) -> CallToolResult:
    """List repositories for a GitHub user or organization."""
    if not github_analyzer:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="GitHub token not configured. Please set GITHUB_TOKEN environment variable."
                )
            ]
        )
    
    username = arguments.get("username")
    if not username:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Username is required."
                )
            ]
        )
    
    try:
        repos = github_analyzer.list_repositories(username)
        
        if not repos:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"No repositories found for user: {username}"
                    )
                ]
            )
        
        # Format the results
        result = f"# Repositories for {username}\n\n"
        for repo in repos[:20]:  # Show first 20 repositories
            result += f"## {repo.get('name', 'Unknown')}\n"
            result += f"- **Full Name:** {repo.get('full_name', 'Unknown')}\n"
            result += f"- **Description:** {repo.get('description', 'No description')}\n"
            result += f"- **Language:** {repo.get('language', 'Unknown')}\n"
            result += f"- **Stars:** {repo.get('stars', 0)}\n"
            result += f"- **Forks:** {repo.get('forks', 0)}\n"
            result += f"- **URL:** {repo.get('url', 'N/A')}\n"
            result += f"- **Private:** {repo.get('private', False)}\n"
            result += f"- **Updated:** {repo.get('updated_at', 'Unknown')}\n\n"
        
        if len(repos) > 20:
            result += f"... and {len(repos) - 20} more repositories\n"
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=result
                )
            ]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error listing repositories: {str(e)}"
                )
            ]
        )


async def get_repository_info(arguments: Dict[str, Any]) -> CallToolResult:
    """Get detailed information about a specific GitHub repository."""
    if not github_analyzer:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="GitHub token not configured. Please set GITHUB_TOKEN environment variable."
                )
            ]
        )
    
    repo_url = arguments.get("repository_url")
    if not repo_url:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Repository URL is required."
                )
            ]
        )
    
    try:
        repo_info = github_analyzer.get_repository_info(repo_url)
        
        if "error" in repo_info:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error: {repo_info['error']}"
                    )
                ]
            )
        
        # Format the results
        result = f"# Repository Information\n\n"
        result += f"## {repo_info.get('name', 'Unknown')}\n"
        result += f"- **Full Name:** {repo_info.get('full_name', 'Unknown')}\n"
        result += f"- **Description:** {repo_info.get('description', 'No description')}\n"
        result += f"- **Language:** {repo_info.get('language', 'Unknown')}\n"
        result += f"- **Stars:** {repo_info.get('stars', 0)}\n"
        result += f"- **Forks:** {repo_info.get('forks', 0)}\n"
        result += f"- **Open Issues:** {repo_info.get('open_issues', 0)}\n"
        result += f"- **License:** {repo_info.get('license', 'No license')}\n"
        result += f"- **Size:** {repo_info.get('size', 0)} KB\n"
        result += f"- **Default Branch:** {repo_info.get('default_branch', 'Unknown')}\n"
        result += f"- **Created:** {repo_info.get('created_at', 'Unknown')}\n"
        result += f"- **Updated:** {repo_info.get('updated_at', 'Unknown')}\n"
        result += f"- **URL:** {repo_info.get('url', 'N/A')}\n"
        result += f"- **Clone URL:** {repo_info.get('clone_url', 'N/A')}\n"
        
        if repo_info.get('topics'):
            result += f"- **Topics:** {', '.join(repo_info['topics'])}\n"
        
        result += f"- **Has Wiki:** {repo_info.get('has_wiki', False)}\n"
        result += f"- **Has Issues:** {repo_info.get('has_issues', False)}\n"
        result += f"- **Has Projects:** {repo_info.get('has_projects', False)}\n"
        result += f"- **Has Downloads:** {repo_info.get('has_downloads', False)}\n"
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=result
                )
            ]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error getting repository info: {str(e)}"
                )
            ]
        )


async def create_trello_card(arguments: Dict[str, Any]) -> CallToolResult:
    """Create a single Trello card."""
    if not trello_manager:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Trello credentials not configured. Please set TRELLO_API_KEY, TRELLO_TOKEN, and TRELLO_BOARD_ID environment variables."
                )
            ]
        )
    
    title = arguments.get("title")
    description = arguments.get("description", "")
    list_name = arguments.get("list_name", "To Do")
    labels = arguments.get("labels", [])
    
    if not title:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Card title is required."
                )
            ]
        )
    
    try:
        card = trello_manager.create_card(
            title=title,
            description=description,
            list_name=list_name,
            labels=labels
        )
        
        if not card:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="Failed to create Trello card."
                    )
                ]
            )
        
        result = f"# Trello Card Created Successfully\n\n"
        result += f"## Card Details\n"
        result += f"- **Title:** {card.get('name', 'Unknown')}\n"
        result += f"- **Description:** {card.get('description', 'No description')}\n"
        result += f"- **List:** {card.get('list_name', 'Unknown')}\n"
        result += f"- **Labels:** {', '.join(card.get('labels', []))}\n"
        result += f"- **URL:** {card.get('url', 'N/A')}\n"
        result += f"- **ID:** {card.get('id', 'Unknown')}\n"
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=result
                )
            ]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error creating Trello card: {str(e)}"
                )
            ]
        )


async def main():
    """Run the MCP server."""
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="github-trello-analyzer",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main()) 