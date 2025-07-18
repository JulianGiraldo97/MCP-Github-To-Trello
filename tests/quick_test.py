"""
Quick Test Script

This script quickly tests the essential functionality.
"""

import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzers.github_analyzer import GitHubAnalyzer
from managers.trello_manager import TrelloManager

# Load environment variables
load_dotenv()

def quick_test():
    """Run a quick test of the core functionality."""
    print("⚡ Quick MCP Test")
    print("=" * 30)
    
    # Test GitHub
    print("🔍 Testing GitHub...")
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        try:
            analyzer = GitHubAnalyzer(github_token)
            repo_info = analyzer.get_repository_info("JulianGiraldo97/practica-docker-microservices")
            if "error" not in repo_info:
                print(f"✅ GitHub: {repo_info.get('name', 'Unknown')} ({repo_info.get('language', 'Unknown')})")
            else:
                print(f"❌ GitHub: {repo_info['error']}")
        except Exception as e:
            print(f"❌ GitHub: {e}")
    else:
        print("❌ GitHub: No token")
    
    # Test Trello
    print("📋 Testing Trello...")
    trello_api_key = os.getenv("TRELLO_API_KEY")
    trello_token = os.getenv("TRELLO_TOKEN")
    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    
    if all([trello_api_key, trello_token, trello_board_id]):
        try:
            trello = TrelloManager(trello_api_key, trello_token, trello_board_id)
            lists = trello.get_lists()
            print(f"✅ Trello: {len(lists)} lists found")
            
            # Create a quick test card
            test_card = trello.create_card(
                title="Quick Test - MCP Working!",
                description="This card was created by the MCP GitHub Repository Analyzer",
                list_name="To Do",
                labels=["test", "mcp"]
            )
            if test_card:
                print(f"✅ Trello: Test card created (ID: {test_card.get('id', 'Unknown')})")
            else:
                print("❌ Trello: Failed to create test card")
        except Exception as e:
            print(f"❌ Trello: {e}")
    else:
        print("❌ Trello: Missing credentials")
    
    print("\n✨ Quick test completed!")

if __name__ == "__main__":
    quick_test() 