"""
Parser for Keithley instrument files.

Supports exports from:
- 2400/2450 series SourceMeters
- DMM6500/DAQ6510 multimeters
- 2100/2110 series DMMs

Format:
- CSV with header containing instrument info
- Timestamp and measurement columns
- Multiple readings with statistics
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class KeithleyParser(BaseParser):
    """Parser for Keithley instrument files."""

    name = "keithley"
    description = "Parser for Keithley SourceMeter and DMM exports"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Keithley file."""
        try:
            path = Path(filepath)
            suffix = path.suffix.lower()

            if suffix in ['.csv', '.txt']:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    header_lines = [f.readline() for _ in range(20)]
                    header_text = ''.join(header_lines).lower()

                    keithley_markers = [
                        'keithley',
                        'tektronix keithley',
                        'sourcemeter',
                        'source meter',
                        '2400',
                        '2450',
                        '2460',
                        '2470',
                        'dmm6500',
                        'daq6510',
                        '2100',
                        '2110',
                        'kickstart',
                    ]
                    return any(marker in header_text for marker in keithley_markers)

            elif suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath, nrows=15, header=None)
                text = df.astype(str).values.flatten()
                text_lower = ' '.join(text).lower()

                return 'keithley' in text_lower or 'sourcemeter' in text_lower

            return False
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Keithley file."""
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
            if any(t in col_lower for t in ['time', 'timestamp', 'date', 'reading']):
                time_col = col
                break

        # If no time column, use index
        if time_col is None:
            df.insert(0, 'Reading', range(len(df)))
            time_col = 'Reading'

        # Try to parse time
        if time_col and time_col != 'Reading':
            try:
                df[time_col] = pd.to_datetime(df[time_col])
            except (ValueError, TypeError):
                try:
                    df[time_col] = pd.to_numeric(df[time_col])
                except (ValueError, TypeError):
                    pass

        # Extract channels
        channels = [c for c in df.columns if c != time_col]

        # Parse units (Keithley columns often have units: "Voltage (V)", "Current (A)")
        units = {}
        for col in channels:
            name, unit = self._extract_unit(str(col))
            if unit:
                units[col] = unit
            else:
                # Infer from column name
                col_lower = str(col).lower()
                if 'volt' in col_lower or col_lower == 'v':
                    units[col] = 'V'
                elif 'current' in col_lower or col_lower == 'i':
                    units[col] = 'A'
                elif 'resist' in col_lower or col_lower == 'r':
                    units[col] = 'Ohm'
                elif 'power' in col_lower or col_lower == 'p':
                    units[col] = 'W'

        # Detect equipment type
        equipment = 'Keithley Instrument'
        if 'model' in metadata:
            model = metadata['model']
            if '24' in model:
                equipment = 'Keithley SourceMeter'
            elif 'dmm' in model.lower() or '21' in model:
                equipment = 'Keithley DMM'
            elif 'daq' in model.lower():
                equipment = 'Keithley DAQ'

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
        """Parse CSV format."""
        metadata = {}
        header_row = 0

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines[:30]):
            line_lower = line.lower()

            # Parse metadata
            if 'keithley' in line_lower or 'model' in line_lower:
                match = re.search(r'(\d{4}[a-z]?)', line)
                if match:
                    metadata['model'] = match.group(1)

            if 'date' in line_lower:
                match = re.search(r'(\d{4}[/-]\d{2}[/-]\d{2})', line)
                if match:
                    metadata['acquisition_date'] = match.group(1)

            if 'serial' in line_lower:
                parts = line.split(':')
                if len(parts) > 1:
                    metadata['serial'] = parts[1].strip()

            # Find header row
            if any(h in line_lower for h in ['voltage', 'current', 'time', 'reading', 'v,', 'i,']):
                header_row = i
                break

            if i > 10 and re.match(r'^-?[\d.e+-]+[,\t]', line):
                header_row = max(0, i - 1)
                break

        df = pd.read_csv(filepath, skiprows=header_row)
        return df, metadata

    def _parse_excel(self, filepath: str) -> tuple[pd.DataFrame, dict]:
        """Parse Excel format."""
        metadata = {}

        df_raw = pd.read_excel(filepath, header=None, nrows=30)

        header_row = 0
        for i in range(len(df_raw)):
            row_text = ' '.join(df_raw.iloc[i].astype(str)).lower()

            if 'keithley' in row_text:
                match = re.search(r'(\d{4}[a-z]?)', row_text)
                if match:
                    metadata['model'] = match.group(1)

            if any(h in row_text for h in ['voltage', 'current', 'time', 'reading']):
                header_row = i
                break

        df = pd.read_excel(filepath, header=header_row)
        return df, metadata
