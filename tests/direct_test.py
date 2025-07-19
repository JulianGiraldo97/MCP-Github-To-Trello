"""
Direct Test Script

This script tests the core functionality directly without going through the MCP protocol.
"""

import os
import asyncio
import base64
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzers.github_analyzer import GitHubAnalyzer
from managers.trello_manager import TrelloManager
from analyzers.ai_analyzer import AIAnalyzer

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

async def test_ai_analysis():
    """Test AI analysis functionality."""
    print("\n🤖 Testing AI Analysis")
    print("=" * 40)
    
    try:
        ai_analyzer = AIAnalyzer(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        # Test with sample code
        sample_files = [
            {
                'path': 'test.py',
                'language': 'python',
                'code': '''
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
'''
            }
        ]
        
        # Create a mock repository object for testing
        class MockRepo:
            def get_contents(self, path):
                class MockContent:
                    def __init__(self, content):
                        self.content = base64.b64encode(content.encode()).decode()
                return MockContent(sample_files[0]['code'])
        
        mock_repo = MockRepo()
        analysis = ai_analyzer.analyze_repository_with_ai(mock_repo, sample_files)
        
        print("✅ AI analysis completed!")
        print(f"   Issues found: {len(analysis.issues)}")
        print(f"   Suggestions: {len(analysis.suggestions)}")
        print(f"   Code Quality Score: {analysis.code_quality_score}/100")
        print(f"   Security Score: {analysis.security_score}/100")
        print(f"   Maintainability Score: {analysis.maintainability_score}/100")
        
        if analysis.issues:
            print("   Sample issues:")
            for issue in analysis.issues[:2]:  # Show first 2 issues
                print(f"     - {issue.get('title', 'Unknown')} ({issue.get('severity', 'Unknown')})")
        
        return True
        
    except Exception as e:
        print(f"❌ AI analysis error: {e}")
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
        ai_analyzer = AIAnalyzer(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
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
        
        # Perform AI analysis
        print("🤖 Performing AI analysis...")
        sample_files = []
        contents = repo.get_contents("")
        for content in contents[:5]:  # Limit to 5 files for testing
            if hasattr(content, 'content'):
                sample_files.append({
                    'path': content.path,
                    'language': content.name.split('.')[-1] if '.' in content.name else 'unknown'
                })
        
        ai_analysis = ai_analyzer.analyze_repository_with_ai(repo, sample_files)
        
        # Combine analysis
        combined_analysis = {
            "issues": code_quality.get("issues", []) + ai_analysis.issues,
            "suggestions": code_quality.get("suggestions", []) + ai_analysis.suggestions,
            "score": (code_quality.get("score", 100) + ai_analysis.code_quality_score) // 2
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
    results["ai_analysis"] = await test_ai_analysis()
    
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