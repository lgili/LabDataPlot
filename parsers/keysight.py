"""
Parser for Keysight 34970A (BenchLink Data Logger) exported files.

Format:
- Header with metadata in the first rows
- Channel configuration (row 6 onwards)
- Data starts after "Scan Control:" and "Scan" header
- Alternating columns: value and alarm for each channel
"""

import pandas as pd
import re
from pathlib import Path
from datetime import datetime
from .base import BaseParser, DataInfo


class KeysightParser(BaseParser):
    """Parser for Keysight 34970A BenchLink files."""

    name = "keysight"
    description = "Parser for Keysight 34970A BenchLink Data Logger files"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Keysight file."""
        try:
            df = pd.read_excel(filepath, sheet_name=0, header=None, nrows=10)

            # Look for typical Keysight identifiers
            for i in range(min(6, len(df))):
                row_values = df.iloc[i].astype(str).str.lower()
                if any('34970' in str(v) or '34972' in str(v) for v in row_values):
                    return True
                if any('instrument:' in str(v) for v in row_values):
                    return True

            return False
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Keysight file."""
        # Read complete file without header
        df_raw = pd.read_excel(filepath, sheet_name=0, header=None)

        # Extract metadata from header
        metadata = self._parse_header(df_raw)

        # Find where data starts
        data_start_row = self._find_data_start(df_raw)

        if data_start_row is None:
            raise ValueError("Could not find data start in file")

        # Read data - data_start_row is the header, data starts on next row
        df = pd.read_excel(
            filepath,
            sheet_name=0,
            header=data_start_row
        )

        # Process columns - remove alarm columns
        df, channels, units = self._process_columns(df)

        # Process time column
        time_col = self._find_time_column(df)
        if time_col:
            df = self._convert_time(df, time_col)

        # Create DataInfo
        info = DataInfo(
            filename=Path(filepath).name,
            equipment='Keysight 34970A',
            acquisition_date=metadata.get('acquisition_date'),
            channels=channels,
            time_column=time_col,
            units=units,
            metadata=metadata
        )

        return df, info

    def _parse_header(self, df: pd.DataFrame) -> dict:
        """Extracts metadata from header."""
        metadata = {}

        for i in range(min(10, len(df))):
            row = df.iloc[i]
            first_col = str(row.iloc[0]).lower() if pd.notna(row.iloc[0]) else ''

            if 'name:' in first_col:
                metadata['name'] = row.iloc[1] if pd.notna(row.iloc[1]) else None

            elif 'owner:' in first_col:
                metadata['owner'] = row.iloc[1] if pd.notna(row.iloc[1]) else None

            elif 'acquisition date:' in first_col:
                date_val = row.iloc[1]
                if pd.notna(date_val):
                    if isinstance(date_val, datetime):
                        metadata['acquisition_date'] = date_val.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        metadata['acquisition_date'] = str(date_val)

            elif 'instrument:' in first_col:
                metadata['instrument'] = row.iloc[1] if pd.notna(row.iloc[1]) else None
                # Look for slots
                for j in range(len(row)):
                    val = str(row.iloc[j]).lower() if pd.notna(row.iloc[j]) else ''
                    if 'slot' in val and j + 1 < len(row):
                        metadata[val.replace(':', '')] = row.iloc[j + 1]

            elif 'total channels:' in first_col:
                metadata['total_channels'] = row.iloc[1] if pd.notna(row.iloc[1]) else None

        return metadata

    def _find_data_start(self, df: pd.DataFrame) -> int | None:
        """Finds the row where data starts."""
        for i in range(len(df)):
            first_val = str(df.iloc[i, 0]).lower() if pd.notna(df.iloc[i, 0]) else ''
            if first_val == 'scan':
                return i
        return None

    def _process_columns(self, df: pd.DataFrame) -> tuple[pd.DataFrame, list, dict]:
        """Removes alarm columns and extracts units."""
        columns_to_keep = []
        channels = []
        units = {}

        for col in df.columns:
            col_str = str(col).lower()

            # Skip alarm columns
            if 'alarm' in col_str:
                continue

            columns_to_keep.append(col)

            # Extract unit from column name
            name, unit = self._extract_unit(str(col))
            if unit:
                units[col] = unit
                channels.append(name)
            elif col not in ['Scan', 'Time']:
                channels.append(str(col))

        return df[columns_to_keep], channels, units

    def _find_time_column(self, df: pd.DataFrame) -> str | None:
        """Finds the time column."""
        for col in df.columns:
            col_lower = str(col).lower()
            if col_lower == 'time' or 'time' in col_lower:
                return col
        return None

    def _convert_time(self, df: pd.DataFrame, time_col: str) -> pd.DataFrame:
        """Converts time column to datetime."""
        try:
            # Typical format: "25/11/2025 17:37:51:442"
            df[time_col] = pd.to_datetime(df[time_col], format='%d/%m/%Y %H:%M:%S:%f')
        except (ValueError, TypeError):
            try:
                df[time_col] = pd.to_datetime(df[time_col])
            except (ValueError, TypeError):
                pass  # Keep as is
        return df

    def get_channels_by_slot(self, df: pd.DataFrame) -> dict:
        """
        Groups channels by slot (1xx, 2xx, 3xx).

        Returns:
            dict: {1: [slot 1 channels], 2: [slot 2 channels], ...}
        """
        slots = {}
        for col in df.columns:
            if col in ['Scan', 'Time']:
                continue

            # Extract channel number
            name, _ = self._extract_unit(str(col))
            match = re.match(r'(\d)', name)
            if match:
                slot = int(match.group(1))
                if slot not in slots:
                    slots[slot] = []
                slots[slot].append(col)

        return slots
