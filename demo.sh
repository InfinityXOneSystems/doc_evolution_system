#!/bin/bash
# Demo script for Document Evolution System

echo "=== Document Evolution System Demo ==="
echo ""

# Initialize
echo "1. Initialize the system:"
python3 cli.py init
echo ""

# Track the README
echo "2. Track the README.md:"
python3 cli.py track README.md -m "Initial version" -a "Demo User"
echo ""

# Create a test document
echo "3. Create a test document:"
cat > test_doc.md << 'EOF'
# Test Document

## Version 1
This is the first version of the test document.

### Features
- Feature A
- Feature B
EOF

# Track it
echo "4. Track the test document:"
python3 cli.py track test_doc.md -m "Initial test document" -a "Demo User"
echo ""

# Modify the document
echo "5. Modify the test document:"
cat >> test_doc.md << 'EOF'

## Version 2 Changes
- Added Feature C
- Improved Feature A
EOF

# Update it
echo "6. Update the tracked document:"
python3 cli.py update test_doc.md -m "Added version 2 changes" -a "Demo User"
echo ""

# List all documents
echo "7. List all tracked documents:"
python3 cli.py list
echo ""

# Show history
echo "8. Show version history:"
python3 cli.py history test_doc.md
echo ""

# Show status
echo "9. Check system status:"
python3 cli.py status
echo ""

# Compare versions
echo "10. Compare versions 1 and 2:"
python3 cli.py diff test_doc.md 1 2
echo ""

# Restore old version
echo "11. Restore version 1 to a new file:"
python3 cli.py restore test_doc.md 1 -o test_doc_v1.md
echo ""

echo "12. Show contents of restored version:"
cat test_doc_v1.md
echo ""

echo "=== Demo Complete ==="
echo ""
echo "Files created:"
echo "  - test_doc.md (current version)"
echo "  - test_doc_v1.md (restored version 1)"
echo ""
echo "Version data stored in: .doc_evolve/"
