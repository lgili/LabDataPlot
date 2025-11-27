"""
Parser for Yokogawa data acquisition files.

Supports exports from:
- DL series oscilloscopes (DL850, DL350, etc.)
- SL series ScopeCorders
- WT series power analyzers
- MW100/MW200 data acquisition units

Format varies by product but typically:
- CSV with header containing model info
- Time column and channel data
- Units in header or column names
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class YokogawaParser(BaseParser):
    """Parser for Yokogawa instrument files."""

    name = "yokogawa"
    description = "Parser for Yokogawa DL/SL/WT/MW series exports"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Yokogawa file."""
        try:
            path = Path(filepath)
            suffix = path.suffix.lower()

            if suffix in ['.csv', '.txt']:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    header_lines = [f.readline() for _ in range(25)]
                    header_text = ''.join(header_lines).lower()

                    yokogawa_markers = [
                        'yokogawa',
                        'dl850',
                        'dl350',
                        'dl750',
                        'sl1000',
                        'wt300',
                        'wt500',
                        'wt1800',
                        'wt3000',
                        'wt5000',
                        'mw100',
                        'mw200',
                        'scopecorder',
                        'dlm',
                    ]
                    return any(marker in header_text for marker in yokogawa_markers)

            elif suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath, nrows=15, header=None)
                text = df.astype(str).values.flatten()
                text_lower = ' '.join(text).lower()

                return 'yokogawa' in text_lower or 'dl850' in text_lower or 'wt' in text_lower

            return False
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Yokogawa file."""
        path = Path(filepath)
        suffix = path.suffix.lower()
        metadata = {}

        if suffix in ['.xlsx', '.xls']:
            df, metadata = self._parse_excel(filepath)
        else:
            df, metadata = self._parse_csv(filepath)

        # Find time column
        time_col = self._find_time_column(df)

        # Try to parse time
        if time_col:
            df = self._parse_time(df, time_col)

        # Extract channels
        channels = [c for c in df.columns if c != time_col]

        # Parse units
        units = {}
        for col in channels:
            name, unit = self._extract_unit(str(col))
            if unit:
                units[col] = unit
            # Yokogawa format: "CH1[V]" or "P1[W]"
            match = re.search(r'\[([^\]]+)\]', str(col))
            if match:
                units[col] = match.group(1)

        # Calculate sample rate
        sample_rate = metadata.get('sample_rate')
        if sample_rate is None and time_col:
            if df[time_col].dtype in ['float64', 'float32', 'int64', 'int32']:
                if len(df) > 1:
                    dt = df[time_col].iloc[1] - df[time_col].iloc[0]
                    if dt > 0:
                        sample_rate = 1.0 / dt

        # Detect equipment type
        equipment = 'Yokogawa'
        if 'model' in metadata:
            model = metadata['model'].upper()
            if 'DL' in model:
                equipment = 'Yokogawa DL Oscilloscope'
            elif 'SL' in model:
                equipment = 'Yokogawa ScopeCorder'
            elif 'WT' in model:
                equipment = 'Yokogawa WT Power Analyzer'
            elif 'MW' in model:
                equipment = 'Yokogawa MW Data Acquisition'

        info = DataInfo(
            filename=path.name,
            equipment=equipment,
            acquisition_date=metadata.get('acquisition_date'),
            channels=channels,
            time_column=time_col,
            sample_rate=sample_rate,
            units=units,
            metadata=metadata
        )

        return df, info

    def _parse_csv(self, filepath: str) -> tuple[pd.DataFrame, dict]:
        """Parse CSV format."""
        metadata = {}
        header_row = 0

        encodings = ['utf-8', 'shift-jis', 'cp1252', 'latin-1']

        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines[:30]):
                    line_lower = line.lower()

                    # Parse metadata
                    if 'model' in line_lower or 'yokogawa' in line_lower:
                        metadata['model'] = line.strip()

                    if 'date' in line_lower:
                        match = re.search(r'(\d{4}[/-]\d{2}[/-]\d{2})', line)
                        if match:
                            metadata['acquisition_date'] = match.group(1)

                    if 'sample' in line_lower and 'rate' in line_lower:
                        match = re.search(r'([\d.]+)\s*(hz|khz|mhz|s|ms|us)', line_lower)
                        if match:
                            value = float(match.group(1))
                            unit = match.group(2)
                            if unit == 'khz':
                                value *= 1000
                            elif unit == 'mhz':
                                value *= 1000000
                            elif unit == 's':
                                value = 1.0 / value
                            elif unit == 'ms':
                                value = 1000.0 / value
                            elif unit == 'us':
                                value = 1000000.0 / value
                            metadata['sample_rate'] = value

                    # Find header row
                    if 'time' in line_lower or 'ch1' in line_lower or 'ch 1' in line_lower:
                        header_row = i
                        break

                    if i > 10 and re.match(r'^-?[\d.e+-]+[,\t]', line):
                        header_row = max(0, i - 1)
                        break

                df = pd.read_csv(filepath, skiprows=header_row, encoding=encoding)
                return df, metadata

            except Exception:
                continue

        df = pd.read_csv(filepath)
        return df, metadata

    def _parse_excel(self, filepath: str) -> tuple[pd.DataFrame, dict]:
        """Parse Excel format."""
        metadata = {}

        df_raw = pd.read_excel(filepath, header=None, nrows=30)

        header_row = 0
        for i in range(len(df_raw)):
            row_text = ' '.join(df_raw.iloc[i].astype(str)).lower()

            if 'yokogawa' in row_text or any(m in row_text for m in ['dl850', 'wt', 'mw']):
                metadata['model'] = row_text

            if 'time' in row_text or 'ch1' in row_text:
                header_row = i
                break

        df = pd.read_excel(filepath, header=header_row)
        return df, metadata

    def _find_time_column(self, df: pd.DataFrame) -> str | None:
        """Find time column."""
        for col in df.columns:
            col_lower = str(col).lower()
            if any(t in col_lower for t in ['time', 'date', 't[s]', 't[ms]', 'elapsed']):
                return col

        # Check first column
        if len(df.columns) > 0:
            first_col = df.columns[0]
            try:
                numeric = pd.to_numeric(df[first_col], errors='coerce')
                if numeric.is_monotonic_increasing:
                    return first_col
            except Exception:
                pass

        return None

    def _parse_time(self, df: pd.DataFrame, time_col: str) -> pd.DataFrame:
        """Parse time column."""
        try:
            df[time_col] = pd.to_datetime(df[time_col])
            return df
        except (ValueError, TypeError):
            pass

        try:
            df[time_col] = pd.to_numeric(df[time_col])
            return df
        except (ValueError, TypeError):
            pass

        return df
