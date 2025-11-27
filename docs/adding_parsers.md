# Adding New Parsers

This guide explains how to add support for new equipment file formats.

## Overview

Each file format is handled by a parser class that:
1. **Detects** if a file matches the format
2. **Parses** the file into a standard DataFrame + metadata structure

## Step-by-Step Guide

### 1. Create the Parser File

Create a new file in `labdataplot/parsers/`:

```python
# labdataplot/parsers/my_equipment.py

"""
Parser for My Equipment exported files.

Format description:
- Explain the file structure here
- What sheets exist
- Where data is located
- Column naming conventions
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class MyEquipmentParser(BaseParser):
    """Parser for My Equipment files."""

    name = "my_equipment"
    description = "Parser for My Equipment data files"

    def detect(self, filepath: str) -> bool:
        """
        Detects if the file is from My Equipment.

        Look for unique identifiers in the file that distinguish
        it from other formats.
        """
        try:
            # Example: check for specific sheet names or content
            xl = pd.ExcelFile(filepath)

            # Check sheet names
            if 'MyDataSheet' in xl.sheet_names:
                return True

            # Or check content
            df = pd.read_excel(filepath, nrows=5, header=None)
            first_cell = str(df.iloc[0, 0]).lower()
            if 'my equipment' in first_cell:
                return True

            return False
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """
        Reads and parses the file.

        Returns:
            tuple: (DataFrame with data, DataInfo with metadata)
        """
        # 1. Read metadata (adapt to your format)
        metadata = self._extract_metadata(filepath)

        # 2. Read the actual data
        df = pd.read_excel(
            filepath,
            sheet_name='DataSheet',  # Adjust as needed
            header=5  # Skip header rows if needed
        )

        # 3. Process columns if needed
        # Remove unwanted columns, rename, etc.

        # 4. Handle time column
        time_col = self._find_time_column(df)
        if time_col:
            df[time_col] = pd.to_datetime(df[time_col])

        # 5. Create DataInfo
        info = DataInfo(
            filename=Path(filepath).name,
            equipment='My Equipment',
            acquisition_date=metadata.get('date'),
            channels=list(df.columns),
            time_column=time_col,
            units=self._extract_units(df.columns),
            metadata=metadata
        )

        return df, info

    def _extract_metadata(self, filepath: str) -> dict:
        """Extract metadata from file header."""
        metadata = {}
        # Your extraction logic here
        return metadata

    def _find_time_column(self, df: pd.DataFrame) -> str | None:
        """Find the time column in the DataFrame."""
        for col in df.columns:
            if 'time' in str(col).lower():
                return col
        return None

    def _extract_units(self, columns) -> dict:
        """Extract units from column names."""
        units = {}
        for col in columns:
            name, unit = self._extract_unit(str(col))
            if unit:
                units[col] = unit
        return units
```

### 2. Register the Parser

Add your parser to `labdataplot/parsers/__init__.py`:

```python
from .base import BaseParser
from .dewesoft import DewesoftParser
from .keysight import KeysightParser
from .my_equipment import MyEquipmentParser  # Add import

PARSERS = {
    'dewesoft': DewesoftParser,
    'keysight': KeysightParser,
    'keysight_34970a': KeysightParser,
    'my_equipment': MyEquipmentParser,  # Add to registry
}
```

### 3. Test Your Parser

```python
from labdataplot import DataLoader

# Test auto-detection
loader = DataLoader('test_file.xlsx')
print(loader.info.equipment)  # Should show 'My Equipment'

# Test explicit format
loader = DataLoader('test_file.xlsx', format='my_equipment')
print(loader.columns)
print(loader.head())
```

## BaseParser Reference

Your parser must inherit from `BaseParser` and implement:

### Required Methods

#### `detect(filepath: str) -> bool`

Returns `True` if the file matches this format.

**Tips:**
- Check sheet names
- Check specific cell contents
- Look for equipment identifiers
- Return `False` on any exception

#### `parse(filepath: str) -> tuple[pd.DataFrame, DataInfo]`

Reads the file and returns data + metadata.

**Must return:**
1. `pd.DataFrame` with the measurement data
2. `DataInfo` object with metadata

### Inherited Helper Methods

#### `_extract_unit(column_name: str) -> tuple[str, str | None]`

Extracts unit from column names like "Channel (V)" -> ("Channel", "V")

#### `_parse_time_column(df, time_col) -> pd.DataFrame`

Attempts to convert a column to datetime.

## DataInfo Fields

| Field | Type | Description |
|-------|------|-------------|
| `filename` | str | Original filename |
| `equipment` | str | Equipment name/model |
| `acquisition_date` | str | Acquisition timestamp |
| `channels` | list | List of data column names |
| `time_column` | str | Name of time column (or None) |
| `sample_rate` | float | Sample rate if known |
| `units` | dict | {column: unit} mapping |
| `metadata` | dict | Any additional metadata |

## Best Practices

1. **Detection should be fast**: Only read what's necessary
2. **Handle exceptions**: Return `False` from detect() on errors
3. **Document the format**: Explain file structure in docstrings
4. **Include equipment-specific methods**: Like `get_channels_by_slot()`
5. **Test with multiple files**: Ensure robustness

## Example: CSV Parser

Here's a simpler example for CSV files:

```python
class SimpleCSVParser(BaseParser):
    """Parser for simple CSV files with time in first column."""

    name = "simple_csv"
    description = "Simple CSV with time column"

    def detect(self, filepath: str) -> bool:
        return filepath.lower().endswith('.csv')

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        df = pd.read_csv(filepath)

        # Assume first column is time
        time_col = df.columns[0]
        df[time_col] = pd.to_datetime(df[time_col])

        info = DataInfo(
            filename=Path(filepath).name,
            equipment='CSV Data',
            channels=list(df.columns[1:]),
            time_column=time_col,
        )

        return df, info
```
