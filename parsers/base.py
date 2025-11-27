"""
Base class for data parsers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd


@dataclass
class DataInfo:
    """Metadata from the loaded file."""
    filename: str
    equipment: str
    acquisition_date: Optional[str] = None
    channels: list = field(default_factory=list)
    time_column: Optional[str] = None
    sample_rate: Optional[float] = None
    units: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def __repr__(self):
        return (
            f"DataInfo(\n"
            f"  equipment='{self.equipment}',\n"
            f"  channels={len(self.channels)},\n"
            f"  time_column='{self.time_column}',\n"
            f"  acquisition_date='{self.acquisition_date}'\n"
            f")"
        )


class BaseParser(ABC):
    """Abstract base class for data parsers."""

    name: str = "base"
    description: str = "Base parser"

    @abstractmethod
    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """
        Reads and processes the file.

        Returns:
            tuple: (DataFrame with data, DataInfo with metadata)
        """
        pass

    @abstractmethod
    def detect(self, filepath: str) -> bool:
        """
        Detects if the file is compatible with this parser.

        Returns:
            bool: True if file is compatible
        """
        pass

    def _parse_time_column(self, df: pd.DataFrame, time_col: str) -> pd.DataFrame:
        """Attempts to convert time column to datetime or timedelta."""
        if time_col not in df.columns:
            return df

        col = df[time_col]

        # Try to convert to datetime
        try:
            df[time_col] = pd.to_datetime(col)
            return df
        except (ValueError, TypeError):
            pass

        # Try to convert to numeric (seconds)
        try:
            df[time_col] = pd.to_numeric(col)
            return df
        except (ValueError, TypeError):
            pass

        return df

    def _extract_unit(self, column_name: str) -> tuple[str, Optional[str]]:
        """
        Extracts unit from column name.

        Example: "101 (VDC)" -> ("101", "VDC")
        """
        import re
        match = re.search(r'(.+?)\s*\(([^)]+)\)', column_name)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return column_name, None
