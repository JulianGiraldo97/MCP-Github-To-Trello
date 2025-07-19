"""
Full MCP Workflow Runner

This script runs the complete MCP workflow:
1. Analyzes a GitHub repository
2. Identifies issues and suggestions
3. Creates Trello cards for all findings
4. Provides a comprehensive summary
"""

import os
import asyncio
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzers.github_analyzer import GitHubAnalyzer
from managers.trello_manager import TrelloManager
from analyzers.ai_analyzer import AIAnalyzer

# Load environment variables
load_dotenv()

def run_full_mcp_workflow(repo_name="JulianGiraldo97/practica-docker-microservices"):
    """Run the complete MCP workflow for repository analysis and Trello integration."""
    print("🚀 Full MCP Workflow - GitHub Repository Analysis & Trello Integration")
    print("=" * 80)
    
    # Check environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    trello_api_key = os.getenv("TRELLO_API_KEY")
    trello_token = os.getenv("TRELLO_TOKEN")
    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    
    if not github_token:
        print("❌ GitHub token not found!")
        return False
    
    if not all([trello_api_key, trello_token, trello_board_id]):
        print("❌ Trello credentials not found!")
        return False
    
    try:
        # Initialize components
        print("🔧 Initializing components...")
        github_analyzer = GitHubAnalyzer(github_token)
        trello_manager = TrelloManager(trello_api_key, trello_token, trello_board_id)
        
        # Initialize AI analyzer
        ai_analyzer = AIAnalyzer(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        print(f"✅ Components initialized")
        print(f"📊 Target repository: {repo_name}")
        
        # Step 1: Get repository information
        print("\n" + "="*50)
        print("STEP 1: Repository Information")
        print("="*50)
        
        repo_info = github_analyzer.get_repository_info(repo_name)
        if "error" in repo_info:
            print(f"❌ Error: {repo_info['error']}")
            return False
        
        print("✅ Repository information retrieved!")
        print(f"   Name: {repo_info.get('name', 'Unknown')}")
        print(f"   Language: {repo_info.get('language', 'Unknown')}")
        print(f"   Description: {repo_info.get('description', 'No description')}")
        print(f"   Stars: {repo_info.get('stars', 0)}")
        print(f"   Forks: {repo_info.get('forks', 0)}")
        print(f"   Open Issues: {repo_info.get('open_issues', 0)}")
        print(f"   Size: {repo_info.get('size', 0)} KB")
        print(f"   URL: {repo_info.get('url', 'N/A')}")
        
        # Step 2: Get repository object for analysis
        print("\n" + "="*50)
        print("STEP 2: Repository Analysis")
        print("="*50)
        
        repo = github_analyzer.get_repository(repo_name)
        if not repo:
            print("❌ Could not get repository object")
            return False
        
        # Step 3: Analyze repository structure
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
        
        # Step 4: Analyze code quality
        print("\n🔍 Analyzing code quality...")
        code_quality = github_analyzer.analyze_code_quality(repo)
        print("✅ Code quality analyzed!")
        print(f"   Quality Score: {code_quality.get('score', 0)}/100")
        print(f"   Issues Found: {len(code_quality.get('issues', []))}")
        print(f"   Suggestions: {len(code_quality.get('suggestions', []))}")
        
        # Step 5: Perform AI-powered code analysis
        print("\n🤖 Performing AI-powered code analysis...")
        
        # Initialize combined_analysis with basic results
        combined_analysis = {
            "issues": code_quality.get("issues", []),
            "suggestions": code_quality.get("suggestions", []),
            "score": code_quality.get("score", 70),
            "ai_scores": {"code_quality": 70, "security": 70, "maintainability": 70},
            "ai_analysis": "AI analysis was not available.",
            "files_analyzed": 0
        }
        
        try:
            # Get sample files for AI analysis
            sample_files = []
            contents = repo.get_contents("")
            
            # Collect files for analysis (limit to 15 files for cost efficiency)
            for content in contents[:15]:
                if hasattr(content, 'content'):  # It's a file, not a directory
                    sample_files.append({
                        'path': content.path,
                        'language': content.name.split('.')[-1] if '.' in content.name else 'unknown'
                    })
            
            print(f"📁 Found {len(sample_files)} files for AI analysis")
            
            ai_analysis = ai_analyzer.analyze_repository_with_ai(repo, sample_files)
            print("✅ AI analysis completed!")
            print(f"   AI Issues Found: {len(ai_analysis.issues)}")
            print(f"   AI Suggestions: {len(ai_analysis.suggestions)}")
            print(f"   Code Quality Score: {ai_analysis.code_quality_score}/100")
            print(f"   Security Score: {ai_analysis.security_score}/100")
            print(f"   Maintainability Score: {ai_analysis.maintainability_score}/100")
            
            # Use AI analysis as the primary analysis
            combined_analysis["issues"] = ai_analysis.issues
            combined_analysis["suggestions"] = ai_analysis.suggestions
            combined_analysis["score"] = (ai_analysis.code_quality_score + ai_analysis.security_score + ai_analysis.maintainability_score) // 3
            combined_analysis["ai_scores"] = {
                "code_quality": ai_analysis.code_quality_score,
                "security": ai_analysis.security_score,
                "maintainability": ai_analysis.maintainability_score
            }
            combined_analysis["ai_analysis"] = ai_analysis.detailed_analysis
            combined_analysis["files_analyzed"] = len(sample_files)
            
        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}")
            print("   Using basic structural analysis only...")
        
        # Step 7: Get recent issues and commits
        print("\n📋 Getting recent GitHub issues...")
        try:
            recent_issues = github_analyzer.get_recent_issues(repo, limit=10)
            print(f"✅ Found {len(recent_issues)} recent issues")
        except Exception as e:
            print(f"⚠️  Could not fetch issues: {e}")
            recent_issues = []
        
        print("\n📝 Getting recent commits...")
        try:
            recent_commits = github_analyzer.get_recent_commits(repo, limit=10)
            print(f"✅ Found {len(recent_commits)} recent commits")
        except Exception as e:
            print(f"⚠️  Could not fetch commits: {e}")
            recent_commits = []
        
        # Step 8: Combine all analysis results
        print("\n" + "="*50)
        print("STEP 3: Combining Analysis Results")
        print("="*50)
        
        print(f"✅ Analysis combined!")
        print(f"   Total Issues: {len(combined_analysis['issues'])}")
        print(f"   Total Suggestions: {len(combined_analysis['suggestions'])}")
        print(f"   Final Score: {combined_analysis['score']}/100")
        
        # Step 9: Create Trello cards
        print("\n" + "="*50)
        print("STEP 4: Creating Trello Cards")
        print("="*50)
        
        print("📝 Creating analysis cards...")
        analysis_cards = trello_manager.create_analysis_cards(combined_analysis, repo_info["full_name"])
        print(f"✅ Created {len(analysis_cards)} analysis cards")
        
        print("📝 Creating issue cards...")
        issue_cards = trello_manager.create_issue_cards(recent_issues, repo_info["full_name"])
        print(f"✅ Created {len(issue_cards)} issue cards")
        
        print("📝 Creating summary card...")
        total_cards = len(analysis_cards) + len(issue_cards)
        summary_card = trello_manager.create_summary_card(repo_info, combined_analysis, total_cards)
        if summary_card:
            print("✅ Created summary card")
        else:
            print("⚠️  Could not create summary card")
        
        # Step 10: Final summary
        print("\n" + "="*50)
        print("STEP 5: Final Summary")
        print("="*50)
        
        print("📊 Repository Analysis Summary")
        print(f"   Repository: {repo_info.get('full_name', 'Unknown')}")
        print(f"   Language: {repo_info.get('language', 'Unknown')}")
        print(f"   Quality Score: {combined_analysis['score']}/100")
        print(f"   Issues Found: {len(combined_analysis['issues'])}")
        print(f"   Suggestions: {len(combined_analysis['suggestions'])}")
        print(f"   Files Analyzed: {combined_analysis.get('files_analyzed', 0)}")
        print(f"   Recent Issues: {len(recent_issues)}")
        print(f"   Recent Commits: {len(recent_commits)}")
        
        # Show AI analysis results if available
        if combined_analysis.get('ai_scores'):
            print("\n🤖 AI Analysis Results:")
            ai_scores = combined_analysis['ai_scores']
            print(f"   Code Quality Score: {ai_scores.get('code_quality', 70)}/100")
            print(f"   Security Score: {ai_scores.get('security', 70)}/100")
            print(f"   Maintainability Score: {ai_scores.get('maintainability', 70)}/100")
            print(f"   AI Issues Found: {len(combined_analysis.get('ai_issues', []))}")
            print(f"   AI Suggestions: {len(combined_analysis.get('ai_suggestions', []))}")
        
        print("\n📋 Trello Integration Summary")
        print(f"   Analysis Cards Created: {len(analysis_cards)}")
        print(f"   Issue Cards Created: {len(issue_cards)}")
        print(f"   Summary Card Created: {'Yes' if summary_card else 'No'}")
        print(f"   Total Cards Created: {total_cards + (1 if summary_card else 0)}")
        print(f"   Trello Board: {trello_manager.board.url if trello_manager.board else 'N/A'}")
        
        # Show detailed issues
        if combined_analysis.get('issues'):
            print("\n🚨 Issues Found:")
            for i, issue in enumerate(combined_analysis['issues'], 1):
                print(f"   {i}. {issue.get('severity', 'Unknown').upper()}: {issue.get('title', 'Unknown')}")
                print(f"      {issue.get('description', 'No description')}")
        
        # Show detailed suggestions
        if combined_analysis.get('suggestions'):
            print("\n💡 Suggestions:")
            for i, suggestion in enumerate(combined_analysis['suggestions'], 1):
                print(f"   {i}. {suggestion.get('title', 'Unknown')}")
                print(f"      {suggestion.get('description', 'No description')}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        if combined_analysis['score'] < 80:
            print("   - Consider addressing the issues found to improve code quality")
        if not structure.get('has_readme'):
            print("   - Add a README.md file to document your project")
        if not structure.get('has_license'):
            print("   - Consider adding a license file")
        if not structure.get('has_tests'):
            print("   - Consider adding tests to improve code reliability")
        if not structure.get('has_github_actions'):
            print("   - Consider adding GitHub Actions for CI/CD")
        if total_cards > 0:
            print("   - Check your Trello board for detailed task cards")
        
        print("\n✨ Full MCP workflow completed successfully!")
        print("🎯 Check your Trello board to see all the created cards!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during MCP workflow: {e}")
        return False

def main():
    """Main function to run the MCP workflow."""
    print("🎯 MCP GitHub Repository Analyzer - Full Workflow")
    print("=" * 60)
    
    # You can change the repository here
    repo_name = "JulianGiraldo97/practica-docker-microservices"
    
    success = run_full_mcp_workflow(repo_name)
    
    if success:
        print("\n🎉 Workflow completed successfully!")
        print("📋 Check your Trello board for the created cards")
    else:
        print("\n❌ Workflow failed. Check the error messages above.")

if __name__ == "__main__":
    main() 