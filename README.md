# LabDataPlot

<p align="center">
  <strong>A flexible Python library for reading and plotting data from laboratory measurement equipment</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/labdataplot/"><img src="https://img.shields.io/pypi/v/labdataplot.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/labdataplot/"><img src="https://img.shields.io/pypi/pyversions/labdataplot.svg" alt="Python versions"></a>
  <a href="https://github.com/lgili/LabDataPlot/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

---

**LabDataPlot** simplifies the process of loading, analyzing, and visualizing data exported from laboratory instruments. Stop wrestling with different file formats and focus on your data.

## Features

- **Automatic format detection** - Just pass the file, the library figures out the format
- **Multiple equipment support** - 10+ instruments from major manufacturers
- **Simple plotting API** - Clean wrapper around matplotlib for quick visualizations
- **Direct data access** - Full pandas DataFrame access for custom analysis
- **Time-aware** - Automatic detection and parsing of timestamp columns
- **Metadata extraction** - Access acquisition date, channel info, units, and more

## Supported Equipment

### Data Acquisition / Dataloggers
| Equipment | Parser Name | File Type |
|-----------|-------------|-----------|
| Keysight 34970A/34972A | `keysight` | Excel (.xlsx) |
| Dewesoft Datalogger | `dewesoft` | Excel (.xlsx) |
| Fluke Hydra 2680/2686 | `fluke` | CSV, Excel |
| Hioki LR8400/LR8401/MR8875 | `hioki` | CSV, Excel |

### Oscilloscopes
| Equipment | Parser Name | File Type |
|-----------|-------------|-----------|
| Tektronix TDS/MSO/DPO/MDO | `tektronix` | CSV |
| Rigol DS/MSO series | `rigol` | CSV |
| Yokogawa DL/SL series | `yokogawa` | CSV, Excel |

### Power Analyzers & Source Meters
| Equipment | Parser Name | File Type |
|-----------|-------------|-----------|
| Yokogawa WT series | `yokogawa` | CSV, Excel |
| Keithley 2400/2450 SourceMeter | `keithley` | CSV, Excel |
| Keithley DMM6500/DAQ6510 | `keithley` | CSV, Excel |

### Generic
| Format | Parser Name | Description |
|--------|-------------|-------------|
| CSV | `csv` | Generic CSV with auto-detection |

## Installation

```bash
pip install labdataplot
```

### Requirements

- Python 3.10+
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- openpyxl >= 3.1.0

## Quick Start

### Basic Usage

```python
from labdataplot import DataLoader, Plotter

# Load data (format auto-detected)
loader = DataLoader('measurement.xlsx')

# View file information
print(loader.info)
# DataInfo(
#   equipment='Keysight 34970A',
#   channels=60,
#   time_column='Time',
#   acquisition_date='2025-11-25 17:37:50'
# )

# Create plots
plotter = Plotter(loader)
plotter.plot(['101 (VDC)', '102 (VDC)', '103 (VDC)'])
plotter.show()
```

### Loading Data

```python
from labdataplot import DataLoader, list_parsers

# See all available parsers
print(list_parsers())
# ['dewesoft', 'keysight', 'fluke', 'hioki', 'tektronix', 'rigol', 'yokogawa', 'keithley', 'csv']

# Auto-detect format
loader = DataLoader('data.xlsx')

# Or specify format explicitly
loader = DataLoader('data.csv', format='tektronix')

# Access data
df = loader.data              # Full pandas DataFrame
time = loader.time            # Time column (if available)
cols = loader.columns         # List of data columns
channel = loader['CH1']       # Direct column access

# Find channels by pattern
voltage_channels = loader.get_channel(r'VDC')  # All channels with "VDC"
```

### Plotting

```python
from labdataplot import DataLoader, Plotter

loader = DataLoader('oscilloscope_capture.csv')
plotter = Plotter(loader)

# Single channel
plotter.plot('CH1', title='Channel 1', ylabel='Voltage (V)')

# Multiple channels
plotter.plot(['CH1', 'CH2', 'CH3', 'CH4'])

# Subplots - one per channel
plotter.subplots(['CH1', 'CH2', 'CH3', 'CH4'], rows=2, cols=2)

# Quick view of first N channels
plotter.quick(10)

# Heatmap visualization
plotter.heatmap(title='All Channels Overview')

# Save figure
plotter.save('output.png', dpi=300)

plotter.show()
```

