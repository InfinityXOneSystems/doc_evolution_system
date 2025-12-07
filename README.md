# Document Evolution System

A system that tracks and evolves documents as systems evolve. Keep your documentation synchronized with your codebase changes through automatic version tracking and history management.

## Features

- **Version Tracking**: Automatically track changes to documents with full version history
- **Change Detection**: Smart detection of document changes using content hashing
- **Metadata Support**: Attach metadata (author, message, etc.) to each version
- **History Management**: View complete version history with timestamps and metadata
- **Version Restoration**: Restore any previous version of a document
- **Version Comparison**: Compare different versions to see what changed
- **Persistence**: All version data is automatically saved and persists across sessions
- **CLI Interface**: Easy-to-use command-line tools for all operations

## Installation

No external dependencies required - uses only Python standard library.

```bash
# Make the CLI executable
chmod +x cli.py
```

## Quick Start

### 1. Initialize the System

```bash
python3 cli.py init
```

This creates a `.doc_evolve` directory to store version history.

### 2. Track a Document

```bash
python3 cli.py track README.md -m "Initial version" -a "Your Name"
```

### 3. Update After Changes

After modifying your document:

```bash
python3 cli.py update README.md -m "Added new section" -a "Your Name"
```

### 4. View History

```bash
python3 cli.py history README.md
```

### 5. Check Status

```bash
python3 cli.py status
```

## CLI Commands

### `init [path]`
Initialize a document evolution system in the specified path (default: current directory).

```bash
python3 cli.py init
python3 cli.py init /path/to/project
```

### `track <file>`
Start tracking a document. Creates the first version.

```bash
python3 cli.py track document.md
python3 cli.py track document.md -m "Initial version" -a "John Doe"
```

Options:
- `-m, --message`: Version message describing the changes
- `-a, --author`: Author of the version
- `-r, --root`: Root path of the system (default: current directory)

### `update <file>`
Update a tracked document. Only creates a new version if content has changed.

```bash
python3 cli.py update document.md
python3 cli.py update document.md -m "Updated API docs" -a "Jane Smith"
```

Options:
- `-m, --message`: Version message describing the changes
- `-a, --author`: Author of the version
- `-r, --root`: Root path of the system

### `list`
List all tracked documents with version counts and last update time.

```bash
python3 cli.py list
```

### `history <file>`
Show complete version history for a document.

```bash
python3 cli.py history document.md
```

### `restore <file> <version>`
Restore a specific version of a document.

```bash
# Restore version 1 (overwrites current file)
python3 cli.py restore document.md 1

# Restore to a different file
python3 cli.py restore document.md 1 -o document.v1.md
```

Options:
- `-o, --output`: Output file path (default: overwrites original)

### `diff <file> <version1> <version2>`
Compare two versions of a document.

```bash
python3 cli.py diff document.md 1 2
```

### `status`
Show system status and documents with uncommitted changes.

```bash
python3 cli.py status
```

## Python API

You can also use the system programmatically:

```python
from doc_evolve import DocumentEvolutionSystem

# Initialize system
system = DocumentEvolutionSystem('/path/to/project')

# Track a document
doc = system.track_document('document.md', metadata={
    'author': 'John Doe',
    'message': 'Initial version'
})

# Update after changes
version = system.update_document('document.md', metadata={
    'author': 'Jane Smith',
    'message': 'Updated content'
})

# Get version history
history = system.get_document_history('document.md')

# Restore a version
system.restore_version('document.md', version_number=1)

# Compare versions
diff = system.diff_versions('document.md', 1, 2)
```

## Use Cases

### 1. Documentation Evolution with Code
Track documentation changes alongside code commits:

```bash
# After making code changes and updating docs
python3 cli.py update docs/API.md -m "Updated for v2.0 API changes"
python3 cli.py update docs/README.md -m "Added new features section"
```

### 2. Review Document History
See how a document evolved over time:

```bash
python3 cli.py history docs/architecture.md
```

### 3. Restore Previous Versions
Accidentally overwrote important content? Restore it:

```bash
python3 cli.py restore docs/important.md 3
```

### 4. Compare Versions
See what changed between versions:

```bash
python3 cli.py diff requirements.md 1 2
```

## Architecture

### Components

1. **DocumentVersion**: Represents a single version of a document
   - Content storage
   - SHA256 hash for change detection
   - Timestamp and metadata
   
2. **Document**: Manages multiple versions of a document
   - Version history
   - Change detection
   - Version retrieval

3. **DocumentEvolutionSystem**: Main system coordinator
   - Document tracking
   - State persistence
   - Version management operations

### Storage

All version data is stored in `.doc_evolve/state.json` as JSON:

```json
{
  "documents": {
    "document.md": {
      "name": "document.md",
      "path": "/full/path/to/document.md",
      "current_version": 2,
      "versions": [
        {
          "version": 1,
          "timestamp": "2025-12-07T04:43:00",
          "hash": "abc123...",
          "content": "...",
          "metadata": {
            "author": "John Doe",
            "message": "Initial version"
          }
        }
      ]
    }
  }
}
```

## Running Tests

Run the test suite:

```bash
python3 test_doc_evolve.py
```

Run with verbose output:

```bash
python3 test_doc_evolve.py -v
```

Run specific test:

```bash
python3 -m unittest test_doc_evolve.TestDocumentEvolutionSystem.test_track_document
```

## Examples

### Example 1: Basic Workflow

```bash
# Initialize
python3 cli.py init

# Create and track a document
echo "# My Project" > README.md
python3 cli.py track README.md -m "Initial commit"

# Make changes
echo "\n## Features" >> README.md
python3 cli.py update README.md -m "Added features section"

# Make more changes
echo "\n- Feature 1" >> README.md
python3 cli.py update README.md -m "Listed first feature"

# View history
python3 cli.py history README.md

# Restore version 2
python3 cli.py restore README.md 2
```

### Example 2: Team Collaboration

```bash
# Team member 1
python3 cli.py update specs.md -m "Added API endpoints" -a "Alice"

# Team member 2
python3 cli.py update specs.md -m "Updated authentication" -a "Bob"

# Review history
python3 cli.py history specs.md
```

### Example 3: Document Synchronization

```bash
# Check what needs updating
python3 cli.py status

# Update all changed documents
for file in $(python3 cli.py status | grep "^  -" | cut -d' ' -f4); do
    python3 cli.py update "$file" -m "Synced with system changes"
done
```

## Best Practices

1. **Commit Often**: Track documents frequently to maintain detailed history
2. **Use Meaningful Messages**: Add descriptive messages to help track changes
3. **Include Authors**: Track who made changes for accountability
4. **Regular Status Checks**: Use `status` command to catch uncommitted changes
5. **Version Control Integration**: Use alongside git for complete traceability

## Contributing

Contributions are welcome! The system is designed to be extended with:
- Additional diff algorithms
- Export/import capabilities
- Integration with other version control systems
- Notification systems for document changes
- Automated synchronization triggers

## License

This project is open source and available for use and modification.