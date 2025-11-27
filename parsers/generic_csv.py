"""
Generic CSV parser for simple data files.

Handles standard CSV files with:
- Optional header row
- Time/index column (auto-detected or first column)
- Multiple data columns

This is a fallback parser for CSV files that don't match any specific equipment.
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class GenericCSVParser(BaseParser):
    """Parser for generic CSV data files."""

    name = "csv"
    description = "Generic parser for CSV data files"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a CSV file (used as fallback)."""
        try:
            path = Path(filepath)
            return path.suffix.lower() in ['.csv', '.txt', '.tsv']
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads generic CSV file with smart detection."""
        path = Path(filepath)
        metadata = {}

        # Detect delimiter and encoding
        delimiter, encoding, has_header, skip_rows = self._detect_format(filepath)

        # Read data
        df = pd.read_csv(
            filepath,
            delimiter=delimiter,
            encoding=encoding,
            header=0 if has_header else None,
            skiprows=skip_rows
        )

        # Generate column names if no header
        if not has_header:
            df.columns = [f'Col_{i+1}' for i in range(len(df.columns))]

        # Detect time column
        time_col = self._detect_time_column(df)

        # If no time column, create index
        if time_col is None:
            # Check if first column could be time/index
            first_col = df.columns[0]
            if self._is_monotonic(df[first_col]):
                time_col = first_col
            else:
                df.insert(0, 'Index', range(len(df)))
                time_col = 'Index'

        # Try to parse time column
        if time_col and time_col != 'Index':
            df = self._parse_time(df, time_col)

        # Extract channels
        channels = [c for c in df.columns if c != time_col]

        # Try to extract units from column names
        units = {}
        for col in channels:
            name, unit = self._extract_unit(str(col))
            if unit:
                units[col] = unit

        # Calculate sample rate if time is numeric
        sample_rate = None
        if time_col and df[time_col].dtype in ['float64', 'float32', 'int64', 'int32']:
            if len(df) > 1:
                dt = df[time_col].iloc[1] - df[time_col].iloc[0]
                if dt > 0:
                    sample_rate = 1.0 / dt

        info = DataInfo(
            filename=path.name,
            equipment='Generic CSV',
            channels=channels,
            time_column=time_col,
            sample_rate=sample_rate,
            units=units,
            metadata=metadata
        )

        return df, info

    def _detect_format(self, filepath: str) -> tuple[str, str, bool, int]:
        """Detects CSV format parameters."""
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']

        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding, errors='strict') as f:
                    lines = [f.readline() for _ in range(10)]

                # Detect delimiter
                first_data_line = lines[0]
                delimiters = [',', '\t', ';', '|']
                delimiter = ','

                max_count = 0
                for d in delimiters:
                    count = first_data_line.count(d)
                    if count > max_count:
                        max_count = count
                        delimiter = d

                # Detect if has header (first row contains non-numeric values)
                has_header = False
                first_values = first_data_line.split(delimiter)
                non_numeric = 0
                for val in first_values:
                    val = val.strip().strip('"\'')
                    try:
                        float(val)
                    except ValueError:
                        if val:  # Non-empty non-numeric
                            non_numeric += 1

                has_header = non_numeric > len(first_values) / 2

                # Detect skip rows (comment lines, empty lines at start)
                skip_rows = 0
                for line in lines:
                    line = line.strip()
                    if line.startswith('#') or line.startswith('//') or not line:
                        skip_rows += 1
                    else:
                        break

                return delimiter, encoding, has_header, skip_rows

            except (UnicodeDecodeError, UnicodeError):
                continue

        # Defaults
        return ',', 'utf-8', True, 0

    def _detect_time_column(self, df: pd.DataFrame) -> str | None:
        """Detects which column contains time data."""
        time_keywords = ['time', 'date', 'timestamp', 't', 'datetime', 'elapsed', 'seconds', 'ms']

        for col in df.columns:
            col_lower = str(col).lower()
            if any(kw in col_lower for kw in time_keywords):
                return col

        # Check first column content
        if len(df.columns) > 0:
            first_col = df.columns[0]
            # Try to parse as datetime
            try:
                pd.to_datetime(df[first_col].iloc[:5])
                return first_col
            except (ValueError, TypeError):
                pass

        return None

    def _is_monotonic(self, series: pd.Series) -> bool:
        """Checks if series is monotonically increasing (like time/index)."""
        try:
            numeric = pd.to_numeric(series, errors='coerce')
            if numeric.isna().sum() < len(numeric) * 0.1:  # Less than 10% NaN
                return numeric.is_monotonic_increasing or numeric.is_monotonic_decreasing
        except Exception:
            pass
        return False

    def _parse_time(self, df: pd.DataFrame, time_col: str) -> pd.DataFrame:
        """Attempts to parse time column."""
        # Try datetime parsing
        try:
            df[time_col] = pd.to_datetime(df[time_col])
            return df
        except (ValueError, TypeError):
            pass

        # Try numeric conversion
        try:
            df[time_col] = pd.to_numeric(df[time_col])
            return df
        except (ValueError, TypeError):
            pass

        return df