### Comparing Multiple Files

```python
loader1 = DataLoader('before_test.csv')
loader2 = DataLoader('after_test.csv')

plotter = Plotter(loader1)
plotter.compare(
    loader2,
    column='CH1',
    labels=['Before', 'After'],
    title='Test Comparison'
)
plotter.show()
```

## Examples

### Simple Line Plot
```python
plotter.plot(
    ['CH1', 'CH2'],
    title='Oscilloscope Capture',
    ylabel='Voltage (V)',
    xlabel='Time (s)'
)
```
![Simple Plot](docs/img_simple_plot.png)

### Subplots
```python
plotter.subplots(
    ['101 (VDC)', '201 (VDC)', '301 (VDC)'],
    rows=3,
    title='One Channel per Slot'
)
```
![Subplots](docs/img_subplots.png)

### Heatmap
```python
plotter.heatmap(
    columns=loader.columns[:15],
    title='First 15 Channels'
)
```
![Heatmap](docs/img_heatmap.png)

## Adding Support for New Equipment

LabDataPlot is designed to be easily extensible. To add support for new equipment:

1. Create a new parser in `labdataplot/parsers/`
2. Inherit from `BaseParser`
3. Implement `detect()` and `parse()` methods
4. Register in `parsers/__init__.py`

```python
from labdataplot.parsers.base import BaseParser, DataInfo
import pandas as pd

class MyEquipmentParser(BaseParser):
    name = "my_equipment"
    description = "Parser for My Equipment"

    def detect(self, filepath: str) -> bool:
        # Return True if file matches this format
        ...

    def parse(self, filepath: str) -> tuple[pd.DataFrame, DataInfo]:
        # Read and return (DataFrame, DataInfo)
        ...
```

See the [documentation](docs/adding_parsers.md) for detailed instructions.

## API Reference

### DataLoader

| Property/Method | Description |
|-----------------|-------------|
| `data` | Returns pandas DataFrame with all data |
| `info` | Returns DataInfo with metadata |
| `columns` | List of data column names |
| `time` | Time column as Series (if available) |
| `head(n)` | First n rows |
| `describe()` | Statistical summary |
| `get_channel(pattern)` | Find columns matching regex pattern |

### Plotter

| Method | Description |
|--------|-------------|
| `plot(columns, ...)` | Line plot of one or more columns |
| `subplots(columns, rows, cols, ...)` | Multiple subplots |
| `compare(*loaders, column, ...)` | Compare same column across files |
| `heatmap(columns, ...)` | Heatmap visualization |
| `quick(n)` | Quick view of first n columns |
| `save(filename, dpi)` | Save current figure |
| `show()` | Display all plots |

## Documentation

Full documentation is available in the [docs folder](docs/):

- [Getting Started](docs/getting_started.md)
- [DataLoader API](docs/api_dataloader.md)
- [Plotter API](docs/api_plotter.md)
- [Adding New Parsers](docs/adding_parsers.md)
- [Examples](docs/examples.md)

## Contributing

Contributions are welcome! Whether it's:

- Adding support for new equipment
- Bug fixes
- Documentation improvements
- Feature requests

Please feel free to open an issue or submit a pull request.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/lgili/LabDataPlot.git
cd LabDataPlot

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black labdataplot
ruff check labdataplot
```

## Roadmap

- [x] Keysight 34970A datalogger support
- [x] Dewesoft datalogger support
- [x] Tektronix oscilloscope support
- [x] Rigol oscilloscope support
- [x] Yokogawa instruments support
- [x] Keithley SourceMeter support
- [x] Fluke datalogger support
- [x] Hioki datalogger support
- [x] Generic CSV support
- [ ] Interactive plots with Plotly
- [ ] Data export functionality
- [ ] Report generation
- [ ] CLI interface
- [ ] NI DAQ support
- [ ] LeCroy oscilloscope support
- [ ] Rohde & Schwarz support

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pandas](https://pandas.pydata.org/) and [matplotlib](https://matplotlib.org/)
- Inspired by the need to quickly visualize test data from various lab equipment
