# LabDataPlot

A flexible Python library for reading and plotting data from laboratory measurement equipment.

## Features

- **Automatic format detection**: Just pass the file, the library figures out the format
- **Multiple equipment support**: Dewesoft, Keysight 34970A, and easily extensible
- **Simple plotting API**: Wrapper around matplotlib for quick visualizations
- **Direct data access**: Full pandas DataFrame access for custom analysis

## Installation

```bash
pip install labdataplot
```

## Quick Start

```python
from labdataplot import DataLoader, Plotter

# Load data (format auto-detected)
loader = DataLoader('my_data.xlsx')

# Check what was loaded
print(loader.info)
print(loader.columns)

# Create plots
plotter = Plotter(loader)
plotter.plot(['channel_01', 'channel_02'])
plotter.show()
```

## Documentation

- [Getting Started](getting_started.md) - Basic usage and concepts
- [DataLoader API](api_dataloader.md) - Loading and accessing data
- [Plotter API](api_plotter.md) - Creating visualizations
- [Adding New Parsers](adding_parsers.md) - Extending for new equipment
- [Examples](examples.md) - Common use cases with code

## Supported Formats

| Parser | Equipment | File Characteristics |
|--------|-----------|---------------------|
| `dewesoft` | Dewesoft Datalogger | Sheet "Data" + root sheet, columns PREFIX_NN |
| `keysight` | Keysight 34970A | Header with metadata, columns with units like "101 (VDC)" |

## Basic Examples

### Loading Data

```python
from labdataplot import DataLoader

# Auto-detect format
loader = DataLoader('measurement.xlsx')

# Or specify format explicitly
loader = DataLoader('measurement.xlsx', format='keysight')

# Access data
df = loader.data              # Full DataFrame
time = loader.time            # Time column (if available)
cols = loader.columns         # List of data columns
channel = loader['NN_01']     # Direct column access
```

### Simple Plots

```python
from labdataplot import DataLoader, Plotter

loader = DataLoader('data.xlsx')
plotter = Plotter(loader)

# Single channel
plotter.plot('101 (VDC)', title='Channel 101', ylabel='Voltage (V)')

# Multiple channels
plotter.plot(['101 (VDC)', '102 (VDC)', '103 (VDC)'])

plotter.show()
```

### Subplots

```python
# Vertical stack of plots
plotter.subplots(['ch1', 'ch2', 'ch3'], rows=3)

# Grid layout
plotter.subplots(['ch1', 'ch2', 'ch3', 'ch4'], rows=2, cols=2)

# Quick view of first 10 channels
plotter.quick(10)
```

### Comparing Files

```python
loader1 = DataLoader('test_before.xlsx')
loader2 = DataLoader('test_after.xlsx')

plotter = Plotter(loader1)
plotter.compare(loader2, column='NN_01', labels=['Before', 'After'])
```

## License

MIT License
