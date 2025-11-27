"""
Parser for Tektronix oscilloscope files.

Supports exports from:
- TDS series (TDS1000, TDS2000, TDS3000)
- MSO/DPO series (MSO4000, DPO4000, etc.)
- MDO series (MDO3000, MDO4000)

Format:
- CSV with metadata header
- Time column and channel data (CH1, CH2, etc.)
- Optional math and reference channels
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class TektronixParser(BaseParser):
    """Parser for Tektronix oscilloscope files."""

    name = "tektronix"
    description = "Parser for Tektronix oscilloscope CSV exports"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Tektronix file."""
        try:
            path = Path(filepath)
            if path.suffix.lower() not in ['.csv', '.txt']:
                return False

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                header_lines = [f.readline() for _ in range(10)]
                header_text = ''.join(header_lines).lower()

                tektronix_markers = [
                    'tektronix',
                    'tds',
                    'mso',
                    'dpo',
                    'mdo',
                    'record length',
                    'sample interval',
                    'trigger point',
                ]
                return any(marker in header_text for marker in tektronix_markers)

        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Tektronix CSV file."""
        path = Path(filepath)
        metadata = {}

        # Read header to extract metadata
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        header_row = 0
        for i, line in enumerate(lines[:20]):
            line_lower = line.lower()

            # Parse metadata
            if 'record length' in line_lower:
                match = re.search(r'(\d+)', line)
                if match:
                    metadata['record_length'] = int(match.group(1))

            if 'sample interval' in line_lower:
                match = re.search(r'([\d.e+-]+)', line)
                if match:
                    metadata['sample_interval'] = float(match.group(1))

            if 'model' in line_lower or 'tektronix' in line_lower:
                metadata['model'] = line.strip()

            # Find header row (contains TIME or CH1)
            if 'time' in line_lower or 'ch1' in line_lower:
                header_row = i
                break

            # If we find numeric data, header is previous row
            if i > 5 and re.match(r'^-?[\d.e+-]+[,\t]', line):
                header_row = max(0, i - 1)
                break

        # Read data
        df = pd.read_csv(filepath, skiprows=header_row)

        # Standardize column names
        df.columns = [self._clean_column_name(c) for c in df.columns]

        # Find time column
        time_col = None
        for col in df.columns:
            col_lower = str(col).lower()
            if 'time' in col_lower or col_lower == 't':
                time_col = col
                break

        # If no time column, create from sample interval
        if time_col is None and 'sample_interval' in metadata:
            dt = metadata['sample_interval']
            df.insert(0, 'Time', [i * dt for i in range(len(df))])
            time_col = 'Time'

        # Extract channels
        channels = [c for c in df.columns if c != time_col]

        # Calculate sample rate
        sample_rate = None
        if 'sample_interval' in metadata:
            sample_rate = 1.0 / metadata['sample_interval']

        # Parse units (typically V for oscilloscopes)
        units = {}
        for col in channels:
            if 'ch' in col.lower() or 'math' in col.lower():
                units[col] = 'V'

        info = DataInfo(
            filename=path.name,
            equipment='Tektronix Oscilloscope',
            channels=channels,
            time_column=time_col,
            sample_rate=sample_rate,
            units=units,
            metadata=metadata
        )

        return df, info

    def _clean_column_name(self, name: str) -> str:
        """Clean column name."""
        name = str(name).strip()
        # Standardize channel names
        name = re.sub(r'^ch(\d+)$', r'CH\1', name, flags=re.IGNORECASE)
        return name
