"""
Parsers for different equipment file formats.
"""

from .base import BaseParser
from .dewesoft import DewesoftParser
from .keysight import KeysightParser

# Registry of available parsers
PARSERS = {
    'dewesoft': DewesoftParser,
    'keysight': KeysightParser,
    'keysight_34970a': KeysightParser,
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


__all__ = ['BaseParser', 'DewesoftParser', 'KeysightParser', 'get_parser', 'list_parsers']
