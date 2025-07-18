"""
Code Analyzer

This module performs static code analysis to identify potential issues and improvements.
"""

import re
from typing import Dict, List, Any, Optional
from github import Repository


class CodeAnalyzer:
    def __init__(self):
        """Initialize the code analyzer."""
        self.issue_patterns = {
            "security": [
                r"password\s*=\s*['\"][^'\"]+['\"]",  # Hardcoded passwords
                r"api_key\s*=\s*['\"][^'\"]+['\"]",   # Hardcoded API keys
                r"secret\s*=\s*['\"][^'\"]+['\"]",    # Hardcoded secrets
                r"eval\s*\(",                          # eval() usage
                r"exec\s*\(",                          # exec() usage
                r"os\.system\s*\(",                    # os.system() usage
                r"subprocess\.call\s*\(",              # subprocess.call() usage
            ],
            "code_quality": [
                r"TODO:",                              # TODO comments
                r"FIXME:",                             # FIXME comments
                r"XXX:",                               # XXX comments
                r"HACK:",                              # HACK comments
                r"print\s*\(",                         # print statements (in production code)
                r"debugger;",                          # debugger statements
                r"console\.log\s*\(",                  # console.log statements
            ],
            "performance": [
                r"for\s+.*\s+in\s+.*:\s*\n.*\s+for\s+.*\s+in\s+.*:",  # Nested loops
                r"while\s+True:",                      # Infinite loops
                r"import\s+\*",                        # Wildcard imports
            ]
        }

    def analyze_file_content(self, content: str, filename: str) -> Dict[str, Any]:
        """Analyze a single file for potential issues."""
        if not content:
            return {"issues": [], "suggestions": []}

        issues = []
        suggestions = []
        
        # Determine file type
        file_ext = filename.split('.')[-1].lower()
        is_python = file_ext in ['py', 'pyx', 'pyi']
        is_javascript = file_ext in ['js', 'jsx', 'ts', 'tsx']
        is_config = file_ext in ['json', 'yaml', 'yml', 'toml', 'ini', 'cfg']
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower().strip()
            
            # Skip comments and empty lines for most checks
            if line_lower.startswith('#') or line_lower.startswith('//') or line_lower.startswith('/*') or not line_lower:
                continue
            
            # Security checks
            for pattern in self.issue_patterns["security"]:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "type": "security",
                        "severity": "high",
                        "title": f"Security Issue in {filename}",
                        "description": f"Potential security vulnerability found on line {line_num}: {line.strip()}",
                        "line": line_num,
                        "code": line.strip()
                    })
                    break
            
            # Code quality checks
            for pattern in self.issue_patterns["code_quality"]:
                if re.search(pattern, line, re.IGNORECASE):
                    severity = "medium"
                    if "TODO:" in line or "FIXME:" in line:
                        severity = "low"
                    
                    issues.append({
                        "type": "code_quality",
                        "severity": severity,
                        "title": f"Code Quality Issue in {filename}",
                        "description": f"Code quality issue found on line {line_num}: {line.strip()}",
                        "line": line_num,
                        "code": line.strip()
                    })
                    break
            
            # Performance checks
            for pattern in self.issue_patterns["performance"]:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "type": "performance",
                        "severity": "medium",
                        "title": f"Performance Issue in {filename}",
                        "description": f"Potential performance issue found on line {line_num}: {line.strip()}",
                        "line": line_num,
                        "code": line.strip()
                    })
                    break
            
            # Language-specific checks
            if is_python:
                # Python-specific checks
                if "import *" in line:
                    suggestions.append({
                        "type": "python",
                        "title": f"Consider explicit imports in {filename}",
                        "description": f"Wildcard import on line {line_num} should be replaced with explicit imports for better code clarity.",
                        "line": line_num,
                        "code": line.strip()
                    })
                
                if "print(" in line and not line.strip().startswith('#'):
                    suggestions.append({
                        "type": "python",
                        "title": f"Consider logging instead of print in {filename}",
                        "description": f"Print statement on line {line_num} should be replaced with proper logging for production code.",
                        "line": line_num,
                        "code": line.strip()
                    })
            
            elif is_javascript:
                # JavaScript-specific checks
                if "console.log(" in line and not line.strip().startswith('//'):
                    suggestions.append({
                        "type": "javascript",
                        "title": f"Consider proper logging in {filename}",
                        "description": f"Console.log statement on line {line_num} should be replaced with proper logging for production code.",
                        "line": line_num,
                        "code": line.strip()
                    })
                
                if "debugger;" in line:
                    issues.append({
                        "type": "javascript",
                        "severity": "high",
                        "title": f"Debugger statement in {filename}",
                        "description": f"Debugger statement found on line {line_num} should be removed from production code.",
                        "line": line_num,
                        "code": line.strip()
                    })
        
        # File-level analysis
        if len(lines) > 1000:
            suggestions.append({
                "type": "file_size",
                "title": f"Large file detected: {filename}",
                "description": f"File {filename} has {len(lines)} lines. Consider breaking it into smaller, more manageable files.",
                "line": None,
                "code": None
            })
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "total_lines": len(lines)
        }

    def analyze_repository_files(self, repo: Repository, max_files: int = 50) -> Dict[str, Any]:
        """Analyze multiple files in a repository."""
        all_issues = []
        all_suggestions = []
        analyzed_files = 0
        
        try:
            # Get repository contents recursively
            contents = repo.get_contents("")
            files_to_analyze = []
            
            def collect_files(contents_list):
                for content in contents_list:
                    if content.type == "dir":
                        try:
                            sub_contents = repo.get_contents(content.path)
                            collect_files(sub_contents)
                        except:
                            continue
                    elif content.type == "file":
                        # Only analyze certain file types
                        filename = content.name.lower()
                        if any(filename.endswith(ext) for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', '.cs']):
                            files_to_analyze.append(content)
            
            collect_files(contents)
            
            # Limit the number of files to analyze
            files_to_analyze = files_to_analyze[:max_files]
            
            for content in files_to_analyze:
                try:
                    # Get file content
                    file_content = content.decoded_content.decode('utf-8')
                    
                    # Analyze the file
                    analysis = self.analyze_file_content(file_content, content.name)
                    
                    all_issues.extend(analysis["issues"])
                    all_suggestions.extend(analysis["suggestions"])
                    analyzed_files += 1
                    
                except Exception as e:
                    # Skip files that can't be read or decoded
                    continue
            
            return {
                "issues": all_issues,
                "suggestions": all_suggestions,
                "analyzed_files": analyzed_files,
                "total_files_found": len(files_to_analyze)
            }
            
        except Exception as e:
            return {
                "issues": [],
                "suggestions": [],
                "analyzed_files": 0,
                "total_files_found": 0,
                "error": str(e)
            }

    def get_analysis_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the analysis results."""
        issues = analysis.get("issues", [])
        suggestions = analysis.get("suggestions", [])
        
        # Count issues by type and severity
        issue_types = {}
        issue_severities = {"high": 0, "medium": 0, "low": 0}
        
        for issue in issues:
            issue_type = issue.get("type", "unknown")
            severity = issue.get("severity", "medium")
            
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
            issue_severities[severity] = issue_severities.get(severity, 0) + 1
        
        # Count suggestions by type
        suggestion_types = {}
        for suggestion in suggestions:
            suggestion_type = suggestion.get("type", "unknown")
            suggestion_types[suggestion_type] = suggestion_types.get(suggestion_type, 0) + 1
        
        return {
            "total_issues": len(issues),
            "total_suggestions": len(suggestions),
            "issue_types": issue_types,
            "issue_severities": issue_severities,
            "suggestion_types": suggestion_types,
            "analyzed_files": analysis.get("analyzed_files", 0),
            "total_files_found": analysis.get("total_files_found", 0)
        } 