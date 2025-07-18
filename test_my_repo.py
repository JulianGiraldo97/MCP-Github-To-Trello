"""
Test My Repository

This script performs a comprehensive analysis of your repository.
"""

import os
from dotenv import load_dotenv
from github_analyzer import GitHubAnalyzer
from code_analyzer import CodeAnalyzer

# Load environment variables
load_dotenv()

def analyze_my_repository():
    """Analyze the user's repository comprehensively."""
    print("🔍 Analyzing Your Repository: JulianGiraldo97/practica-docker-microservices")
    print("=" * 70)
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GitHub token not found!")
        return
    
    try:
        # Initialize analyzers
        github_analyzer = GitHubAnalyzer(github_token)
        code_analyzer = CodeAnalyzer()
        
        repo_name = "JulianGiraldo97/practica-docker-microservices"
        
        # Get repository info
        print("📊 Getting repository information...")
        repo_info = github_analyzer.get_repository_info(repo_name)
        
        if "error" in repo_info:
            print(f"❌ Error: {repo_info['error']}")
            return
        
        print("✅ Repository information retrieved!")
        print(f"   Name: {repo_info.get('name', 'Unknown')}")
        print(f"   Language: {repo_info.get('language', 'Unknown')}")
        print(f"   Description: {repo_info.get('description', 'No description')}")
        print(f"   Stars: {repo_info.get('stars', 0)}")
        print(f"   Forks: {repo_info.get('forks', 0)}")
        print(f"   Open Issues: {repo_info.get('open_issues', 0)}")
        print(f"   Size: {repo_info.get('size', 0)} KB")
        print(f"   Created: {repo_info.get('created_at', 'Unknown')}")
        print(f"   Updated: {repo_info.get('updated_at', 'Unknown')}")
        
        # Get repository object for analysis
        print("\n🔍 Getting repository for analysis...")
        repo = github_analyzer.get_repository(repo_name)
        if not repo:
            print("❌ Could not get repository object")
            return
        
        # Analyze repository structure
        print("\n📁 Analyzing repository structure...")
        structure = github_analyzer.analyze_repository_structure(repo)
        print("✅ Repository structure analyzed!")
        print(f"   Has README: {structure.get('has_readme', False)}")
        print(f"   Has License: {structure.get('has_license', False)}")
        print(f"   Has Requirements: {structure.get('has_requirements', False)}")
        print(f"   Has Dockerfile: {structure.get('has_dockerfile', False)}")
        print(f"   Has GitHub Actions: {structure.get('has_github_actions', False)}")
        print(f"   Has Tests: {structure.get('has_tests', False)}")
        
        if structure.get('files'):
            print(f"   Files: {', '.join(structure['files'][:10])}{'...' if len(structure['files']) > 10 else ''}")
        
        if structure.get('directories'):
            print(f"   Directories: {', '.join(structure['directories'][:10])}{'...' if len(structure['directories']) > 10 else ''}")
        
        # Analyze code quality
        print("\n🔍 Analyzing code quality...")
        code_quality = github_analyzer.analyze_code_quality(repo)
        print("✅ Code quality analyzed!")
        print(f"   Quality Score: {code_quality.get('score', 0)}/100")
        print(f"   Issues Found: {len(code_quality.get('issues', []))}")
        print(f"   Suggestions: {len(code_quality.get('suggestions', []))}")
        
        # Show issues
        if code_quality.get('issues'):
            print("\n🚨 Issues Found:")
            for issue in code_quality['issues']:
                print(f"   - {issue.get('severity', 'Unknown').upper()}: {issue.get('title', 'Unknown')}")
                print(f"     {issue.get('description', 'No description')}")
        
        # Show suggestions
        if code_quality.get('suggestions'):
            print("\n💡 Suggestions:")
            for suggestion in code_quality['suggestions']:
                print(f"   - {suggestion.get('title', 'Unknown')}")
                print(f"     {suggestion.get('description', 'No description')}")
        
        # Perform detailed code analysis
        print("\n🔍 Performing detailed code analysis...")
        code_analysis = code_analyzer.analyze_repository_files(repo, max_files=20)  # Limit for faster analysis
        print("✅ Detailed code analysis completed!")
        print(f"   Files Analyzed: {code_analysis.get('analyzed_files', 0)}")
        print(f"   Total Files Found: {code_analysis.get('total_files_found', 0)}")
        print(f"   Code Issues Found: {len(code_analysis.get('issues', []))}")
        print(f"   Code Suggestions: {len(code_analysis.get('suggestions', []))}")
        
        # Show code analysis issues
        if code_analysis.get('issues'):
            print("\n🔍 Code Analysis Issues:")
            for issue in code_analysis['issues'][:5]:  # Show first 5
                print(f"   - {issue.get('severity', 'Unknown').upper()}: {issue.get('title', 'Unknown')}")
                if issue.get('line'):
                    print(f"     Line {issue.get('line')}: {issue.get('code', 'No code shown')}")
        
        # Get recent issues
        print("\n📋 Getting recent GitHub issues...")
        recent_issues = github_analyzer.get_recent_issues(repo, limit=5)
        print(f"✅ Found {len(recent_issues)} recent issues")
        
        if recent_issues:
            print("   Recent Issues:")
            for issue in recent_issues:
                print(f"   - #{issue.get('number', 'Unknown')}: {issue.get('title', 'Unknown')}")
                print(f"     Labels: {', '.join(issue.get('labels', []))}")
        
        # Get recent commits
        print("\n📝 Getting recent commits...")
        recent_commits = github_analyzer.get_recent_commits(repo, limit=5)
        print(f"✅ Found {len(recent_commits)} recent commits")
        
        if recent_commits:
            print("   Recent Commits:")
            for commit in recent_commits:
                print(f"   - {commit.get('sha', 'Unknown')[:8]}: {commit.get('message', 'Unknown').split('\n')[0]}")
                print(f"     By: {commit.get('author', 'Unknown')}")
        
        # Summary
        print("\n📊 Analysis Summary")
        print("=" * 30)
        total_issues = len(code_quality.get('issues', [])) + len(code_analysis.get('issues', []))
        total_suggestions = len(code_quality.get('suggestions', [])) + len(code_analysis.get('suggestions', []))
        
        print(f"Repository: {repo_info.get('full_name', 'Unknown')}")
        print(f"Language: {repo_info.get('language', 'Unknown')}")
        print(f"Quality Score: {code_quality.get('score', 0)}/100")
        print(f"Total Issues: {total_issues}")
        print(f"Total Suggestions: {total_suggestions}")
        print(f"Files Analyzed: {code_analysis.get('analyzed_files', 0)}")
        print(f"Recent Issues: {len(recent_issues)}")
        print(f"Recent Commits: {len(recent_commits)}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        if code_quality.get('score', 100) < 80:
            print("   - Consider addressing the issues found to improve code quality")
        if not structure.get('has_readme'):
            print("   - Add a README.md file to document your project")
        if not structure.get('has_license'):
            print("   - Consider adding a license file")
        if not structure.get('has_tests'):
            print("   - Consider adding tests to improve code reliability")
        if total_issues == 0:
            print("   - Great job! No major issues found in your codebase")
        
        print("\n✨ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    analyze_my_repository() 