"""
Parsers for different equipment file formats.
"""

from .base import BaseParser
from .dewesoft import DewesoftParser
from .keysight import KeysightParser
from .tektronix import TektronixParser
from .rigol import RigolParser
from .fluke import FlukeParser
from .hioki import HiokiParser
from .yokogawa import YokogawaParser
from .keithley import KeithleyParser
from .generic_csv import GenericCSVParser

# Registry of available parsers
# Order matters for auto-detection: specific parsers first, generic last
PARSERS = {
    # Data Acquisition / Dataloggers
    'dewesoft': DewesoftParser,
    'keysight': KeysightParser,
    'keysight_34970a': KeysightParser,
    'fluke': FlukeParser,
    'hioki': HiokiParser,

    # Oscilloscopes
    'tektronix': TektronixParser,
    'rigol': RigolParser,
    'yokogawa': YokogawaParser,

    # Source Meters / DMMs
    'keithley': KeithleyParser,

    # Generic (fallback)
    'csv': GenericCSVParser,
}


def get_parser(name: str) -> type:
    """Returns the parser class by name."""
    name_lower = name.lower()
    if name_lower not in PARSERS:
        available = ', '.join(PARSERS.keys())
        raise ValueError(f"Parser '{name}' not found. Available: {available}")
    return PARSERS[name_lower]


def list_parsers() -> list:
    """Lists all available parsers."""
    return list(PARSERS.keys())


__all__ = [
    'BaseParser',
    'DewesoftParser',
    'KeysightParser',
    'TektronixParser',
    'RigolParser',
    'FlukeParser',
    'HiokiParser',
    'YokogawaParser',
    'KeithleyParser',
    'GenericCSVParser',
    'get_parser',
    'list_parsers',
    'PARSERS',
]
