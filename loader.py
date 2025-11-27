"""
DataLoader - Flexible data loader for multiple file formats.
"""

import pandas as pd
import numpy as np
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

        # With time step (generates time axis in seconds)
        loader = DataLoader('file.xlsx', time_step=1.0)  # 1 second between points

        # With time step and display in different unit
        loader = DataLoader('file.xlsx', time_step=1.0, display_unit='min')  # Convert to minutes
        loader = DataLoader('file.xlsx', time_step=1.0, display_unit='h')    # Convert to hours

        # Access data
        df = loader.data
        info = loader.info
        print(loader.columns)
    """

    # Conversion factors to seconds
    TIME_CONVERSIONS = {
        'ms': 0.001,
        's': 1.0,
        'min': 60.0,
        'h': 3600.0,
    }

    def __init__(
        self,
        filepath: str,
        format: str | None = None,
        time_step: float | None = None,
        time_unit: str = 's',
        display_unit: str | None = None
    ):
        """
        Initializes the loader.

        Args:
            filepath: Path to the file
            format: Format/parser name (optional, auto-detects if not provided)
            time_step: Time interval between samples (optional).
                       The unit is specified by time_unit parameter.
                       Examples: 1.0 (1 second if time_unit='s'), 100 (100ms if time_unit='ms')
            time_unit: Unit of the time_step value ('ms', 's', 'min', 'h'). Default: 's'
            display_unit: Unit to display on the time axis ('ms', 's', 'min', 'h').
                          If not provided, uses time_unit.
                          Useful when measuring in seconds but want to display in minutes/hours.
        """
        self.filepath = Path(filepath)
        self._time_step = time_step
        self._time_unit = time_unit
        self._display_unit = display_unit or time_unit

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

        # Generate time axis if time_step is provided
        if time_step is not None:
            self._generate_time_axis(time_step, time_unit, self._display_unit)

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

    def _generate_time_axis(self, time_step: float, time_unit: str, display_unit: str):
        """
        Generates a time axis based on the time step.

        Args:
            time_step: Time interval between samples (in time_unit)
            time_unit: Unit of the time_step ('ms', 's', 'min', 'h')
            display_unit: Unit to display on the axis ('ms', 's', 'min', 'h')
        """
        n_points = len(self._data)

        # Calculate time values in the original unit
        time_values = np.arange(n_points) * time_step

        # Convert to display unit if different
        if time_unit != display_unit:
            # First convert to seconds, then to display unit
            time_in_seconds = time_values * self.TIME_CONVERSIONS.get(time_unit, 1.0)
            time_values = time_in_seconds / self.TIME_CONVERSIONS.get(display_unit, 1.0)

        # Create column name with display unit
        time_col_name = f'Time ({display_unit})'

        # Insert time column at the beginning
        if self._info.time_column and self._info.time_column in self._data.columns:
            # Replace existing time column
            old_time_col = self._info.time_column
            col_idx = self._data.columns.get_loc(old_time_col)
            self._data.drop(columns=[old_time_col], inplace=True)
            self._data.insert(col_idx, time_col_name, time_values)
        else:
            # Insert new time column at the beginning
            self._data.insert(0, time_col_name, time_values)

        # Update info
        self._info.time_column = time_col_name

        # Calculate sample rate in Hz (samples per second)
        time_step_in_seconds = time_step * self.TIME_CONVERSIONS.get(time_unit, 1.0)
        if time_step_in_seconds > 0:
            self._info.sample_rate = 1.0 / time_step_in_seconds

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

    @property
    def time_step(self) -> float | None:
        """Returns the time step used for generating time axis."""
        return self._time_step

    @property
    def time_unit(self) -> str:
        """Returns the time unit of the time_step value."""
        return self._time_unit

    @property
    def display_unit(self) -> str:
        """Returns the display unit for the time axis."""
        return self._display_unit

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
