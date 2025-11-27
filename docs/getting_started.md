# Getting Started

This guide will help you get up and running with LabDataPlot.

## Installation

```bash
pip install labdataplot
```

Or install from source:

```bash
pip install pandas matplotlib openpyxl
```

## Supported Equipment

LabDataPlot supports data files from:

### Data Acquisition / Dataloggers
- Keysight 34970A/34972A (Excel)
- Dewesoft Datalogger (Excel)
- Fluke Hydra 2680/2686 (CSV, Excel)
- Hioki LR8400/LR8401/MR8875 (CSV, Excel)

### Oscilloscopes
- Tektronix TDS/MSO/DPO/MDO series (CSV)
- Rigol DS/MSO series (CSV)
- Yokogawa DL/SL series (CSV, Excel)

### Power Analyzers & Source Meters
- Yokogawa WT series (CSV, Excel)
- Keithley 2400/2450 SourceMeter (CSV, Excel)
- Keithley DMM6500/DAQ6510 (CSV, Excel)

### Generic
- Any CSV file with auto-detection

## Basic Workflow

The typical workflow is:

1. **Load data** using `DataLoader`
2. **Explore** the loaded data
3. **Plot** using `Plotter`

## Step 1: Loading Data

```python
from labdataplot import DataLoader, list_parsers

# See all available parsers
print(list_parsers())
# ['dewesoft', 'keysight', 'fluke', 'hioki', 'tektronix', 'rigol', 'yokogawa', 'keithley', 'csv']

# The simplest way - auto-detects the format
loader = DataLoader('path/to/your/file.xlsx')
```

The module will automatically detect your file format based on content.

If you want to explicitly specify the format:

```python
loader = DataLoader('file.csv', format='tektronix')
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
channel_data = loader['CH1']

# Find channels by pattern
voltage_channels = loader.get_channel(r'VDC')  # All channels containing "VDC"
slot1_channels = loader.get_channel(r'^10')    # Channels starting with "10"
```

## Step 4: Creating Plots

```python
from labdataplot import Plotter

plotter = Plotter(loader)

# Simple plot
plotter.plot('CH1')

# Multiple channels on same plot
plotter.plot(['CH1', 'CH2', 'CH3'])

# Show the plots
plotter.show()
```

## Complete Example

```python
from labdataplot import DataLoader, Plotter

# Load
loader = DataLoader('measurement.xlsx')

# Explore
print(f"Equipment: {loader.info.equipment}")
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

## Working with Different Equipment

### Oscilloscope Data (Tektronix, Rigol)

```python
loader = DataLoader('scope_capture.csv')

print(f"Sample rate: {loader.info.sample_rate} Hz")
print(f"Channels: {loader.columns}")

plotter = Plotter(loader)
plotter.plot(['CH1', 'CH2'], title='Oscilloscope Capture')
plotter.show()
```

### Power Analyzer Data (Yokogawa WT, Keithley)

```python
loader = DataLoader('power_measurement.csv', format='keithley')

# Access voltage and current
voltage = loader['Voltage']
current = loader['Current']

plotter = Plotter(loader)
plotter.subplots(['Voltage', 'Current', 'Power'], rows=3)
plotter.show()
```

### Datalogger Data (Keysight, Dewesoft, Fluke, Hioki)

```python
loader = DataLoader('temperature_log.xlsx')

# Find all temperature channels
temp_channels = loader.get_channel(r'Temp|°C')

plotter = Plotter(loader)
plotter.heatmap(columns=temp_channels, title='Temperature Distribution')
plotter.show()
```

## Next Steps

- Learn more about [DataLoader API](api_dataloader.md)
- Explore [Plotter features](api_plotter.md)
- See more [Examples](examples.md)
- Learn how to [Add New Parsers](adding_parsers.md)
