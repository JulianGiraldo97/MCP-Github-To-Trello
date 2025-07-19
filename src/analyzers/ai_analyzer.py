"""
AI-Powered Code Analyzer

This module uses generative AI to analyze code quality, security, and provide intelligent suggestions.
"""

import os
import json
import base64
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import openai
import anthropic
from github import Repository, GithubException


@dataclass
class AIAnalysisResult:
    """Result of AI analysis."""
    issues: List[Dict[str, Any]]
    suggestions: List[Dict[str, Any]]
    code_quality_score: int
    security_score: int
    maintainability_score: int
    detailed_analysis: str


class AIAnalyzer:
    """AI-powered code analyzer using OpenAI and Anthropic."""
    
    def __init__(self, openai_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        """Initialize AI analyzer with API keys."""
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize OpenAI
        if openai_api_key:
            openai.api_key = openai_api_key
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        # Initialize Anthropic
        if anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
    
    def analyze_repository_with_ai(self, repo: Repository, sample_files: List[Dict[str, Any]]) -> AIAnalysisResult:
        """Analyze repository using AI for intelligent code analysis."""
        
        # Prepare code samples for analysis
        code_samples = self._prepare_code_samples(repo, sample_files)
        
        # Analyze with AI
        analysis = self._perform_ai_analysis(code_samples, repo.name)
        
        return analysis
    
    def _prepare_code_samples(self, repo: Repository, sample_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare code samples for AI analysis."""
        samples = []
        
        for file_info in sample_files[:10]:  # Limit to 10 files for cost efficiency
            try:
                content = repo.get_contents(file_info['path'])
                if hasattr(content, 'content'):
                    code = base64.b64decode(content.content).decode('utf-8')
                    samples.append({
                        'path': file_info['path'],
                        'language': file_info.get('language', 'unknown'),
                        'code': code[:2000],  # Limit code size
                        'size': len(code)
                    })
            except GithubException:
                continue
        
        return samples
    
    def _perform_ai_analysis(self, code_samples: List[Dict[str, Any]], repo_name: str) -> AIAnalysisResult:
        """Perform AI analysis on code samples."""
        
        # Create analysis prompt
        prompt = self._create_analysis_prompt(code_samples, repo_name)
        
        # Try OpenAI first, then Anthropic as fallback
        if self.openai_client:
            try:
                return self._analyze_with_openai(prompt)
            except Exception as e:
                print(f"OpenAI analysis failed: {e}")
        
        if self.anthropic_client:
            try:
                return self._analyze_with_anthropic(prompt)
            except Exception as e:
                print(f"Anthropic analysis failed: {e}")
        
        # Fallback to basic analysis
        return self._fallback_analysis(code_samples)
    
    def _create_analysis_prompt(self, code_samples: List[Dict[str, Any]], repo_name: str) -> str:
        """Create a comprehensive analysis prompt for AI."""
        
        code_text = ""
        for sample in code_samples:
            code_text += f"\n--- File: {sample['path']} ({sample['language']}) ---\n"
            code_text += sample['code'][:1000] + "\n"
        
        prompt = f"""
You are an expert software engineer and code reviewer. Analyze the following code samples from repository "{repo_name}" and provide a comprehensive analysis.

Code samples:
{code_text}

Please provide a detailed analysis in JSON format with the following structure:
{{
    "issues": [
        {{
            "type": "security|performance|maintainability|code_quality",
            "severity": "low|medium|high|critical",
            "title": "Brief issue title",
            "description": "Detailed description of the issue",
            "file": "path/to/file",
            "line": "approximate line number if applicable",
            "suggestion": "How to fix this issue"
        }}
    ],
    "suggestions": [
        {{
            "type": "improvement|refactoring|optimization",
            "title": "Brief suggestion title",
            "description": "Detailed description of the suggestion",
            "priority": "low|medium|high",
            "impact": "Brief description of the impact"
        }}
    ],
    "scores": {{
        "code_quality": 0-100,
        "security": 0-100,
        "maintainability": 0-100
    }},
    "detailed_analysis": "Comprehensive analysis summary in markdown format"
}}

Focus on:
1. Security vulnerabilities (SQL injection, XSS, hardcoded secrets, etc.)
2. Performance issues (inefficient algorithms, memory leaks, etc.)
3. Code quality (readability, maintainability, best practices)
4. Architecture and design patterns
5. Testing coverage and quality
6. Documentation quality
7. Modern language features and improvements

Be specific and actionable in your recommendations.
"""
        
        return prompt
    
    def _analyze_with_openai(self, prompt: str) -> AIAnalysisResult:
        """Analyze code using OpenAI GPT-4."""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer and software engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        
        # Try to parse JSON response
        try:
            # Extract JSON from response (in case there's extra text)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            analysis_data = json.loads(json_str)
            
            return AIAnalysisResult(
                issues=analysis_data.get('issues', []),
                suggestions=analysis_data.get('suggestions', []),
                code_quality_score=analysis_data.get('scores', {}).get('code_quality', 70),
                security_score=analysis_data.get('scores', {}).get('security', 70),
                maintainability_score=analysis_data.get('scores', {}).get('maintainability', 70),
                detailed_analysis=analysis_data.get('detailed_analysis', 'AI analysis completed.')
            )
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return self._fallback_analysis([])
    
    def _analyze_with_anthropic(self, prompt: str) -> AIAnalysisResult:
        """Analyze code using Anthropic Claude."""
        
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.content[0].text
        
        # Try to parse JSON response
        try:
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            analysis_data = json.loads(json_str)
            
            return AIAnalysisResult(
                issues=analysis_data.get('issues', []),
                suggestions=analysis_data.get('suggestions', []),
                code_quality_score=analysis_data.get('scores', {}).get('code_quality', 70),
                security_score=analysis_data.get('scores', {}).get('security', 70),
                maintainability_score=analysis_data.get('scores', {}).get('maintainability', 70),
                detailed_analysis=analysis_data.get('detailed_analysis', 'AI analysis completed.')
            )
            
        except json.JSONDecodeError:
            return self._fallback_analysis([])
    
    def _fallback_analysis(self, code_samples: List[Dict[str, Any]]) -> AIAnalysisResult:
        """Fallback analysis when AI is not available."""
        
        return AIAnalysisResult(
            issues=[
                {
                    "type": "ai_unavailable",
                    "severity": "medium",
                    "title": "AI Analysis Unavailable",
                    "description": "AI-powered analysis could not be performed. Check API keys and try again.",
                    "file": "N/A",
                    "line": "N/A",
                    "suggestion": "Ensure OpenAI or Anthropic API keys are properly configured."
                }
            ],
            suggestions=[
                {
                    "type": "improvement",
                    "title": "Enable AI Analysis",
                    "description": "Configure AI API keys to get more detailed code analysis.",
                    "priority": "medium",
                    "impact": "Better code quality insights and security analysis."
                }
            ],
            code_quality_score=70,
            security_score=70,
            maintainability_score=70,
            detailed_analysis="AI analysis was not available. Using basic analysis instead."
        )
    
    def analyze_specific_file(self, repo: Repository, file_path: str) -> Dict[str, Any]:
        """Analyze a specific file with AI."""
        
        try:
            content = repo.get_contents(file_path)
            if hasattr(content, 'content'):
                code = base64.b64decode(content.content).decode('utf-8')
                
                prompt = f"""
Analyze this specific file: {file_path}

Code:
{code[:3000]}

Provide a detailed analysis focusing on:
1. Code quality and readability
2. Potential bugs or issues
3. Security concerns
4. Performance optimizations
5. Best practices and improvements

Format your response as JSON:
{{
    "issues": [...],
    "suggestions": [...],
    "overall_score": 0-100,
    "summary": "Brief summary"
}}
"""
                
                if self.openai_client:
                    return self._analyze_with_openai(prompt)
                elif self.anthropic_client:
                    return self._analyze_with_anthropic(prompt)
                    
        except GithubException:
            pass
        
        return {"error": "Could not analyze file"} 