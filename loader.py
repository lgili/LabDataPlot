"""
DataLoader - Flexible data loader for multiple file formats.
"""

import pandas as pd
from pathlib import Path
from .parsers import get_parser, PARSERS
from .parsers.base import BaseParser, DataInfo


class DataLoader:
    """
    Data loader with support for multiple formats.

    Usage:
        # With automatic detection
        loader = DataLoader('file.xlsx')

        # Specifying format
        loader = DataLoader('file.xlsx', format='keysight')

        # Access data
        df = loader.data
        info = loader.info
        print(loader.columns)
    """

    def __init__(self, filepath: str, format: str | None = None):
        """
        Initializes the loader.

        Args:
            filepath: Path to the file
            format: Format/parser name (optional, auto-detects if not provided)
        """
        self.filepath = Path(filepath)

        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        # Select parser
        if format:
            parser_class = get_parser(format)
            self._parser = parser_class()
        else:
            self._parser = self._auto_detect()

        # Load data
        self._data, self._info = self._parser.parse(str(self.filepath))

    def _auto_detect(self) -> BaseParser:
        """Automatically detects the file format."""
        for name, parser_class in PARSERS.items():
            parser = parser_class()
            if parser.detect(str(self.filepath)):
                return parser

        raise ValueError(
            f"Could not detect file format: {self.filepath.name}\n"
            f"Supported formats: {', '.join(PARSERS.keys())}"
        )

    @property
    def data(self) -> pd.DataFrame:
        """Returns the DataFrame with data."""
        return self._data

    @property
    def info(self) -> DataInfo:
        """Returns file metadata."""
        return self._info

    @property
    def columns(self) -> list:
        """Lists all data columns (excluding time)."""
        time_col = self._info.time_column
        return [c for c in self._data.columns if c != time_col]

    @property
    def time(self) -> pd.Series | None:
        """Returns the time column, if it exists."""
        if self._info.time_column:
            return self._data[self._info.time_column]
        return None

    def __getitem__(self, key):
        """Direct column access: loader['column']"""
        return self._data[key]

    def __repr__(self):
        return (
            f"DataLoader(\n"
            f"  file='{self.filepath.name}',\n"
            f"  format='{self._parser.name}',\n"
            f"  shape={self._data.shape},\n"
            f"  columns={len(self.columns)}\n"
            f")"
        )

    def head(self, n: int = 5) -> pd.DataFrame:
        """Shows the first n rows."""
        return self._data.head(n)

    def describe(self) -> pd.DataFrame:
        """Descriptive statistics of the data."""
        return self._data.describe()

    def get_channel(self, pattern: str) -> list:
        """
        Finds channels matching a pattern.

        Args:
            pattern: Search pattern (e.g., '_01', '101')

        Returns:
            list: List of matching columns
        """
        import re
        regex = re.compile(pattern, re.IGNORECASE)
        return [c for c in self.columns if regex.search(str(c))]
