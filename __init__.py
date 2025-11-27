"""
LabDataPlot - A flexible Python library for reading and plotting data from laboratory equipment.

Supports multiple Excel/CSV file formats from various measurement instruments including
Keysight, Dewesoft, and more.

Basic usage:
    from labdataplot import DataLoader, Plotter

    loader = DataLoader('measurement.xlsx')
    plotter = Plotter(loader)
    plotter.plot(['channel_01', 'channel_02'])
    plotter.show()
"""

from .loader import DataLoader
from .plotter import Plotter
from .parsers import get_parser, list_parsers

__all__ = ['DataLoader', 'Plotter', 'get_parser', 'list_parsers']
__version__ = '0.1.0'
