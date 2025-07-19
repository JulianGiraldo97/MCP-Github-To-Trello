#!/usr/bin/env python3
"""
Test AI Analysis Functionality

This script demonstrates how to use the AI-powered code analyzer.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzers.github_analyzer import GitHubAnalyzer
from analyzers.ai_analyzer import AIAnalyzer

def test_ai_analysis():
    """Test the AI analysis functionality."""
    
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not github_token:
        print("❌ GitHub token not found!")
        return False
    
    if not openai_api_key and not anthropic_api_key:
        print("⚠️  No AI API keys found. Will use fallback analysis.")
        print("   To enable AI analysis, add OPENAI_API_KEY or ANTHROPIC_API_KEY to your .env file")
    
    # Initialize analyzers
    github_analyzer = GitHubAnalyzer(github_token)
    ai_analyzer = AIAnalyzer(
        openai_api_key=openai_api_key,
        anthropic_api_key=anthropic_api_key
    )
    
    # Test repository
    repo_name = "JulianGiraldo97/practica-docker-microservices"
    
    print(f"🤖 Testing AI Analysis on: {repo_name}")
    print("=" * 60)
    
    # Get repository
    repo = github_analyzer.get_repository(repo_name)
    if not repo:
        print("❌ Could not access repository")
        return False
    
    # Get some sample files for analysis
    print("📁 Getting sample files for AI analysis...")
    try:
        contents = repo.get_contents("")
        sample_files = []
        
        for content in contents[:5]:  # Limit to 5 files for testing
            if hasattr(content, 'content'):  # It's a file, not a directory
                sample_files.append({
                    'path': content.path,
                    'language': content.name.split('.')[-1] if '.' in content.name else 'unknown'
                })
        
        print(f"✅ Found {len(sample_files)} sample files")
        
        # Perform AI analysis
        print("\n🤖 Performing AI analysis...")
        ai_result = ai_analyzer.analyze_repository_with_ai(repo, sample_files)
        
        # Display results
        print("\n📊 AI Analysis Results:")
        print(f"   Code Quality Score: {ai_result.code_quality_score}/100")
        print(f"   Security Score: {ai_result.security_score}/100")
        print(f"   Maintainability Score: {ai_result.maintainability_score}/100")
        print(f"   Issues Found: {len(ai_result.issues)}")
        print(f"   Suggestions: {len(ai_result.suggestions)}")
        
        # Show detailed issues
        if ai_result.issues:
            print("\n🚨 AI Issues Found:")
            for i, issue in enumerate(ai_result.issues, 1):
                print(f"   {i}. {issue.get('severity', 'Unknown').upper()}: {issue.get('title', 'Unknown')}")
                print(f"      Type: {issue.get('type', 'Unknown')}")
                print(f"      File: {issue.get('file', 'N/A')}")
                print(f"      Description: {issue.get('description', 'No description')}")
                if issue.get('suggestion'):
                    print(f"      Suggestion: {issue['suggestion']}")
                print()
        
        # Show detailed suggestions
        if ai_result.suggestions:
            print("\n💡 AI Suggestions:")
            for i, suggestion in enumerate(ai_result.suggestions, 1):
                print(f"   {i}. {suggestion.get('title', 'Unknown')}")
                print(f"      Type: {suggestion.get('type', 'Unknown')}")
                print(f"      Priority: {suggestion.get('priority', 'Unknown')}")
                print(f"      Description: {suggestion.get('description', 'No description')}")
                if suggestion.get('impact'):
                    print(f"      Impact: {suggestion['impact']}")
                print()
        
        # Show detailed analysis
        if ai_result.detailed_analysis:
            print("\n📋 Detailed AI Analysis:")
            print(ai_result.detailed_analysis)
        
        print("\n✅ AI analysis test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")
        return False

def test_specific_file_analysis():
    """Test AI analysis on a specific file."""
    
    load_dotenv()
    
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not github_token:
        print("❌ GitHub token not found!")
        return False
    
    github_analyzer = GitHubAnalyzer(github_token)
    ai_analyzer = AIAnalyzer(openai_api_key=openai_api_key)
    
    repo_name = "JulianGiraldo97/practica-docker-microservices"
    file_path = "pom.xml"  # Example file
    
    print(f"\n🔍 Testing AI analysis on specific file: {file_path}")
    print("=" * 60)
    
    repo = github_analyzer.get_repository(repo_name)
    if not repo:
        print("❌ Could not access repository")
        return False
    
    try:
        result = ai_analyzer.analyze_specific_file(repo, file_path)
        
        if "error" in result:
            print(f"❌ {result['error']}")
            return False
        
        print("✅ File analysis completed!")
        print(f"   Issues: {len(result.get('issues', []))}")
        print(f"   Suggestions: {len(result.get('suggestions', []))}")
        print(f"   Overall Score: {result.get('overall_score', 'N/A')}/100")
        
        if result.get('summary'):
            print(f"   Summary: {result['summary']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        return False

if __name__ == "__main__":
    print("🤖 AI Analysis Test Suite")
    print("=" * 60)
    
    # Test repository analysis
    success1 = test_ai_analysis()
    
    # Test specific file analysis
    success2 = test_specific_file_analysis()
    
    if success1 and success2:
        print("\n🎉 All AI analysis tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.") 