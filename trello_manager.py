"""
Trello Task Manager

This module handles Trello API interactions for creating and managing tasks.
"""

import os
import re
from typing import Dict, List, Optional, Any
from trello import TrelloClient
from trello.exceptions import ResourceUnavailable


class TrelloManager:
    def __init__(self, api_key: str, token: str, board_id: str):
        """Initialize Trello manager with API credentials."""
        self.client = TrelloClient(api_key=api_key, token=token)
        self.board_id = self._extract_board_id(board_id)
        
        try:
            self.board = self.client.get_board(self.board_id)
        except ResourceUnavailable as e:
            print(f"Warning: Could not access Trello board: {e}")
            self.board = None
        
        # Cache for lists and labels
        self._lists_cache = None
        self._labels_cache = None

    def _extract_board_id(self, board_id: str) -> str:
        """Extract board ID from various formats."""
        # If it's a full URL, extract the ID
        if board_id.startswith('http'):
            # Extract ID from URL like https://trello.com/b/Diz3GQos/mcp-practice
            match = re.search(r'/b/([a-zA-Z0-9]+)', board_id)
            if match:
                return match.group(1)
        
        # If it's already just the ID, return as is
        return board_id

    def get_lists(self) -> List[Dict[str, Any]]:
        """Get all lists from the board."""
        if self._lists_cache is None:
            try:
                if not self.board:
                    return []
                lists = self.board.list_lists()
                self._lists_cache = [
                    {
                        "id": lst.id,
                        "name": lst.name,
                        "closed": lst.closed
                    }
                    for lst in lists
                ]
            except ResourceUnavailable:
                self._lists_cache = []
        return self._lists_cache

    def get_labels(self) -> List[Dict[str, Any]]:
        """Get all labels from the board."""
        if self._labels_cache is None:
            try:
                if not self.board:
                    return []
                labels = self.board.get_labels()
                self._labels_cache = [
                    {
                        "id": label.id,
                        "name": label.name,
                        "color": label.color
                    }
                    for label in labels
                ]
            except ResourceUnavailable:
                self._labels_cache = []
        return self._labels_cache

    def create_label(self, name: str, color: str = "blue") -> Optional[str]:
        """Create a new label on the board."""
        try:
            if not self.board:
                return None
            label = self.board.add_label(name, color)
            # Refresh labels cache
            self._labels_cache = None
            return label.id
        except ResourceUnavailable:
            return None

    def get_or_create_label(self, name: str, color: str = "blue") -> Optional[str]:
        """Get existing label or create a new one."""
        labels = self.get_labels()
        
        # Check if label already exists
        for label in labels:
            if label["name"].lower() == name.lower():
                return label["id"]
        
        # Create new label
        return self.create_label(name, color)

    def get_list_by_name(self, list_name: str) -> Optional[str]:
        """Get list ID by name."""
        lists = self.get_lists()
        for lst in lists:
            if lst["name"].lower() == list_name.lower():
                return lst["id"]
        return None

    def create_card(self, 
                   title: str, 
                   description: str = "", 
                   list_name: str = "To Do",
                   labels: List[str] = None,
                   due_date: str = None) -> Optional[Dict[str, Any]]:
        """Create a new card in the specified list."""
        try:
            if not self.board:
                print("Warning: Trello board not accessible")
                return None
                
            # Get list
            list_id = self.get_list_by_name(list_name)
            if not list_id:
                # Use first available list
                lists = self.get_lists()
                if not lists:
                    return None
                list_id = lists[0]["id"]
            
            # Get list object
            trello_list = self.client.get_list(list_id)
            
            # Create card
            card = trello_list.add_card(name=title, desc=description, due=due_date)
            
            # Add labels
            if labels:
                label_ids = []
                for label_name in labels:
                    label_id = self.get_or_create_label(label_name)
                    if label_id:
                        label_ids.append(label_id)
                
                if label_ids:
                    card.add_labels(label_ids)
            
            return {
                "id": card.id,
                "name": card.name,
                "description": card.description,
                "url": card.url,
                "list_name": list_name,
                "labels": labels or []
            }
            
        except ResourceUnavailable as e:
            print(f"Error creating Trello card: {e}")
            return None

    def create_issue_cards(self, issues: List[Dict[str, Any]], repo_name: str) -> List[Dict[str, Any]]:
        """Create Trello cards for GitHub issues."""
        created_cards = []
        
        for issue in issues:
            # Determine list based on issue type
            list_name = "To Do"
            if "bug" in [label.lower() for label in issue.get("labels", [])]:
                list_name = "Bugs"
            elif "enhancement" in [label.lower() for label in issue.get("labels", [])]:
                list_name = "Enhancements"
            
            # Create labels
            labels = [repo_name] + issue.get("labels", [])
            
            # Create description
            description = f"""
**GitHub Issue #{issue['number']}**

{issue.get('body', 'No description provided')}

**Created by:** {issue.get('user', 'Unknown')}
**Created:** {issue.get('created_at', 'Unknown')}
**Labels:** {', '.join(issue.get('labels', []))}

[View on GitHub](https://github.com/{repo_name}/issues/{issue['number']})
            """.strip()
            
            # Create card
            card = self.create_card(
                title=f"Issue #{issue['number']}: {issue['title']}",
                description=description,
                list_name=list_name,
                labels=labels
            )
            
            if card:
                created_cards.append(card)
        
        return created_cards

    def create_analysis_cards(self, analysis: Dict[str, Any], repo_name: str) -> List[Dict[str, Any]]:
        """Create Trello cards for code analysis issues."""
        created_cards = []
        
        # Create cards for issues
        for issue in analysis.get("issues", []):
            # Determine list based on severity
            list_name = "To Do"
            if issue.get("severity") == "high":
                list_name = "High Priority"
            elif issue.get("severity") == "critical":
                list_name = "Critical"
            
            # Create labels
            labels = [repo_name, issue.get("type", "analysis"), issue.get("severity", "medium")]
            
            # Create description
            description = f"""
**Code Analysis Issue**

**Type:** {issue.get('type', 'Unknown')}
**Severity:** {issue.get('severity', 'Medium')}

{issue.get('description', 'No description provided')}

**Repository:** {repo_name}
**Analysis Score:** {analysis.get('score', 'N/A')}/100
            """.strip()
            
            # Create card
            card = self.create_card(
                title=issue.get("title", "Code Analysis Issue"),
                description=description,
                list_name=list_name,
                labels=labels
            )
            
            if card:
                created_cards.append(card)
        
        # Create cards for suggestions
        for suggestion in analysis.get("suggestions", []):
            labels = [repo_name, "suggestion", suggestion.get("type", "improvement")]
            
            description = f"""
**Code Analysis Suggestion**

**Type:** {suggestion.get('type', 'Unknown')}

{suggestion.get('description', 'No description provided')}

**Repository:** {repo_name}
**Analysis Score:** {analysis.get('score', 'N/A')}/100
            """.strip()
            
            card = self.create_card(
                title=suggestion.get("title", "Code Analysis Suggestion"),
                description=description,
                list_name="Suggestions",
                labels=labels
            )
            
            if card:
                created_cards.append(card)
        
        return created_cards

    def create_summary_card(self, repo_info: Dict[str, Any], analysis: Dict[str, Any], 
                          total_cards_created: int) -> Optional[Dict[str, Any]]:
        """Create a summary card with repository analysis results."""
        score = analysis.get("score", 0)
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        
        description = f"""
**Repository Analysis Summary**

**Repository:** {repo_info.get('full_name', 'Unknown')}
**Language:** {repo_info.get('language', 'Unknown')}
**Stars:** {repo_info.get('stars', 0)}
**Forks:** {repo_info.get('forks', 0)}
**Open Issues:** {repo_info.get('open_issues', 0)}

**Analysis Results:**
- **Quality Score:** {score}/100
- **Issues Found:** {len(analysis.get('issues', []))}
- **Suggestions:** {len(analysis.get('suggestions', []))}
- **Trello Cards Created:** {total_cards_created}

**Repository URL:** {repo_info.get('url', 'N/A')}
        """.strip()
        
        labels = [repo_info.get('full_name', 'repo'), "summary", score_color]
        
        return self.create_card(
            title=f"Analysis Summary: {repo_info.get('name', 'Repository')}",
            description=description,
            list_name="Summary",
            labels=labels
        ) 