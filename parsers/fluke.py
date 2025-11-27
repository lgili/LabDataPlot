"""
Parser for Fluke datalogger files.

Supports exports from:
- Hydra 2680/2686 series
- 1620A/1621A DewK
- 2638A Hydra III

Format:
- CSV or Excel with header
- Timestamp and channel readings
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class FlukeParser(BaseParser):
    """Parser for Fluke datalogger files."""

    name = "fluke"
    description = "Parser for Fluke Hydra datalogger exports"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Fluke file."""
        try:
            path = Path(filepath)
            suffix = path.suffix.lower()

            if suffix in ['.csv', '.txt']:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    header_lines = [f.readline() for _ in range(15)]
                    header_text = ''.join(header_lines).lower()

                    fluke_markers = [
                        'fluke',
                        'hydra',
                        '2680',
                        '2686',
                        '2638',
                        '1620',
                        '1621',
                        'dewk',
                    ]
                    return any(marker in header_text for marker in fluke_markers)

            elif suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath, nrows=10, header=None)
                text = df.astype(str).values.flatten()
                text_lower = ' '.join(text).lower()

                return 'fluke' in text_lower or 'hydra' in text_lower

            return False
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Fluke file."""
        path = Path(filepath)
        suffix = path.suffix.lower()
        metadata = {}

        if suffix in ['.xlsx', '.xls']:
            df, metadata = self._parse_excel(filepath)
        else:
            df, metadata = self._parse_csv(filepath)

        # Find time column
        time_col = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(t in col_lower for t in ['time', 'date', 'timestamp', 'scan']):
                time_col = col
                break

        # Try to parse time
        if time_col:
            try:
                df[time_col] = pd.to_datetime(df[time_col])
            except (ValueError, TypeError):
                try:
                    df[time_col] = pd.to_numeric(df[time_col])
                except (ValueError, TypeError):
                    pass

        # Extract channels
        channels = [c for c in df.columns if c != time_col]

        # Parse units from column names
        units = {}
        for col in channels:
            name, unit = self._extract_unit(str(col))
            if unit:
                units[col] = unit

        info = DataInfo(
            filename=path.name,
            equipment='Fluke Hydra Datalogger',
            acquisition_date=metadata.get('acquisition_date'),
            channels=channels,
            time_column=time_col,
            units=units,
            metadata=metadata
        )

        return df, info

    def _parse_csv(self, filepath: str) -> tuple[pd.DataFrame, dict]:
        """Parse CSV format."""
        metadata = {}
        header_row = 0

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines[:20]):
            line_lower = line.lower()

            # Parse metadata
            if 'fluke' in line_lower or 'hydra' in line_lower:
                metadata['manufacturer'] = 'Fluke'
                match = re.search(r'(\d{4}[a-z]?)', line)
                if match:
                    metadata['model'] = match.group(1)

            if 'date' in line_lower:
                match = re.search(r'(\d{4}[/-]\d{2}[/-]\d{2})', line)
                if match:
                    metadata['acquisition_date'] = match.group(1)

            # Find header row
            if 'time' in line_lower or 'channel' in line_lower or 'ch' in line_lower:
                header_row = i
                break

            if i > 8 and re.match(r'^[\d.,-]+', line):
                header_row = max(0, i - 1)
                break

        df = pd.read_csv(filepath, skiprows=header_row)
        return df, metadata

    def _parse_excel(self, filepath: str) -> tuple[pd.DataFrame, dict]:
        """Parse Excel format."""
        metadata = {}

        # Read first rows to find header
        df_raw = pd.read_excel(filepath, header=None, nrows=20)

        header_row = 0
        for i in range(len(df_raw)):
            row_text = ' '.join(df_raw.iloc[i].astype(str)).lower()

            if 'fluke' in row_text or 'hydra' in row_text:
                metadata['manufacturer'] = 'Fluke'

            if 'time' in row_text or 'channel' in row_text:
                header_row = i
                break

        df = pd.read_excel(filepath, header=header_row)
        return df, metadata
