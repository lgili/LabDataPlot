# DataLoader API

The `DataLoader` class is responsible for loading and parsing data files.

## Constructor

```python
DataLoader(filepath: str, format: str | None = None)
```

**Parameters:**
- `filepath`: Path to the Excel file
- `format`: Optional parser name. If not provided, auto-detects the format

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `ValueError`: If format can't be detected or is invalid

**Example:**
```python
# Auto-detect
loader = DataLoader('data.xlsx')

# Explicit format
loader = DataLoader('data.xlsx', format='keysight')
```

## Properties

### `data`

Returns the full pandas DataFrame with all data.

```python
df = loader.data
print(df.shape)  # (100, 62)
print(df.dtypes)
```

### `info`

Returns a `DataInfo` object with metadata about the file.

```python
info = loader.info
print(info.equipment)        # 'Keysight 34970A'
print(info.acquisition_date) # '2025-11-25 17:37:50'
print(info.channels)         # List of channel names
print(info.time_column)      # 'Time' or None
print(info.units)            # {'101 (VDC)': 'VDC', ...}
```

### `columns`

Returns list of data column names (excluding time column).

```python
cols = loader.columns
print(cols[:5])  # ['101 (VDC)', '102 (VDC)', ...]
```

### `time`

Returns the time column as pandas Series, or `None` if no time column exists.

```python
if loader.time is not None:
    print(f"Time range: {loader.time.min()} to {loader.time.max()}")
```

### `filepath`

Returns the Path object of the loaded file.

```python
print(loader.filepath.name)  # 'data.xlsx'
print(loader.filepath.stem)  # 'data'
```

## Methods

### `head(n=5)`

Shows the first n rows of data.

```python
print(loader.head(10))
```

### `describe()`

Returns descriptive statistics of all numeric columns.

```python
stats = loader.describe()
print(stats)
```

### `get_channel(pattern)`

Finds columns matching a regex pattern.

```python
# Find all channels starting with "10"
slot1 = loader.get_channel(r'^10')
# ['101 (VDC)', '102 (VDC)', ..., '120 (VDC)']

# Find all channels with "VDC"
voltage = loader.get_channel(r'VDC')

# Find channel 01 (in Dewesoft format)
ch01 = loader.get_channel(r'_01$')
```

### `__getitem__(key)`

Direct column access using bracket notation.

```python
channel_data = loader['101 (VDC)']
# Same as:
channel_data = loader.data['101 (VDC)']
```

## DataInfo Object

The `DataInfo` dataclass contains file metadata:

| Attribute | Type | Description |
|-----------|------|-------------|
| `filename` | str | Original filename |
| `equipment` | str | Equipment name |
| `acquisition_date` | str | When data was acquired |
| `channels` | list | List of channel names |
| `time_column` | str | Name of time column |
| `sample_rate` | float | Sample rate (if known) |
| `units` | dict | Column -> unit mapping |
| `metadata` | dict | Additional metadata |

## Available Parsers

List all available parsers:

```python
from labdataplot import list_parsers

print(list_parsers())
# ['dewesoft', 'keysight', 'keysight_34970a']
```

Get a specific parser class:

```python
from labdataplot import get_parser

KeysightParser = get_parser('keysight')
```
