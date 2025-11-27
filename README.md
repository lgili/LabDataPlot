# LabDataPlot

<p align="center">
  <strong>A flexible Python library for reading and plotting data from laboratory measurement equipment</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/labdataplot/"><img src="https://img.shields.io/pypi/v/labdataplot.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/labdataplot/"><img src="https://img.shields.io/pypi/pyversions/labdataplot.svg" alt="Python versions"></a>
  <a href="https://github.com/yourusername/labdataplot/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

---

**LabDataPlot** simplifies the process of loading, analyzing, and visualizing data exported from laboratory instruments. Stop wrestling with different file formats and focus on your data.

## Features

- **Automatic format detection** - Just pass the file, the library figures out the format
- **Multiple equipment support** - Keysight, Dewesoft, and easily extensible for more
- **Simple plotting API** - Clean wrapper around matplotlib for quick visualizations
- **Direct data access** - Full pandas DataFrame access for custom analysis
- **Time-aware** - Automatic detection and parsing of timestamp columns
- **Metadata extraction** - Access acquisition date, channel info, units, and more

## Supported Equipment

| Equipment | Parser Name | File Type |
|-----------|-------------|-----------|
| Keysight 34970A/34972A | `keysight` | Excel (.xlsx) |
| Dewesoft Datalogger | `dewesoft` | Excel (.xlsx) |
| *More coming soon...* | | |

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
from labdataplot import DataLoader

# Auto-detect format
loader = DataLoader('data.xlsx')

# Or specify format explicitly
loader = DataLoader('data.xlsx', format='keysight')

# Access data
df = loader.data              # Full pandas DataFrame
time = loader.time            # Time column (if available)
cols = loader.columns         # List of data columns
channel = loader['ch_01']     # Direct column access

# Find channels by pattern
slot1 = loader.get_channel(r'^10')  # Channels starting with "10"
```

### Plotting

```python
from labdataplot import DataLoader, Plotter

loader = DataLoader('data.xlsx')
plotter = Plotter(loader)

# Single channel
plotter.plot('101 (VDC)', title='Channel 101', ylabel='Voltage (V)')

# Multiple channels
plotter.plot(['101 (VDC)', '102 (VDC)', '103 (VDC)'])

# Subplots - one per channel
plotter.subplots(['ch1', 'ch2', 'ch3', 'ch4'], rows=2, cols=2)

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
loader1 = DataLoader('before_test.xlsx')
loader2 = DataLoader('after_test.xlsx')

plotter = Plotter(loader1)
plotter.compare(
    loader2,
    column='ch_01',
    labels=['Before', 'After'],
    title='Test Comparison'
)
plotter.show()
```

## Examples

### Simple Line Plot
```python
plotter.plot(
    ['101 (VDC)', '102 (VDC)'],
    title='Voltage Measurement',
    ylabel='Voltage (V)',
    xlabel='Time'
)
```
![Simple Plot](labdataplot/docs/img_simple_plot.png)

### Subplots
```python
plotter.subplots(
    ['101 (VDC)', '201 (VDC)', '301 (VDC)'],
    rows=3,
    title='One Channel per Slot'
)
```
![Subplots](labdataplot/docs/img_subplots.png)

### Heatmap
```python
plotter.heatmap(
    columns=loader.columns[:15],
    title='First 15 Channels'
)
```
![Heatmap](labdataplot/docs/img_heatmap.png)

## Adding Support for New Equipment

LabDataPlot is designed to be easily extensible. To add support for a new equipment:

1. Create a new parser in `labdataplot/parsers/`
2. Inherit from `BaseParser`
3. Implement `detect()` and `parse()` methods
4. Register in `parsers/__init__.py`

```python
from labdataplot.parsers.base import BaseParser, DataInfo

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

See the [documentation](labdataplot/docs/adding_parsers.md) for detailed instructions.

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

Full documentation is available in the [docs folder](labdataplot/docs/):

- [Getting Started](labdataplot/docs/getting_started.md)
- [DataLoader API](labdataplot/docs/api_dataloader.md)
- [Plotter API](labdataplot/docs/api_plotter.md)
- [Adding New Parsers](labdataplot/docs/adding_parsers.md)
- [Examples](labdataplot/docs/examples.md)

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
git clone https://github.com/yourusername/labdataplot.git
cd labdataplot

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black labdataplot
ruff check labdataplot
```

## Roadmap

- [ ] Support for more equipment (Tektronix, Yokogawa, NI DAQ, etc.)
- [ ] CSV file support
- [ ] Interactive plots with Plotly
- [ ] Data export functionality
- [ ] Report generation
- [ ] CLI interface

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pandas](https://pandas.pydata.org/) and [matplotlib](https://matplotlib.org/)
- Inspired by the need to quickly visualize test data from various lab equipment
