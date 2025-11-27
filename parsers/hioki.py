"""
Parser for Hioki datalogger files.

Supports exports from:
- LR8400/LR8401/LR8402 series
- MR8875 Memory HiCorder
- LR8410/LR8416 wireless loggers

Format:
- CSV with Japanese/English headers
- Time column and channel data
- Multiple encoding support (Shift-JIS, UTF-8)
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class HiokiParser(BaseParser):
    """Parser for Hioki datalogger files."""

    name = "hioki"
    description = "Parser for Hioki LR/MR series datalogger exports"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Hioki file."""
        try:
            path = Path(filepath)
            suffix = path.suffix.lower()

            if suffix in ['.csv', '.txt']:
                # Try multiple encodings (Hioki often uses Shift-JIS)
                for encoding in ['utf-8', 'shift-jis', 'cp932']:
                    try:
                        with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                            header_lines = [f.readline() for _ in range(15)]
                            header_text = ''.join(header_lines).lower()

                            hioki_markers = [
                                'hioki',
                                'lr8400',
                                'lr8401',
                                'lr8402',
                                'lr8410',
                                'lr8416',
                                'mr8875',
                                'memory hicorder',
                            ]
                            if any(marker in header_text for marker in hioki_markers):
                                return True
                    except Exception:
                        continue

            elif suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath, nrows=10, header=None)
                text = df.astype(str).values.flatten()
                text_lower = ' '.join(text).lower()

                return 'hioki' in text_lower or 'lr84' in text_lower

            return False
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Hioki file."""
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
            if any(t in col_lower for t in ['time', 'date', '時間', '日時']):
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

        # Detect equipment model
        equipment = 'Hioki Datalogger'
        if 'model' in metadata:
            model = metadata['model'].upper()
            if 'MR' in model:
                equipment = 'Hioki Memory HiCorder'
            elif 'LR' in model:
                equipment = 'Hioki LR Datalogger'

        info = DataInfo(
            filename=path.name,
            equipment=equipment,
            acquisition_date=metadata.get('acquisition_date'),
            channels=channels,
            time_column=time_col,
            units=units,
            metadata=metadata
        )

        return df, info

    def _parse_csv(self, filepath: str) -> tuple[pd.DataFrame, dict]:
        """Parse CSV format with encoding detection."""
        metadata = {}
        header_row = 0
        encoding_used = 'utf-8'

        # Try different encodings
        for encoding in ['utf-8', 'shift-jis', 'cp932', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=encoding, errors='strict') as f:
                    lines = f.readlines()
                encoding_used = encoding
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

        for i, line in enumerate(lines[:25]):
            line_lower = line.lower()

            # Parse metadata
            if 'hioki' in line_lower:
                metadata['manufacturer'] = 'Hioki'

            if any(m in line_lower for m in ['lr84', 'mr88']):
                match = re.search(r'(lr\d+|mr\d+)', line_lower)
                if match:
                    metadata['model'] = match.group(1).upper()

            if 'date' in line_lower or '日付' in line:
                match = re.search(r'(\d{4}[/-]\d{2}[/-]\d{2})', line)
                if match:
                    metadata['acquisition_date'] = match.group(1)

            # Find header row
            if 'time' in line_lower or 'ch' in line_lower or '時間' in line:
                header_row = i
                break

            if i > 10 and re.match(r'^[\d.,-]+', line):
                header_row = max(0, i - 1)
                break

        df = pd.read_csv(filepath, skiprows=header_row, encoding=encoding_used)
        return df, metadata

    def _parse_excel(self, filepath: str) -> tuple[pd.DataFrame, dict]:
        """Parse Excel format."""
        metadata = {}

        df_raw = pd.read_excel(filepath, header=None, nrows=25)

        header_row = 0
        for i in range(len(df_raw)):
            row_text = ' '.join(df_raw.iloc[i].astype(str)).lower()

            if 'hioki' in row_text:
                metadata['manufacturer'] = 'Hioki'

            if 'time' in row_text or 'ch' in row_text:
                header_row = i
                break

        df = pd.read_excel(filepath, header=header_row)
        return df, metadata
