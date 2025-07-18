"""
Direct Test Script

This script tests the core functionality directly without going through the MCP protocol.
"""

import os
import asyncio
from dotenv import load_dotenv
from github_analyzer import GitHubAnalyzer
from trello_manager import TrelloManager
from code_analyzer import CodeAnalyzer

# Load environment variables
load_dotenv()

async def test_github_integration():
    """Test GitHub integration directly."""
    print("🔍 Testing GitHub Integration")
    print("=" * 40)
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GitHub token not found!")
        return False
    
    try:
        analyzer = GitHubAnalyzer(github_token)
        
        # Test getting repository info
        print("📊 Testing repository info...")
        repo_info = analyzer.get_repository_info("microsoft/vscode")
        
        if "error" in repo_info:
            print(f"❌ Error: {repo_info['error']}")
            return False
        
        print("✅ Repository info retrieved successfully!")
        print(f"   Name: {repo_info.get('name', 'Unknown')}")
        print(f"   Language: {repo_info.get('language', 'Unknown')}")
        print(f"   Stars: {repo_info.get('stars', 0)}")
        print(f"   Forks: {repo_info.get('forks', 0)}")
        
        # Test listing repositories
        print("\n📋 Testing repository listing...")
        repos = analyzer.list_repositories("microsoft")
        
        if not repos or "error" in repos[0]:
            print(f"❌ Error listing repositories: {repos[0].get('error', 'Unknown error')}")
            return False
        
        print(f"✅ Found {len(repos)} repositories for Microsoft")
        print(f"   First repo: {repos[0].get('name', 'Unknown')}")
        
        # Test repository analysis
        print("\n🔍 Testing repository analysis...")
        repo = analyzer.get_repository("microsoft/vscode")
        if not repo:
            print("❌ Could not get repository object")
            return False
        
        structure = analyzer.analyze_repository_structure(repo)
        print("✅ Repository structure analyzed!")
        print(f"   Has README: {structure.get('has_readme', False)}")
        print(f"   Has License: {structure.get('has_license', False)}")
        print(f"   Has Tests: {structure.get('has_tests', False)}")
        
        code_quality = analyzer.analyze_code_quality(repo)
        print("✅ Code quality analyzed!")
        print(f"   Quality Score: {code_quality.get('score', 0)}/100")
        print(f"   Issues Found: {len(code_quality.get('issues', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ GitHub integration error: {e}")
        return False

async def test_trello_integration():
    """Test Trello integration directly."""
    print("\n📋 Testing Trello Integration")
    print("=" * 40)
    
    trello_api_key = os.getenv("TRELLO_API_KEY")
    trello_token = os.getenv("TRELLO_TOKEN")
    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    
    if not all([trello_api_key, trello_token, trello_board_id]):
        print("❌ Trello credentials not found!")
        return False
    
    try:
        trello = TrelloManager(trello_api_key, trello_token, trello_board_id)
        
        # Test getting lists
        print("📋 Testing list retrieval...")
        lists = trello.get_lists()
        print(f"✅ Found {len(lists)} lists in the board")
        for lst in lists[:3]:  # Show first 3 lists
            print(f"   - {lst.get('name', 'Unknown')}")
        
        # Test getting labels
        print("\n🏷️  Testing label retrieval...")
        labels = trello.get_labels()
        print(f"✅ Found {len(labels)} labels in the board")
        for label in labels[:3]:  # Show first 3 labels
            print(f"   - {label.get('name', 'Unknown')} ({label.get('color', 'Unknown')})")
        
        # Test creating a card
        print("\n📝 Testing card creation...")
        test_card = trello.create_card(
            title="Test Card - MCP Integration",
            description="This is a test card created by the MCP GitHub Repository Analyzer",
            list_name="To Do",
            labels=["test", "mcp"]
        )
        
        if test_card:
            print("✅ Test card created successfully!")
            print(f"   Card ID: {test_card.get('id', 'Unknown')}")
            print(f"   Card URL: {test_card.get('url', 'N/A')}")
        else:
            print("❌ Failed to create test card")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Trello integration error: {e}")
        return False

