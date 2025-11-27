"""
Parser for Dewesoft (Datalogger) exported files.

Format:
- First sheet: metadata (root) with name in YYYYMMDD_HHMMSS format
- Second sheet: "Data" with columns named as PREFIX_NN (e.g., NN_01, NN5494_01)
- No explicit time column in data
"""

import pandas as pd
import re
from pathlib import Path
from .base import BaseParser, DataInfo


class DewesoftParser(BaseParser):
    """Parser for Dewesoft/Datalogger files."""

    name = "dewesoft"
    description = "Parser for Dewesoft Datalogger exported files"

    def detect(self, filepath: str) -> bool:
        """Detects if this is a Dewesoft file."""
        try:
            xl = pd.ExcelFile(filepath)
            sheet_names = xl.sheet_names

            # Check if it has "Data" sheet and a sheet with "(root)" in the name
            has_data = 'Data' in sheet_names
            has_root = any('(root)' in name for name in sheet_names)

            return has_data and has_root
        except Exception:
            return False

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        """Reads Dewesoft file."""
        xl = pd.ExcelFile(filepath)

        # Find metadata sheet (root)
        root_sheet = next((s for s in xl.sheet_names if '(root)' in s), None)

        # Extract metadata
        metadata = {}
        acquisition_date = None

        if root_sheet:
            # Extract date from sheet name (format: YYYYMMDD_HHMMSS)
            match = re.search(r'(\d{8}_\d{6})', root_sheet)
            if match:
                date_str = match.group(1)
                try:
                    acquisition_date = pd.to_datetime(date_str, format='%Y%m%d_%H%M%S')
                    acquisition_date = acquisition_date.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    acquisition_date = date_str

            # Read metadata from root sheet
            df_root = pd.read_excel(filepath, sheet_name=root_sheet, nrows=10)
            metadata['root_name'] = df_root.iloc[0, 0] if len(df_root) > 0 else None

        # Read data
        df = pd.read_excel(filepath, sheet_name='Data')

        # Identify column pattern (PREFIX_NN)
        columns = list(df.columns)
        prefix = None
        if columns:
            match = re.match(r'([A-Za-z0-9]+)_\d+', columns[0])
            if match:
                prefix = match.group(1)
                metadata['channel_prefix'] = prefix

        # Create index column as "time" (sample number)
        df.insert(0, 'Sample', range(len(df)))

        # Create DataInfo
        info = DataInfo(
            filename=Path(filepath).name,
            equipment='Dewesoft Datalogger',
            acquisition_date=acquisition_date,
            channels=columns,
            time_column='Sample',
            units={col: 'V' for col in columns},  # Assumes voltage by default
            metadata=metadata
        )

        return df, info

    def get_channel_groups(self, df: pd.DataFrame) -> dict:
        """
        Groups channels by numeric prefix.

        Example: NN_01 to NN_10 -> group 1, NN_11 to NN_20 -> group 2
        """
        groups = {}
        for col in df.columns:
            if col == 'Sample':
                continue
            match = re.search(r'_(\d+)$', col)
            if match:
                num = int(match.group(1))
                group_num = (num - 1) // 10 + 1
                if group_num not in groups:
                    groups[group_num] = []
                groups[group_num].append(col)
        return groups
