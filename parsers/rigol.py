"""
Parser for Rigol oscilloscope files.

Supports exports from:
- DS1000 series
- DS2000 series
- MSO5000 series
- DHO series

Format:
- CSV with optional header
- Time column and channel data
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class RigolParser(BaseParser):
    """Parser for Rigol oscilloscope files."""

    name = "rigol"
    description = "Parser for Rigol oscilloscope CSV exports"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Rigol file."""
        try:
            path = Path(filepath)
            if path.suffix.lower() not in ['.csv', '.txt']:
                return False

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                header_lines = [f.readline() for _ in range(15)]
                header_text = ''.join(header_lines).lower()

                rigol_markers = [
                    'rigol',
                    'ds1',
                    'ds2',
                    'mso5',
                    'dho',
                    'dg1',
                    'x(s)',
                    'ch1(v)',
                ]
                return any(marker in header_text for marker in rigol_markers)

        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Rigol CSV file."""
        path = Path(filepath)
        metadata = {}

        # Read header
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        header_row = 0
        for i, line in enumerate(lines[:20]):
            line_lower = line.lower()

            # Parse metadata
            if 'rigol' in line_lower:
                metadata['manufacturer'] = 'Rigol'

            if any(m in line_lower for m in ['ds1', 'ds2', 'mso', 'dho']):
                match = re.search(r'(ds\d+|mso\d+|dho\d+)', line_lower)
                if match:
                    metadata['model'] = match.group(1).upper()

            if 'sample rate' in line_lower:
                match = re.search(r'([\d.e+-]+)', line)
                if match:
                    metadata['sample_rate'] = float(match.group(1))

            # Find header row
            if 'x(' in line_lower or 'time' in line_lower or 'ch1' in line_lower:
                header_row = i
                break

            if i > 5 and re.match(r'^-?[\d.e+-]+[,\t]', line):
                header_row = max(0, i - 1)
                break

        # Read data
        df = pd.read_csv(filepath, skiprows=header_row)

        # Clean column names
        new_columns = []
        for col in df.columns:
            col_str = str(col).strip()
            # Rigol format: "X(S)" -> "Time", "CH1(V)" -> "CH1"
            if col_str.lower().startswith('x('):
                new_columns.append('Time')
            elif match := re.match(r'(ch\d+)\s*\(', col_str, re.IGNORECASE):
                new_columns.append(match.group(1).upper())
            else:
                new_columns.append(col_str)
        df.columns = new_columns

        # Find time column
        time_col = 'Time' if 'Time' in df.columns else None

        # Extract channels
        channels = [c for c in df.columns if c != time_col]

        # Calculate sample rate from data if not in metadata
        sample_rate = metadata.get('sample_rate')
        if sample_rate is None and time_col and len(df) > 1:
            dt = df[time_col].iloc[1] - df[time_col].iloc[0]
            if dt > 0:
                sample_rate = 1.0 / dt

        # Units (typically V for oscilloscope channels)
        units = {ch: 'V' for ch in channels if ch.upper().startswith('CH')}

        info = DataInfo(
            filename=path.name,
            equipment='Rigol Oscilloscope',
            channels=channels,
            time_column=time_col,
            sample_rate=sample_rate,
            units=units,
            metadata=metadata
        )

        return df, info
