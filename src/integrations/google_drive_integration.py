#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Google Drive Integration
Cloud synchronization and file management
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


class GoogleDriveIntegration:
    """Google Drive API integration for cloud synchronization"""
    
    def __init__(self):
        self.enabled = os.getenv("GOOGLE_DRIVE_ENABLED", "false").lower() == "true"
        self.credentials_file = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "credentials.json")
        self.sync_folders = os.getenv("GOOGLE_DRIVE_SYNC_FOLDERS", "").split(",")
        
        # API configuration
        self.api_base = "https://www.googleapis.com/drive/v3"
        self.upload_api = "https://www.googleapis.com/upload/drive/v3"
        
        # Check if Google Drive is configured
        self.is_configured = self.enabled and Path(self.credentials_file).exists()
        
        # OAuth2 token (would be obtained through OAuth flow)
        self.access_token = os.getenv("GOOGLE_DRIVE_ACCESS_TOKEN")
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        } if self.access_token else {}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Google Drive API connection"""
        if not self.is_configured:
            return {
                "success": False,
                "error": "Google Drive not configured",
                "configured": False,
                "enabled": self.enabled,
                "credentials_file": self.credentials_file
            }
        
        try:
            # Test API access by getting user info
            response = requests.get(
                f"{self.api_base}/about",
                headers=self.headers,
                params={"fields": "user"},
                timeout=10
            )
            
            if response.status_code == 200:
                about_data = response.json()
                user_info = about_data.get("user", {})
                
                return {
                    "success": True,
                    "connected": True,
                    "user_email": user_info.get("emailAddress"),
                    "user_name": user_info.get("displayName"),
                    "quota_used": about_data.get("storageQuota", {}).get("usage"),
                    "quota_total": about_data.get("storageQuota", {}).get("limit"),
                    "configured": True
                }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid access token",
                    "configured": True,
                    "connected": False
                }
            else:
                return {
                    "success": False,
                    "error": f"Google Drive API error: {response.status_code}",
                    "configured": True,
                    "connected": False
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "configured": self.is_configured,
                "connected": False
            }
    
    def list_files(self, folder_id: str = "root", page_size: int = 50) -> Dict[str, Any]:
        """List files in Google Drive"""
        if not self.is_configured:
            return {
                "success": False,
                "error": "Google Drive not configured"
            }
        
        try:
            params = {
                "q": f"'{folder_id}' in parents and trashed=false",
                "pageSize": page_size,
                "fields": "files(id,name,mimeType,size,modifiedTime,parents,webViewLink)"
            }
            
            response = requests.get(f"{self.api_base}/files", headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                files = data.get("files", [])
                
                return {
                    "success": True,
                    "files": [
                        {
                            "id": file["id"],
                            "name": file["name"],
                            "type": file["mimeType"],
                            "size": file.get("size", 0),
                            "modified": file["modifiedTime"],
                            "url": file["webViewLink"]
                        }
                        for file in files
                    ],
                    "count": len(files)
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to list files: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def upload_file(self, file_path: str, folder_id: str = "root") -> Dict[str, Any]:
        """Upload a file to Google Drive"""
        if not self.is_configured:
            return {
                "success": False,
                "error": "Google Drive not configured"
            }
        
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }
            
            # Prepare metadata
            metadata = {
                "name": file_path_obj.name,
                "parents": [folder_id]
            }
            
            # Upload file
            with open(file_path, "rb") as f:
                files = {"file": f}
                data = {"metadata": json.dumps(metadata)}
                
                response = requests.post(
                    f"{self.upload_api}/files?uploadType=multipart",
                    headers=self.headers,
                    data=data,
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                file_data = response.json()
                return {
                    "success": True,
                    "file": {
                        "id": file_data["id"],
                        "name": file_data["name"],
                        "size": file_data.get("size", 0),
                        "url": file_data["webViewLink"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Upload failed: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def download_file(self, file_id: str, local_path: str) -> Dict[str, Any]:
        """Download a file from Google Drive"""
        if not self.is_configured:
            return {
                "success": False,
                "error": "Google Drive not configured"
            }
        
        try:
            # Get file metadata first
            response = requests.get(f"{self.api_base}/files/{file_id}", headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"File not found: {response.status_code}"
                }
            
            file_data = response.json()
            
            # Download file content
            download_response = requests.get(
                f"{self.api_base}/files/{file_id}?alt=media",
                headers=self.headers,
                timeout=30
            )
            
            if download_response.status_code == 200:
                # Save file
                Path(local_path).parent.mkdir(parents=True, exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(download_response.content)
                
                return {
                    "success": True,
                    "file": {
                        "id": file_data["id"],
                        "name": file_data["name"],
                        "size": file_data.get("size", 0),
                        "local_path": local_path
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Download failed: {download_response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_folder(self, folder_name: str, parent_id: str = "root") -> Dict[str, Any]:
        """Create a new folder in Google Drive"""
        if not self.is_configured:
            return {
                "success": False,
                "error": "Google Drive not configured"
            }
        
        try:
            metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id]
            }
            
            response = requests.post(
                f"{self.api_base}/files",
                headers=self.headers,
                json=metadata,
                timeout=10
            )
            
            if response.status_code == 200:
                folder_data = response.json()
                return {
                    "success": True,
                    "folder": {
                        "id": folder_data["id"],
                        "name": folder_data["name"],
                        "url": folder_data["webViewLink"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create folder: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def sync_folder(self, local_folder: str, drive_folder_id: str = "root") -> Dict[str, Any]:
        """Sync a local folder with Google Drive"""
        if not self.is_configured:
            return {
                "success": False,
                "error": "Google Drive not configured"
            }
        
        try:
            local_path = Path(local_folder)
            if not local_path.exists():
                return {
                    "success": False,
                    "error": f"Local folder not found: {local_folder}"
                }
            
            # Get existing files in Drive folder
            drive_files = self.list_files(drive_folder_id)
            if not drive_files["success"]:
                return drive_files
            
            existing_files = {f["name"]: f["id"] for f in drive_files["files"]}
            
            # Upload new/modified files
            uploaded_files = []
            for file_path in local_path.rglob("*"):
                if file_path.is_file():
                    file_name = file_path.name
                    
                    # Check if file exists in Drive
                    if file_name in existing_files:
                        # File exists, check if modified
                        # For simplicity, we'll upload anyway
                        pass
                    
                    # Upload file
                    upload_result = self.upload_file(str(file_path), drive_folder_id)
                    if upload_result["success"]:
                        uploaded_files.append(upload_result["file"])
            
            return {
                "success": True,
                "uploaded_files": uploaded_files,
                "count": len(uploaded_files)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get Google Drive integration status summary"""
        connection_test = self.test_connection()
        
        if connection_test["success"]:
            return {
                "configured": True,
                "connected": True,
                "enabled": self.enabled,
                "user_email": connection_test.get("user_email"),
                "quota_used": connection_test.get("quota_used"),
                "quota_total": connection_test.get("quota_total"),
                "sync_folders": self.sync_folders,
                "last_check": datetime.now().isoformat()
            }
        else:
            return {
                "configured": self.is_configured,
                "connected": False,
                "enabled": self.enabled,
                "error": connection_test.get("error"),
                "sync_folders": self.sync_folders,
                "last_check": datetime.now().isoformat()
            }


# Integration factory function
def create_google_drive_integration() -> GoogleDriveIntegration:
    """Create and return a Google Drive integration instance"""
    return GoogleDriveIntegration() 