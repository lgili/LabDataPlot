# Getting Started

This guide will help you get up and running with DataPlotter.

## Installation

First, ensure you have the required dependencies:

```bash
pip install pandas matplotlib openpyxl
```

Then, add the `labdataplot` folder to your project or Python path.

## Basic Workflow

The typical workflow is:

1. **Load data** using `DataLoader`
2. **Explore** the loaded data
3. **Plot** using `Plotter`

## Step 1: Loading Data

```python
from labdataplot import DataLoader

# The simplest way - auto-detects the format
loader = DataLoader('path/to/your/file.xlsx')
```

The module will automatically detect whether your file is from:
- Dewesoft Datalogger
- Keysight 34970A

If you want to explicitly specify the format:

```python
loader = DataLoader('file.xlsx', format='keysight')
```

## Step 2: Exploring Your Data

Once loaded, you can explore what's available:

```python
# Basic info
print(loader)
# Output:
# DataLoader(
#   file='my_file.xlsx',
#   format='keysight',
#   shape=(100, 62),
#   columns=61
# )

# Detailed metadata
print(loader.info)
# Output:
# DataInfo(
#   equipment='Keysight 34970A',
#   channels=60,
#   time_column='Time',
#   acquisition_date='2025-11-25 17:37:50'
# )

# List available columns
print(loader.columns)
# ['101 (VDC)', '102 (VDC)', '103 (VDC)', ...]

# See first few rows
print(loader.head())
```

## Step 3: Accessing Data

You can access data in several ways:

```python
# Full DataFrame
df = loader.data

# Time column (if available)
time = loader.time

# Single column by name
channel_data = loader['101 (VDC)']

# Find channels by pattern
slot1_channels = loader.get_channel(r'^10')  # Channels starting with "10"
```

## Step 4: Creating Plots

```python
from labdataplot import Plotter

plotter = Plotter(loader)

# Simple plot
plotter.plot('101 (VDC)')

# Multiple channels on same plot
plotter.plot(['101 (VDC)', '102 (VDC)', '103 (VDC)'])

# Show the plots
plotter.show()
```

## Complete Example

```python
from labdataplot import DataLoader, Plotter

# Load
loader = DataLoader('measurement.xlsx')

# Explore
print(f"Loaded {len(loader.columns)} channels")
print(f"Acquisition date: {loader.info.acquisition_date}")
print(f"First 5 channels: {loader.columns[:5]}")

# Plot
plotter = Plotter(loader)
plotter.plot(
    loader.columns[:3],
    title='First 3 Channels',
    ylabel='Voltage (V)'
)
plotter.show()
```

## Next Steps

- Learn more about [DataLoader API](api_dataloader.md)
- Explore [Plotter features](api_plotter.md)
- See more [Examples](examples.md)
