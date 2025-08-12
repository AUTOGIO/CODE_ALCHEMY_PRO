#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - GitHub Integration
Repository management and code synchronization
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.core.config import config


class GitHubIntegration:
    """GitHub API integration for repository management"""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME", "AUTOGIO")
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.token else {}
        
        # Check if GitHub is configured
        self.is_configured = bool(self.token)
    
    def test_connection(self) -> Dict[str, Any]:
        """Test GitHub API connection"""
        try:
            response = requests.get(f"{self.api_base}/user", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "success": True,
                    "username": user_data.get("login"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "repos_count": user_data.get("public_repos", 0)
                }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid GitHub token",
                    "status_code": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code}",
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "configured": self.is_configured
            }
    
    def list_repositories(self) -> Dict[str, Any]:
        """List user repositories"""
        try:
            response = requests.get(f"{self.api_base}/user/repos", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                repos = response.json()
                return {
                    "success": True,
                    "repositories": [
                        {
                            "name": repo["name"],
                            "full_name": repo["full_name"],
                            "description": repo["description"],
                            "language": repo["language"],
                            "stars": repo["stargazers_count"],
                            "forks": repo["forks_count"],
                            "updated": repo["updated_at"],
                            "url": repo["html_url"]
                        }
                        for repo in repos
                    ],
                    "count": len(repos)
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to fetch repositories: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_repository_info(self, repo_name: str) -> Dict[str, Any]:
        """Get detailed information about a repository"""
        try:
            full_name = f"{self.username}/{repo_name}" if "/" not in repo_name else repo_name
            
            response = requests.get(f"{self.api_base}/repos/{full_name}", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                repo_data = response.json()
                return {
                    "success": True,
                    "repository": {
                        "name": repo_data["name"],
                        "full_name": repo_data["full_name"],
                        "description": repo_data["description"],
                        "language": repo_data["language"],
                        "stars": repo_data["stargazers_count"],
                        "forks": repo_data["forks_count"],
                        "size": repo_data["size"],
                        "default_branch": repo_data["default_branch"],
                        "created": repo_data["created_at"],
                        "updated": repo_data["updated_at"],
                        "url": repo_data["html_url"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Repository not found: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_file_content(self, repo_name: str, file_path: str, branch: str = "main") -> Dict[str, Any]:
        """Get content of a file from repository"""
        try:
            full_name = f"{self.username}/{repo_name}" if "/" not in repo_name else repo_name
            
            response = requests.get(
                f"{self.api_base}/repos/{full_name}/contents/{file_path}",
                headers=self.headers,
                params={"ref": branch},
                timeout=10
            )
            
            if response.status_code == 200:
                file_data = response.json()
                
                # Decode content if it's base64 encoded
                content = file_data["content"]
                if file_data.get("encoding") == "base64":
                    content = base64.b64decode(content).decode("utf-8")
                
                return {
                    "success": True,
                    "file": {
                        "name": file_data["name"],
                        "path": file_data["path"],
                        "size": file_data["size"],
                        "content": content,
                        "sha": file_data["sha"],
                        "url": file_data["html_url"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"File not found: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_issue(self, repo_name: str, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        """Create a new issue in repository"""
        try:
            full_name = f"{self.username}/{repo_name}" if "/" not in repo_name else repo_name
            
            payload = {
                "title": title,
                "body": body
            }
            
            if labels:
                payload["labels"] = labels
            
            response = requests.post(
                f"{self.api_base}/repos/{full_name}/issues",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                return {
                    "success": True,
                    "issue": {
                        "number": issue_data["number"],
                        "title": issue_data["title"],
                        "body": issue_data["body"],
                        "state": issue_data["state"],
                        "url": issue_data["html_url"],
                        "created": issue_data["created_at"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create issue: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_recent_commits(self, repo_name: str, branch: str = "main", limit: int = 10) -> Dict[str, Any]:
        """Get recent commits from repository"""
        try:
            full_name = f"{self.username}/{repo_name}" if "/" not in repo_name else repo_name
            
            response = requests.get(
                f"{self.api_base}/repos/{full_name}/commits",
                headers=self.headers,
                params={"sha": branch, "per_page": limit},
                timeout=10
            )
            
            if response.status_code == 200:
                commits = response.json()
                return {
                    "success": True,
                    "commits": [
                        {
                            "sha": commit["sha"][:7],
                            "message": commit["commit"]["message"],
                            "author": commit["commit"]["author"]["name"],
                            "date": commit["commit"]["author"]["date"],
                            "url": commit["html_url"]
                        }
                        for commit in commits
                    ],
                    "count": len(commits)
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to fetch commits: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get GitHub integration status summary"""
        connection_test = self.test_connection()
        
        if connection_test["success"]:
            repos = self.list_repositories()
            return {
                "configured": True,
                "connected": True,
                "username": connection_test.get("username"),
                "repositories_count": repos.get("count", 0) if repos["success"] else 0,
                "last_check": datetime.now().isoformat()
            }
        else:
            return {
                "configured": self.is_configured,
                "connected": False,
                "error": connection_test.get("error"),
                "last_check": datetime.now().isoformat()
            }


# Integration factory function
def create_github_integration() -> GitHubIntegration:
    """Create and return a GitHub integration instance"""
    return GitHubIntegration() 