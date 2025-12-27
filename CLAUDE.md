# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python social graph analyzer that processes CSV files to analyze friendship networks, calculate FOAF (Friend of a Friend) relationships, and export to various formats including JSON and GraphML for visualization in Gephi.

## Key Architecture

### Core Design
- **Zero external dependencies** - Uses only Python standard library modules
- **Wrapper script pattern** - `./social-graph` wrapper adds `src/` to Python path before importing
- **Graph representation** - Uses `defaultdict(set)` for efficient friendship storage
- **Bidirectional by default** - Friendships are mutual unless `--no-bidirectional` flag is used

### Module Structure
```
src/social_graph/
├── __init__.py          # Package exports
├── cli.py               # Command-line interface
└── graph.py             # SocialGraph class (core logic)
```

### Entry Points
- **Wrapper script**: `./social-graph` (recommended - no installation needed)
- **Direct execution**: `python -m social_graph.cli` (requires src/ in PYTHONPATH)
- **Programmatic**: `from social_graph import SocialGraph`

## Common Commands

### Running Analysis
```bash
# Basic usage with stats
./social-graph data/input/friends.csv --stats

# Full export (JSON + GraphML + FOAF report)
./social-graph data/input/friends.csv \
  --output data/output/graph.json \
  --graphml data/output/graph.graphml \
  --foaf-report data/output/foaf.json \
  --stats

# Query specific user
./social-graph data/input/friends.csv --query-user Alice

# Unidirectional mode (followers, not friends)
./social-graph data/input/followers.csv --no-bidirectional
```

### Testing
```bash
# Run example script
python examples/advanced_usage.py data/input/friends.csv
```

## CSV Input Format

**Critical**: Each line is `User,Friend1,Friend2,Friend3,...`

```csv
Alice,Bob,Charlie,David
Bob,Alice,Eve,Frank
Charlie,Alice,David,George
```

**Data cleaning**:
- Spaces are stripped automatically
- Duplicates are eliminated via Set
- Empty rows/columns are ignored
- Self-references are prevented

## File Organization

### Data Directories
- `data/input/` - Source CSV files (only `friends.csv` is versioned)
- `data/output/` - Generated files (all ignored by git)

### Git Versioning Policy
- ✅ **Versioned**: `data/input/friends.csv` (example data)
- ❌ **Ignored**: All other `data/input/*.csv` (user's personal data)
- ❌ **Ignored**: All `data/output/*` (generated files)

### Documentation
- `README.md` - Main user documentation
- `docs/gephi-guide.md` - Gephi visualization guide
- `examples/` - Usage examples and sample data

## Code Patterns

### Adding a New Export Format
1. Add method to `SocialGraph` class in `src/social_graph/graph.py`
2. Add CLI argument in `src/social_graph/cli.py`
3. Follow existing patterns (see `to_json()`, `to_graphml()`)

### GraphML Export Requirements
- **Must include `<key id="label">` definition** for Gephi compatibility
- Each node needs `<data key="label">NodeName</data>`
- Escape XML special characters: `&`, `<`, `>`, `"`
- Set `edgedefault="undirected"` for bidirectional graphs

### FOAF Algorithm
```python
def get_foaf(self, user: str) -> Set[str]:
    # 1. Get direct friends
    # 2. For each friend, get their friends (friends of friends)
    # 3. Remove self and direct friends from results
    # Returns: Set of second-degree connections
```

## Important Implementation Notes

### Wrapper Script (`social-graph`)
- **Why it exists**: Avoids `pip install -e .` issues with editable installs
- **Linting**: `# noqa: E402` is required - import must come after path manipulation
- **Pylance warning**: False positive - imports work at runtime despite IDE warning

### No Virtual Environment Needed
- Project has zero external dependencies
- All imports are from Python standard library
- No `pip install` required - just Python 3.12+

### Default Output Paths
- JSON: `data/output/social_graph.json`
- All outputs go to `data/output/` to keep repository clean

## Troubleshooting

### "Permission denied: ./social-graph"
```bash
chmod +x social-graph
```

### Output files not being created
- Check that `data/output/` directory exists
- Verify write permissions on output directory
- Default path changed to `data/output/` (not project root)

### Import errors when using programmatically
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "src"))
from social_graph import SocialGraph
```

## Development Guidelines

### Code Style
- Line length: 100 characters (configured in pyproject.toml)
- Type hints: Required for function signatures
- Docstrings: Google style for all public methods
- Python version: 3.12+ (uses modern type hints like `str | Path`)

### When Modifying the Graph Structure
- Remember: `self.graph` is `Dict[str, Set[str]]`
- Use `_clean_name()` for all user input
- Maintain bidirectional consistency in `add_friendship()`
- Use `Set` operations for FOAF calculations (efficient intersections)

### Export Format Compatibility
- JSON: Standard dict-to-JSON with sorted friend lists
- GraphML: XML 1.0, UTF-8, follows GraphML schema 1.0
- FOAF reports: JSON with `direct_friends`, `friends_of_friends`, `total_foaf` keys

## Example Data

`data/input/friends.csv` contains 9 users with 12 bidirectional relationships:
- Alice, Bob, Charlie, David, Eve, Frank, George, Helen, Ivan
- Useful for testing and demonstrating all features
