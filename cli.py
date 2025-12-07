#!/usr/bin/env python3
"""
Command-line interface for Document Evolution System.
"""

import argparse
import sys
import json
from pathlib import Path
from doc_evolve import DocumentEvolutionSystem


def cmd_init(args):
    """Initialize a document evolution system."""
    system = DocumentEvolutionSystem(args.path)
    print(f"Initialized document evolution system in {args.path}")
    print(f"Evolution data stored in: {system.evolution_dir}")


def cmd_track(args):
    """Track a new document."""
    system = DocumentEvolutionSystem(args.root)
    metadata = {}
    if args.message:
        metadata['message'] = args.message
    if args.author:
        metadata['author'] = args.author
    
    doc = system.track_document(args.file, metadata)
    latest = doc.get_latest_version()
    print(f"Tracking document: {doc.name}")
    print(f"Version: {latest.version}")
    print(f"Hash: {latest.hash}")


def cmd_update(args):
    """Update a tracked document."""
    system = DocumentEvolutionSystem(args.root)
    metadata = {}
    if args.message:
        metadata['message'] = args.message
    if args.author:
        metadata['author'] = args.author
    
    version = system.update_document(args.file, metadata)
    if version:
        print(f"Updated document: {args.file}")
        print(f"New version: {version.version}")
        print(f"Hash: {version.hash}")
    else:
        print(f"No changes detected in: {args.file}")


def cmd_list(args):
    """List all tracked documents."""
    system = DocumentEvolutionSystem(args.root)
    docs = system.list_documents()
    
    if not docs:
        print("No documents tracked yet.")
        return
    
    print(f"Tracked documents ({len(docs)}):")
    for doc_name in sorted(docs):
        doc = system.get_document(doc_name)
        latest = doc.get_latest_version()
        print(f"  {doc_name}")
        print(f"    Versions: {doc.current_version}")
        if latest:
            print(f"    Last updated: {latest.timestamp}")
            if latest.metadata.get('message'):
                print(f"    Message: {latest.metadata['message']}")


def cmd_history(args):
    """Show version history for a document."""
    system = DocumentEvolutionSystem(args.root)
    history = system.get_document_history(args.file)
    
    if not history:
        print(f"No history found for: {args.file}")
        return
    
    print(f"Version history for {args.file}:")
    for version_info in history:
        print(f"\nVersion {version_info['version']}:")
        print(f"  Timestamp: {version_info['timestamp']}")
        print(f"  Hash: {version_info['hash'][:16]}...")
        if version_info['metadata']:
            if version_info['metadata'].get('message'):
                print(f"  Message: {version_info['metadata']['message']}")
            if version_info['metadata'].get('author'):
                print(f"  Author: {version_info['metadata']['author']}")


def cmd_restore(args):
    """Restore a specific version of a document."""
    system = DocumentEvolutionSystem(args.root)
    version = system.restore_version(args.file, args.version, args.output)
    
    target = args.output or args.file
    print(f"Restored version {args.version} of {args.file} to {target}")
    print(f"Hash: {version.hash}")


def cmd_diff(args):
    """Compare two versions of a document."""
    system = DocumentEvolutionSystem(args.root)
    diff = system.diff_versions(args.file, args.version1, args.version2)
    
    print(f"Comparing versions {args.version1} and {args.version2} of {args.file}:")
    print(f"  Version {args.version1}: {diff['lines_v1']} lines")
    print(f"  Version {args.version2}: {diff['lines_v2']} lines")
    print(f"  Changed: {diff['changed']}")


def cmd_status(args):
    """Show status of tracked documents."""
    system = DocumentEvolutionSystem(args.root)
    docs = system.list_documents()
    
    if not docs:
        print("No documents tracked.")
        return
    
    print(f"Document Evolution System Status")
    print(f"Root: {args.root}")
    print(f"Tracked documents: {len(docs)}")
    
    # Check for changes in tracked documents
    changed = []
    for doc_name in docs:
        doc = system.get_document(doc_name)
        try:
            with open(doc.path, 'r') as f:
                current_content = f.read()
            if doc.has_changed(current_content):
                changed.append(doc_name)
        except FileNotFoundError:
            pass
    
    if changed:
        print(f"\nDocuments with uncommitted changes ({len(changed)}):")
        for doc_name in changed:
            print(f"  - {doc_name}")
    else:
        print("\nNo uncommitted changes.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Document Evolution System - Track and evolve documents as systems evolve'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Init command
    parser_init = subparsers.add_parser('init', help='Initialize document evolution system')
    parser_init.add_argument('path', nargs='?', default='.', help='Root path for the system')
    parser_init.set_defaults(func=cmd_init)
    
    # Track command
    parser_track = subparsers.add_parser('track', help='Start tracking a document')
    parser_track.add_argument('file', help='File to track')
    parser_track.add_argument('-r', '--root', default='.', help='Root path')
    parser_track.add_argument('-m', '--message', help='Version message')
    parser_track.add_argument('-a', '--author', help='Author name')
    parser_track.set_defaults(func=cmd_track)
    
    # Update command
    parser_update = subparsers.add_parser('update', help='Update a tracked document')
    parser_update.add_argument('file', help='File to update')
    parser_update.add_argument('-r', '--root', default='.', help='Root path')
    parser_update.add_argument('-m', '--message', help='Version message')
    parser_update.add_argument('-a', '--author', help='Author name')
    parser_update.set_defaults(func=cmd_update)
    
    # List command
    parser_list = subparsers.add_parser('list', help='List tracked documents')
    parser_list.add_argument('-r', '--root', default='.', help='Root path')
    parser_list.set_defaults(func=cmd_list)
    
    # History command
    parser_history = subparsers.add_parser('history', help='Show document version history')
    parser_history.add_argument('file', help='Document name')
    parser_history.add_argument('-r', '--root', default='.', help='Root path')
    parser_history.set_defaults(func=cmd_history)
    
    # Restore command
    parser_restore = subparsers.add_parser('restore', help='Restore a document version')
    parser_restore.add_argument('file', help='Document name')
    parser_restore.add_argument('version', type=int, help='Version number')
    parser_restore.add_argument('-o', '--output', help='Output file (default: overwrite original)')
    parser_restore.add_argument('-r', '--root', default='.', help='Root path')
    parser_restore.set_defaults(func=cmd_restore)
    
    # Diff command
    parser_diff = subparsers.add_parser('diff', help='Compare document versions')
    parser_diff.add_argument('file', help='Document name')
    parser_diff.add_argument('version1', type=int, help='First version')
    parser_diff.add_argument('version2', type=int, help='Second version')
    parser_diff.add_argument('-r', '--root', default='.', help='Root path')
    parser_diff.set_defaults(func=cmd_diff)
    
    # Status command
    parser_status = subparsers.add_parser('status', help='Show system status')
    parser_status.add_argument('-r', '--root', default='.', help='Root path')
    parser_status.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
