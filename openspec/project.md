# Project Context

## Purpose
LabDataPlot is a Python library for reading and plotting data from laboratory measurement equipment. It simplifies the process of loading, analyzing, and visualizing data exported from instruments like oscilloscopes, dataloggers, and power analyzers.

## Tech Stack
- Python 3.10+
- pandas >= 2.0.0 (data manipulation)
- matplotlib >= 3.7.0 (static plots)
- numpy (numerical operations)
- openpyxl >= 3.1.0 (Excel file support)

## Project Conventions

### Code Style
- Follow PEP 8
- Type hints for all public APIs
- Docstrings in Google style
- Maximum line length: 100 characters

### Architecture Patterns
- **Parser Pattern**: Each equipment type has its own parser inheriting from `BaseParser`
- **Loader/Plotter Separation**: `DataLoader` handles data, `Plotter` handles visualization
- **Auto-detection**: Parsers implement `detect()` to identify file formats

### File Structure
```
labdataplot/
├── __init__.py          # Public API exports
├── loader.py            # DataLoader class
├── plotter.py           # Plotter class
└── parsers/
    ├── base.py          # BaseParser, DataInfo
    ├── keysight.py      # Keysight 34970A
    ├── dewesoft.py      # Dewesoft Datalogger
    ├── tektronix.py     # Tektronix oscilloscopes
    └── ...              # Other parsers
```

### Testing Strategy
- pytest for unit tests
- Test files in `tests/` directory
- Test with sample data files

### Git Workflow
- Main branch: `main`
- Feature branches: `feat/feature-name`
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`

## Domain Context
- **Channels**: Individual measurement signals (e.g., CH1, 101 (VDC))
- **Time Column**: X-axis data, can be timestamps or elapsed time
- **Sample Rate**: Frequency of data acquisition in Hz
- **Units**: Physical units like V, A, °C, Ohm

## Important Constraints
- Must support Python 3.10+
- Minimal dependencies (pandas, matplotlib, numpy, openpyxl)
- No breaking changes to existing API without major version bump
- Parsers must handle different file encodings (UTF-8, Shift-JIS, Latin-1)

## External Dependencies
- PyPI for distribution
- GitHub Actions for CI/CD
- Plotly (optional, for interactive plots)
