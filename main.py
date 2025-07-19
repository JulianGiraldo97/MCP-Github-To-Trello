#!/usr/bin/env python3
"""
MCP GitHub Repository Analyzer - Main Entry Point

This script serves as the main entry point for the MCP GitHub Repository Analyzer.
It can run the MCP server or execute other functionality.
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def run_mcp_server():
    """Run the MCP server."""
    from mcp_server import main as mcp_main
    import asyncio
    asyncio.run(mcp_main())

def run_workflow(repo_name):
    """Run the full MCP workflow."""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))
    from run_full_mcp_workflow import run_full_mcp_workflow
    run_full_mcp_workflow(repo_name)

def run_test():
    """Run the quick test."""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))
    from quick_test import quick_test
    quick_test()

def setup_trello():
    """Set up the Trello board."""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))
    from setup_trello_board import setup_trello_board
    setup_trello_board()

def test_ai():
    """Test AI analysis functionality."""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'examples'))
    from test_ai_analysis import test_ai_analysis, test_specific_file_analysis
    
    print("🤖 Testing AI Analysis...")
    test_ai_analysis()
    test_specific_file_analysis()

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="MCP GitHub Repository Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py server                    # Run the MCP server
  python main.py workflow                  # Run full workflow on default repo
  python main.py workflow owner/repo       # Run workflow on specific repo
  python main.py test                      # Run quick test
  python main.py setup-trello              # Set up Trello board
  python main.py ai-test                   # Test AI analysis functionality
        """
    )
    
    parser.add_argument(
        'command',
        choices=['server', 'workflow', 'test', 'setup-trello', 'ai-test'],
        help='Command to run'
    )
    
    parser.add_argument(
        'repo_name',
        nargs='?',
        default="JulianGiraldo97/taller-devops-maestria",
        help='Repository name (for workflow command)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'server':
        print("🚀 Starting MCP server...")
        run_mcp_server()
    elif args.command == 'workflow':
        print(f"🚀 Running full MCP workflow for {args.repo_name}...")
        run_workflow(args.repo_name)
    elif args.command == 'test':
        print("🧪 Running quick test...")
        run_test()
    elif args.command == 'setup-trello':
        print("🔧 Setting up Trello board...")
        setup_trello()
    elif args.command == 'ai-test':
        print("🤖 Testing AI analysis...")
        test_ai()

if __name__ == "__main__":
    main() 