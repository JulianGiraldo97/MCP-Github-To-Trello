"""
GitHub Repository Analyzer

This module handles GitHub API interactions and repository analysis.
"""

import os
import re
from typing import Dict, List, Optional, Any
from github import Github, Repository, ContentFile
from github.GithubException import GithubException
import base64


class GitHubAnalyzer:
    def __init__(self, token: str):
        """Initialize GitHub analyzer with API token."""
        self.github = Github(token)
        self.token = token

    def get_repository(self, repo_url: str) -> Optional[Repository]:
        """Extract repository from URL and return GitHub repository object."""
        try:
            # Extract owner/repo from various URL formats
            if 'github.com' in repo_url:
                # Handle URLs like https://github.com/owner/repo
                parts = repo_url.split('github.com/')[-1].split('/')
                if len(parts) >= 2:
                    owner, repo_name = parts[0], parts[1]
                    return self.github.get_repo(f"{owner}/{repo_name}")
            else:
                # Assume it's already in owner/repo format
                return self.github.get_repo(repo_url)
        except GithubException as e:
            print(f"Error accessing repository: {e}")
            return None
        return None

    def get_repository_info(self, repo_url: str) -> Dict[str, Any]:
        """Get comprehensive repository information."""
        repo = self.get_repository(repo_url)
        if not repo:
            return {"error": "Could not access repository"}

        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "url": repo.html_url,
            "clone_url": repo.clone_url,
            "default_branch": repo.default_branch,
            "topics": repo.get_topics(),
            "license": repo.license.name if repo.license else None,
            "size": repo.size,  # Size in KB
            "has_wiki": repo.has_wiki,
            "has_issues": repo.has_issues,
            "has_projects": repo.has_projects,
            "has_downloads": repo.has_downloads,
        }

    def list_repositories(self, username: str) -> List[Dict[str, Any]]:
        """List repositories for a given user/organization."""
        try:
            user = self.github.get_user(username)
            repos = []
            for repo in user.get_repos():
                repos.append({
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "language": repo.language,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "url": repo.html_url,
                    "private": repo.private,
                    "updated_at": repo.updated_at.isoformat(),
                })
            return repos
        except GithubException as e:
            return [{"error": f"Could not fetch repositories: {e}"}]

    def get_file_content(self, repo: Repository, path: str) -> Optional[str]:
        """Get content of a specific file from the repository."""
        try:
            content = repo.get_contents(path)
            if isinstance(content, ContentFile):
                # Decode content from base64
                return base64.b64decode(content.content).decode('utf-8')
            return None
        except GithubException:
            return None

    def analyze_repository_structure(self, repo: Repository) -> Dict[str, Any]:
        """Analyze the repository structure and identify key files."""
        try:
            contents = repo.get_contents("")
            structure = {
                "has_readme": False,
                "has_license": False,
                "has_requirements": False,
                "has_dockerfile": False,
                "has_github_actions": False,
                "has_tests": False,
                "files": [],
                "directories": []
            }

            for content in contents:
                name = content.name.lower()
                if name == "readme.md" or name.startswith("readme"):
                    structure["has_readme"] = True
                elif name == "license" or name.startswith("license"):
                    structure["has_license"] = True
                elif name in ["requirements.txt", "pyproject.toml", "setup.py", "package.json"]:
                    structure["has_requirements"] = True
                elif name == "dockerfile":
                    structure["has_dockerfile"] = True
                elif name == ".github":
                    structure["has_github_actions"] = True
                elif name in ["tests", "test", "spec", "__tests__"]:
                    structure["has_tests"] = True

                if content.type == "dir":
                    structure["directories"].append(content.name)
                else:
                    structure["files"].append(content.name)

            return structure
        except GithubException as e:
            return {"error": f"Could not analyze repository structure: {e}"}

    def get_recent_issues(self, repo: Repository, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent issues from the repository."""
        try:
            issues = []
            for issue in repo.get_issues(state='open')[:limit]:
                issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body,
                    "state": issue.state,
                    "labels": [label.name for label in issue.labels],
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "user": issue.user.login,
                })
            return issues
        except GithubException:
            return []

    def get_recent_commits(self, repo: Repository, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commits from the repository."""
        try:
            commits = []
            for commit in repo.get_commits()[:limit]:
                commits.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat(),
                    "url": commit.html_url,
                })
            return commits
        except GithubException:
            return []

    def analyze_code_quality(self, repo: Repository) -> Dict[str, Any]:
        """Analyze code quality by examining key files."""
        analysis = {
            "issues": [],
            "suggestions": [],
            "score": 100  # Start with perfect score
        }

        # Check for README
        readme_content = self.get_file_content(repo, "README.md")
        if not readme_content:
            analysis["issues"].append({
                "type": "documentation",
                "severity": "medium",
                "title": "Missing README.md",
                "description": "Repository lacks a README file which is essential for project documentation."
            })
            analysis["score"] -= 10

        # Check for license
        license_files = ["LICENSE", "LICENSE.md", "LICENSE.txt"]
        has_license = any(self.get_file_content(repo, f) for f in license_files)
        if not has_license:
            analysis["issues"].append({
                "type": "legal",
                "severity": "medium",
                "title": "Missing License",
                "description": "Repository does not have a license file, which may limit its usability."
            })
            analysis["score"] -= 5

        # Check for requirements/dependencies
        req_files = ["requirements.txt", "pyproject.toml", "setup.py", "package.json"]
        has_requirements = any(self.get_file_content(repo, f) for f in req_files)
        if not has_requirements:
            analysis["issues"].append({
                "type": "setup",
                "severity": "high",
                "title": "Missing Dependencies File",
                "description": "No dependency management file found, making it difficult to set up the project."
            })
            analysis["score"] -= 15

        # Check for tests
        test_dirs = ["tests", "test", "spec", "__tests__"]
        has_tests = any(self.get_file_content(repo, f"{d}/") for d in test_dirs)
        if not has_tests:
            analysis["issues"].append({
                "type": "testing",
                "severity": "medium",
                "title": "Missing Tests",
                "description": "No test directory found, which may indicate lack of testing."
            })
            analysis["score"] -= 10

        # Check for CI/CD
        if not self.get_file_content(repo, ".github/workflows/"):
            analysis["suggestions"].append({
                "type": "ci_cd",
                "title": "Consider Adding CI/CD",
                "description": "Adding GitHub Actions or other CI/CD would improve development workflow."
            })

        return analysis 