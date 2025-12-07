#!/usr/bin/env python3
"""
Document Evolution System
A system that tracks and evolves documents as systems evolve.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class DocumentVersion:
    """Represents a single version of a document."""
    
    def __init__(self, content: str, version: int, metadata: Optional[Dict[str, Any]] = None):
        self.content = content
        self.version = version
        self.timestamp = datetime.now().isoformat()
        self.hash = self._compute_hash(content)
        self.metadata = metadata or {}
    
    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of document content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert version to dictionary."""
        return {
            'version': self.version,
            'timestamp': self.timestamp,
            'hash': self.hash,
            'metadata': self.metadata,
            'content': self.content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentVersion':
        """Create version from dictionary."""
        version = cls(
            content=data['content'],
            version=data['version'],
            metadata=data.get('metadata', {})
        )
        version.timestamp = data['timestamp']
        version.hash = data['hash']
        return version


class Document:
    """Represents a document with version history."""
    
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.versions: List[DocumentVersion] = []
        self.current_version = 0
    
    def add_version(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> DocumentVersion:
        """Add a new version of the document."""
        self.current_version += 1
        version = DocumentVersion(content, self.current_version, metadata)
        self.versions.append(version)
        return version
    
    def get_version(self, version_number: int) -> Optional[DocumentVersion]:
        """Get a specific version of the document."""
        for version in self.versions:
            if version.version == version_number:
                return version
        return None
    
    def get_latest_version(self) -> Optional[DocumentVersion]:
        """Get the latest version of the document."""
        return self.versions[-1] if self.versions else None
    
    def has_changed(self, new_content: str) -> bool:
        """Check if content has changed from latest version."""
        latest = self.get_latest_version()
        if not latest:
            return True
        new_hash = hashlib.sha256(new_content.encode('utf-8')).hexdigest()
        return new_hash != latest.hash
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            'name': self.name,
            'path': self.path,
            'current_version': self.current_version,
            'versions': [v.to_dict() for v in self.versions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        """Create document from dictionary."""
        doc = cls(data['name'], data['path'])
        doc.current_version = data['current_version']
        doc.versions = [DocumentVersion.from_dict(v) for v in data['versions']]
        return doc


class DocumentEvolutionSystem:
    """Main system for managing document evolution."""
    
    def __init__(self, root_path: str = '.'):
        self.root_path = Path(root_path)
        self.evolution_dir = self.root_path / '.doc_evolve'
        self.documents: Dict[str, Document] = {}
        self._ensure_evolution_dir()
        self._load_state()
    
    def _ensure_evolution_dir(self):
        """Ensure the evolution directory exists."""
        self.evolution_dir.mkdir(exist_ok=True)
    
    def _state_file(self) -> Path:
        """Get the state file path."""
        return self.evolution_dir / 'state.json'
    
    def _load_state(self):
        """Load system state from disk."""
        state_file = self._state_file()
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.documents = {
                    name: Document.from_dict(doc_data)
                    for name, doc_data in data.get('documents', {}).items()
                }
    
    def _save_state(self):
        """Save system state to disk."""
        state_file = self._state_file()
        data = {
            'documents': {
                name: doc.to_dict()
                for name, doc in self.documents.items()
            }
        }
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def track_document(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> Document:
        """Start tracking a document."""
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            doc_name = str(path.relative_to(self.root_path.resolve()))
        except ValueError:
            # If path is not under root_path, use absolute path
            doc_name = str(path)
        
        if doc_name not in self.documents:
            self.documents[doc_name] = Document(doc_name, str(path))
        
        doc = self.documents[doc_name]
        
        # Only add version if content has changed
        if doc.has_changed(content):
            doc.add_version(content, metadata)
            self._save_state()
        
        return doc
    
    def update_document(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> Optional[DocumentVersion]:
        """Update a tracked document with new content."""
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            doc_name = str(path.relative_to(self.root_path.resolve()))
        except ValueError:
            # If path is not under root_path, use absolute path
            doc_name = str(path)
        
        if doc_name not in self.documents:
            # Track it first
            return self.track_document(file_path, metadata).get_latest_version()
        
        doc = self.documents[doc_name]
        
        if doc.has_changed(content):
            version = doc.add_version(content, metadata)
            self._save_state()
            return version
        
        return None
    
    def get_document(self, doc_name: str) -> Optional[Document]:
        """Get a tracked document by name."""
        return self.documents.get(doc_name)
    
    def list_documents(self) -> List[str]:
        """List all tracked documents."""
        return list(self.documents.keys())
    
    def get_document_history(self, doc_name: str) -> List[Dict[str, Any]]:
        """Get version history for a document."""
        doc = self.get_document(doc_name)
        if not doc:
            return []
        
        return [
            {
                'version': v.version,
                'timestamp': v.timestamp,
                'hash': v.hash,
                'metadata': v.metadata
            }
            for v in doc.versions
        ]
    
    def restore_version(self, doc_name: str, version_number: int, output_path: Optional[str] = None):
        """Restore a specific version of a document."""
        doc = self.get_document(doc_name)
        if not doc:
            raise ValueError(f"Document not found: {doc_name}")
        
        version = doc.get_version(version_number)
        if not version:
            raise ValueError(f"Version {version_number} not found for {doc_name}")
        
        target_path = output_path or doc.path
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(version.content)
        
        return version
    
    def diff_versions(self, doc_name: str, version1: int, version2: int) -> Dict[str, Any]:
        """Compare two versions of a document."""
        doc = self.get_document(doc_name)
        if not doc:
            raise ValueError(f"Document not found: {doc_name}")
        
        v1 = doc.get_version(version1)
        v2 = doc.get_version(version2)
        
        if not v1 or not v2:
            raise ValueError("One or both versions not found")
        
        # Simple line-based diff
        lines1 = v1.content.split('\n')
        lines2 = v2.content.split('\n')
        
        return {
            'version1': version1,
            'version2': version2,
            'lines_v1': len(lines1),
            'lines_v2': len(lines2),
            'changed': v1.hash != v2.hash
        }