async def test_code_analysis():
    """Test code analysis functionality."""
    print("\n🔍 Testing Code Analysis")
    print("=" * 40)
    
    try:
        analyzer = CodeAnalyzer()
        
        # Test with sample code
        sample_code = """
# Sample Python file with issues
import os
import sys

password = "secret123"  # Security issue
api_key = "abc123"      # Security issue

def main():
    print("Hello World")  # Code quality issue
    # TODO: Add error handling  # Code quality issue
    
    for i in range(10):
        for j in range(10):  # Performance issue
            pass
    
    eval("print('dangerous')")  # Security issue
"""
        
        analysis = analyzer.analyze_file_content(sample_code, "test.py")
        
        print("✅ Code analysis completed!")
        print(f"   Issues found: {len(analysis.get('issues', []))}")
        print(f"   Suggestions: {len(analysis.get('suggestions', []))}")
        
        if analysis.get("issues"):
            print("   Sample issues:")
            for issue in analysis["issues"][:2]:  # Show first 2 issues
                print(f"     - {issue.get('title', 'Unknown')} ({issue.get('severity', 'Unknown')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Code analysis error: {e}")
        return False

async def test_full_workflow():
    """Test the complete workflow."""
    print("\n🚀 Testing Full Workflow")
    print("=" * 40)
    
    github_token = os.getenv("GITHUB_TOKEN")
    trello_api_key = os.getenv("TRELLO_API_KEY")
    trello_token = os.getenv("TRELLO_TOKEN")
    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    
    if not all([github_token, trello_api_key, trello_token, trello_board_id]):
        print("❌ Missing required API keys for full workflow test")
        return False
    
    try:
        # Initialize components
        github_analyzer = GitHubAnalyzer(github_token)
        trello_manager = TrelloManager(trello_api_key, trello_token, trello_board_id)
        code_analyzer = CodeAnalyzer()
        
        # Get repository
        print("📊 Getting repository...")
        repo = github_analyzer.get_repository("microsoft/vscode")
        if not repo:
            print("❌ Could not access repository")
            return False
        
        # Get repository info
        repo_info = github_analyzer.get_repository_info("microsoft/vscode")
        
        # Analyze repository
        print("🔍 Analyzing repository...")
        structure = github_analyzer.analyze_repository_structure(repo)
        code_quality = github_analyzer.analyze_code_quality(repo)
        code_analysis = code_analyzer.analyze_repository_files(repo, max_files=10)  # Limit for testing
        
        # Combine analysis
        combined_analysis = {
            "issues": code_quality.get("issues", []) + code_analysis.get("issues", []),
            "suggestions": code_quality.get("suggestions", []) + code_analysis.get("suggestions", []),
            "score": code_quality.get("score", 100)
        }
        
        print(f"✅ Analysis completed! Score: {combined_analysis['score']}/100")
        print(f"   Issues: {len(combined_analysis['issues'])}")
        print(f"   Suggestions: {len(combined_analysis['suggestions'])}")
        
        # Create Trello cards
        print("📝 Creating Trello cards...")
        analysis_cards = trello_manager.create_analysis_cards(combined_analysis, repo_info["full_name"])
        summary_card = trello_manager.create_summary_card(repo_info, combined_analysis, len(analysis_cards))
        
        print(f"✅ Created {len(analysis_cards)} analysis cards")
        if summary_card:
            print("✅ Created summary card")
        
        return True
        
    except Exception as e:
        print(f"❌ Full workflow error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 MCP GitHub Repository Analyzer - Direct Tests")
    print("=" * 60)
    
    results = {}
    
    # Test individual components
    results["github"] = await test_github_integration()
    results["trello"] = await test_trello_integration()
    results["code_analysis"] = await test_code_analysis()
    
    # Test full workflow
    results["full_workflow"] = await test_full_workflow()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test.replace('_', ' ').title()}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed! Your MCP system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return all_passed

if __name__ == "__main__":
    asyncio.run(main()) 