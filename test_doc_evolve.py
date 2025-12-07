#!/usr/bin/env python3
"""
Tests for Document Evolution System.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from doc_evolve import (
    DocumentVersion,
    Document,
    DocumentEvolutionSystem
)


class TestDocumentVersion(unittest.TestCase):
    """Test DocumentVersion class."""
    
    def test_create_version(self):
        """Test creating a document version."""
        content = "Hello, World!"
        version = DocumentVersion(content, 1)
        
        self.assertEqual(version.content, content)
        self.assertEqual(version.version, 1)
        self.assertIsNotNone(version.timestamp)
        self.assertIsNotNone(version.hash)
    
    def test_version_with_metadata(self):
        """Test version with metadata."""
        content = "Test content"
        metadata = {'author': 'test', 'message': 'Initial version'}
        version = DocumentVersion(content, 1, metadata)
        
        self.assertEqual(version.metadata['author'], 'test')
        self.assertEqual(version.metadata['message'], 'Initial version')
    
    def test_version_serialization(self):
        """Test version to/from dict conversion."""
        content = "Test content"
        version = DocumentVersion(content, 1, {'key': 'value'})
        
        data = version.to_dict()
        restored = DocumentVersion.from_dict(data)
        
        self.assertEqual(restored.content, version.content)
        self.assertEqual(restored.version, version.version)
        self.assertEqual(restored.hash, version.hash)
        self.assertEqual(restored.metadata, version.metadata)


class TestDocument(unittest.TestCase):
    """Test Document class."""
    
    def test_create_document(self):
        """Test creating a document."""
        doc = Document('test.txt', '/path/to/test.txt')
        
        self.assertEqual(doc.name, 'test.txt')
        self.assertEqual(doc.path, '/path/to/test.txt')
        self.assertEqual(doc.current_version, 0)
        self.assertEqual(len(doc.versions), 0)
    
    def test_add_version(self):
        """Test adding versions to a document."""
        doc = Document('test.txt', '/path/to/test.txt')
        
        v1 = doc.add_version("Version 1 content")
        self.assertEqual(v1.version, 1)
        self.assertEqual(doc.current_version, 1)
        
        v2 = doc.add_version("Version 2 content")
        self.assertEqual(v2.version, 2)
        self.assertEqual(doc.current_version, 2)
        
        self.assertEqual(len(doc.versions), 2)
    
    def test_get_version(self):
        """Test retrieving specific version."""
        doc = Document('test.txt', '/path/to/test.txt')
        v1 = doc.add_version("Version 1")
        v2 = doc.add_version("Version 2")
        
        retrieved_v1 = doc.get_version(1)
        self.assertIsNotNone(retrieved_v1)
        self.assertEqual(retrieved_v1.content, "Version 1")
        
        retrieved_v2 = doc.get_version(2)
        self.assertIsNotNone(retrieved_v2)
        self.assertEqual(retrieved_v2.content, "Version 2")
    
    def test_get_latest_version(self):
        """Test getting latest version."""
        doc = Document('test.txt', '/path/to/test.txt')
        
        self.assertIsNone(doc.get_latest_version())
        
        doc.add_version("Version 1")
        doc.add_version("Version 2")
        
        latest = doc.get_latest_version()
        self.assertIsNotNone(latest)
        self.assertEqual(latest.version, 2)
        self.assertEqual(latest.content, "Version 2")
    
    def test_has_changed(self):
        """Test change detection."""
        doc = Document('test.txt', '/path/to/test.txt')
        
        # No versions yet, should always return True
        self.assertTrue(doc.has_changed("Any content"))
        
        doc.add_version("Original content")
        
        # Same content, should return False
        self.assertFalse(doc.has_changed("Original content"))
        
        # Different content, should return True
        self.assertTrue(doc.has_changed("Modified content"))
    
    def test_document_serialization(self):
        """Test document to/from dict conversion."""
        doc = Document('test.txt', '/path/to/test.txt')
        doc.add_version("Version 1")
        doc.add_version("Version 2")
        
        data = doc.to_dict()
        restored = Document.from_dict(data)
        
        self.assertEqual(restored.name, doc.name)
        self.assertEqual(restored.path, doc.path)
        self.assertEqual(restored.current_version, doc.current_version)
        self.assertEqual(len(restored.versions), len(doc.versions))


class TestDocumentEvolutionSystem(unittest.TestCase):
    """Test DocumentEvolutionSystem class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.system = DocumentEvolutionSystem(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_init_system(self):
        """Test system initialization."""
        self.assertTrue(self.system.evolution_dir.exists())
        self.assertEqual(len(self.system.documents), 0)
    
    def test_track_document(self):
        """Test tracking a new document."""
        # Create a test file
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Initial content")
        
        doc = self.system.track_document(str(test_file))
        
        self.assertEqual(doc.name, 'test.txt')
        self.assertEqual(doc.current_version, 1)
        self.assertIn('test.txt', self.system.documents)
    
    def test_track_document_with_metadata(self):
        """Test tracking document with metadata."""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Initial content")
        
        metadata = {'author': 'tester', 'message': 'Initial version'}
        doc = self.system.track_document(str(test_file), metadata)
        
        latest = doc.get_latest_version()
        self.assertEqual(latest.metadata['author'], 'tester')
        self.assertEqual(latest.metadata['message'], 'Initial version')
    
    def test_update_document(self):
        """Test updating a tracked document."""
        # Create and track a file
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Version 1")
        self.system.track_document(str(test_file))
        
        # Modify and update
        test_file.write_text("Version 2")
        version = self.system.update_document(str(test_file))
        
        self.assertIsNotNone(version)
        self.assertEqual(version.version, 2)
        self.assertEqual(version.content, "Version 2")
    
    def test_update_unchanged_document(self):
        """Test updating document with no changes."""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Same content")
        self.system.track_document(str(test_file))
        
        # Try to update without changes
        version = self.system.update_document(str(test_file))
        
        self.assertIsNone(version)
    
    def test_list_documents(self):
        """Test listing tracked documents."""
        # Create multiple files
        for i in range(3):
            test_file = Path(self.temp_dir) / f'test{i}.txt'
            test_file.write_text(f"Content {i}")
            self.system.track_document(str(test_file))
        
        docs = self.system.list_documents()
        self.assertEqual(len(docs), 3)
        self.assertIn('test0.txt', docs)
        self.assertIn('test1.txt', docs)
        self.assertIn('test2.txt', docs)
    
    def test_get_document_history(self):
        """Test getting document history."""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Version 1")
        self.system.track_document(str(test_file))
        
        test_file.write_text("Version 2")
        self.system.update_document(str(test_file))
        
        history = self.system.get_document_history('test.txt')
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['version'], 1)
        self.assertEqual(history[1]['version'], 2)
    
    def test_restore_version(self):
        """Test restoring a specific version."""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Version 1")
        self.system.track_document(str(test_file))
        
        test_file.write_text("Version 2")
        self.system.update_document(str(test_file))
        
        # Restore version 1
        self.system.restore_version('test.txt', 1)
        
        with open(test_file, 'r') as f:
            content = f.read()
        
        self.assertEqual(content, "Version 1")
    
    def test_restore_to_different_file(self):
        """Test restoring to a different file."""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Version 1")
        self.system.track_document(str(test_file))
        
        test_file.write_text("Version 2")
        self.system.update_document(str(test_file))
        
        # Restore to different file
        output_file = Path(self.temp_dir) / 'restored.txt'
        self.system.restore_version('test.txt', 1, str(output_file))
        
        with open(output_file, 'r') as f:
            content = f.read()
        
        self.assertEqual(content, "Version 1")
    
    def test_diff_versions(self):
        """Test comparing versions."""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Line 1\nLine 2")
        self.system.track_document(str(test_file))
        
        test_file.write_text("Line 1\nLine 2\nLine 3")
        self.system.update_document(str(test_file))
        
        diff = self.system.diff_versions('test.txt', 1, 2)
        
        self.assertEqual(diff['version1'], 1)
        self.assertEqual(diff['version2'], 2)
        self.assertTrue(diff['changed'])
    
    def test_persistence(self):
        """Test that state persists across system instances."""
        test_file = Path(self.temp_dir) / 'test.txt'
        test_file.write_text("Persistent content")
        self.system.track_document(str(test_file))
        
        # Create new system instance
        new_system = DocumentEvolutionSystem(self.temp_dir)
        
        # Should have the tracked document
        self.assertIn('test.txt', new_system.documents)
        doc = new_system.get_document('test.txt')
        self.assertIsNotNone(doc)
        self.assertEqual(doc.current_version, 1)


if __name__ == '__main__':
    unittest.main()
