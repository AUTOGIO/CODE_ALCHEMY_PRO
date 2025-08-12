#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - File Organization Agent
Real file processing and organization implementation
"""

import sys
import shutil
import time
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import mimetypes
import hashlib

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

# Import base agent interface
try:
    from ..base.agent_interface import BaseAgent
except ImportError:
    # Fallback for direct execution
    sys.path.append(str(project_root / "src" / "agents" / "base"))
    from agent_interface import BaseAgent


from ..base.agent_interface import BaseAgent, AgentStatus

class FileOrganizationAgent(BaseAgent):
    """Real file organization agent with actual processing capabilities"""
    
    def __init__(self):
        super().__init__("File Organization Agent")
        self.processing_stats.update({
            'files_processed': 0,
            'folders_created': 0,
            'duplicates_found': 0,
            'last_activity': None
        })
        
        # Setup directories
        self.documents_dir = Path('data/documents')
        self.reports_dir = Path('data/reports')
        self.cache_dir = Path('data/cache')
        
        # Ensure directories exist
        self.documents_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
    
    def process_documents(self) -> Dict[str, Any]:
        """Process documents in the documents directory"""
        start_time = time.time()
        
        try:
            # Get all files in documents directory
            files = list(self.documents_dir.rglob('*'))
            files = [f for f in files if f.is_file()]
            
            if not files:
                return {
                    'success': True,
                    'message': 'No files to process',
                    'files_processed': 0,
                    'processing_time': time.time() - start_time
                }
            
            # Process each file
            processed_files = []
            duplicates = []
            organized_files = []
            
            for file_path in files:
                try:
                    # Analyze file
                    file_info = self._analyze_file(file_path)
                    
                    # Check for duplicates
                    if self._is_duplicate(file_path, processed_files):
                        duplicates.append(file_info)
                        self.processing_stats['duplicates_found'] += 1
                        continue
                    
                    # Organize file
                    organized_path = self._organize_file(file_path, file_info)
                    if organized_path:
                        organized_files.append({
                            'original': str(file_path),
                            'organized': str(organized_path),
                            'type': file_info['type'],
                            'size': file_info['size']
                        })
                        self.processing_stats['files_processed'] += 1
                    
                    processed_files.append(file_info)
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
            # Generate report
            report = self._generate_organization_report(organized_files, duplicates)
            
            # Update last activity
            self.processing_stats['last_activity'] = datetime.now().isoformat()
            
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'files_processed': len(organized_files),
                'duplicates_found': len(duplicates),
                'processing_time': processing_time,
                'report': report,
                'organized_files': organized_files
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a file and extract metadata"""
        stat = file_path.stat()
        
        # Get file type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        file_type = mime_type.split('/')[0] if mime_type else 'unknown'
        
        # Calculate hash for duplicate detection
        file_hash = self._calculate_file_hash(file_path)
        
        return {
            'name': file_path.name,
            'path': str(file_path),
            'size': stat.st_size,
            'type': file_type,
            'extension': file_path.suffix.lower(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'hash': file_hash
        }
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _is_duplicate(self, file_path: Path, processed_files: List[Dict[str, Any]]) -> bool:
        """Check if file is a duplicate"""
        current_hash = self._calculate_file_hash(file_path)
        
        for processed_file in processed_files:
            if processed_file['hash'] == current_hash:
                return True
        
        return False
    
    def _organize_file(self, file_path: Path, file_info: Dict[str, Any]) -> Path:
        """Organize file into appropriate category"""
        try:
            # Determine category based on file type
            category = self._determine_category(file_info)
            
            # Create category directory
            category_dir = self.documents_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Move file to category
            new_path = category_dir / file_path.name
            
            # Handle filename conflicts
            counter = 1
            original_name = new_path.stem
            original_suffix = new_path.suffix
            
            while new_path.exists():
                new_path = category_dir / f"{original_name}_{counter}{original_suffix}"
                counter += 1
            
            # Move the file
            shutil.move(str(file_path), str(new_path))
            
            return new_path
            
        except Exception as e:
            print(f"Error organizing {file_path}: {e}")
            return None
    
    def _determine_category(self, file_info: Dict[str, Any]) -> str:
        """Determine the appropriate category for a file"""
        file_type = file_info['type']
        extension = file_info['extension']
        
        # Define categories
        categories = {
            'image': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
            'video': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'],
            'audio': ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'],
            'document': ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt'],
            'spreadsheet': ['xls', 'xlsx', 'csv', 'ods'],
            'presentation': ['ppt', 'pptx', 'odp'],
            'archive': ['zip', 'rar', '7z', 'tar', 'gz'],
            'code': ['py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'php', 'rb', 'go', 'rs'],
            'data': ['json', 'xml', 'yaml', 'yml', 'sql', 'db', 'sqlite']
        }
        
        # Check by extension first
        for category, extensions in categories.items():
            if extension in extensions:
                return category
        
        # Fallback to MIME type
        if file_type in ['image', 'video', 'audio']:
            return file_type
        elif file_type == 'text':
            return 'document'
        else:
            return 'other'
    
    def _generate_organization_report(self, organized_files: List[Dict[str, Any]], 
                                   duplicates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a detailed organization report"""
        
        # Calculate statistics
        total_size = sum(f['size'] for f in organized_files)
        type_distribution = {}
        
        for file_info in organized_files:
            file_type = file_info['type']
            type_distribution[file_type] = type_distribution.get(file_type, 0) + 1
        
        # Create report
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'files_organized': len(organized_files),
                'duplicates_found': len(duplicates),
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            },
            'type_distribution': type_distribution,
            'organized_files': organized_files,
            'duplicates': duplicates
        }
        
        # Save report
        report_file = self.reports_dir / f"file_organization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        status = super().get_health_metrics()
        status.update({
            'files_processed': self.processing_stats['files_processed'],
            'duplicates_found': self.processing_stats['duplicates_found'],
            'documents_dir': str(self.documents_dir),
            'reports_dir': str(self.reports_dir)
        })
        return status
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and supported operations"""
        return {
            'name': self.agent_name,
            'capabilities': [
                'file_organization',
                'duplicate_detection',
                'file_categorization',
                'batch_processing',
                'report_generation'
            ],
            'supported_file_types': [
                'document', 'image', 'video', 'audio', 'code',
                'data', 'spreadsheet', 'presentation', 'archive'
            ],
            'operations': [
                'process_documents',
                'organize_files',
                'detect_duplicates',
                'generate_reports',
                'add_test_files'
            ]
        }
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        operation = parameters.get('operation', 'process_documents')
        
        if operation == 'process_documents':
            return self.process_documents()
        elif operation == 'add_test_files':
            return self.add_test_files()
        elif operation == 'organize_files':
            return self.process_documents()
        else:
            return {
                'success': False,
                'error': f'Unknown operation: {operation}',
                'supported_operations': ['process_documents', 'add_test_files', 'organize_files']
            }
    
    def add_test_files(self) -> Dict[str, Any]:
        """Add some test files for demonstration"""
        test_files = [
            ('test_document.pdf', 'document'),
            ('sample_image.jpg', 'image'),
            ('video_sample.mp4', 'video'),
            ('audio_file.mp3', 'audio'),
            ('code_script.py', 'code'),
            ('data_file.json', 'data'),
            ('presentation.pptx', 'presentation'),
            ('spreadsheet.xlsx', 'spreadsheet'),
            ('archive.zip', 'archive')
        ]
        
        created_files = []
        
        for filename, category in test_files:
            file_path = self.documents_dir / filename
            
            # Create a simple test file
            with open(file_path, 'w') as f:
                f.write(f"This is a test {category} file created at {datetime.now().isoformat()}")
            
            created_files.append(str(file_path))
        
        return {
            'success': True,
            'files_created': len(created_files),
            'files': created_files
        }


# Agent factory function
def create_file_organization_agent() -> FileOrganizationAgent:
    """Create and return a file organization agent"""
    return FileOrganizationAgent() 