# Plotter API

The `Plotter` class provides a simplified interface for creating matplotlib plots.

## Constructor

```python
Plotter(loader: DataLoader, figsize: tuple = (12, 6))
```

**Parameters:**
- `loader`: A DataLoader instance with loaded data
- `figsize`: Default figure size (width, height) in inches

**Example:**
```python
loader = DataLoader('data.xlsx')
plotter = Plotter(loader)

# Custom default size
plotter = Plotter(loader, figsize=(16, 8))
```

## Methods

### `plot()`

Creates a line plot of one or more columns.

```python
plot(
    columns: str | list,
    x: str = None,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    legend: bool = True,
    grid: bool = True,
    figsize: tuple = None,
    **kwargs
) -> tuple[Figure, Axes]
```

**Parameters:**
- `columns`: Column name or list of column names to plot
- `x`: Column to use for X axis (default: time column or index)
- `title`: Plot title
- `xlabel`: X axis label
- `ylabel`: Y axis label
- `legend`: Show legend (default: True)
- `grid`: Show grid (default: True)
- `figsize`: Override default figure size
- `**kwargs`: Passed to matplotlib's `plot()`

**Returns:** Tuple of (Figure, Axes)

**Examples:**
```python
# Single channel
fig, ax = plotter.plot('101 (VDC)')

# Multiple channels
fig, ax = plotter.plot(['101 (VDC)', '102 (VDC)', '103 (VDC)'])

# With customization
fig, ax = plotter.plot(
    '101 (VDC)',
    title='Channel 101 Voltage',
    ylabel='Voltage (V)',
    xlabel='Time',
    color='red',
    linewidth=2
)
```

### `subplots()`

Creates multiple subplots, one per column.

```python
subplots(
    columns: list,
    rows: int = None,
    cols: int = 1,
    x: str = None,
    sharex: bool = True,
    sharey: bool = False,
    title: str = None,
    figsize: tuple = None,
    **kwargs
) -> tuple[Figure, ndarray]
```

**Parameters:**
- `columns`: List of column names to plot
- `rows`: Number of rows (auto-calculated if None)
- `cols`: Number of columns (default: 1)
- `x`: Column for X axis
- `sharex`: Share X axis between subplots
- `sharey`: Share Y axis between subplots
- `title`: Overall figure title
- `figsize`: Figure size (auto-calculated if None)
- `**kwargs`: Passed to matplotlib's `plot()`

**Returns:** Tuple of (Figure, array of Axes)

**Examples:**
```python
# Vertical stack
fig, axes = plotter.subplots(['ch1', 'ch2', 'ch3'])

# Explicit rows
fig, axes = plotter.subplots(['ch1', 'ch2', 'ch3', 'ch4'], rows=4)

# 2x2 grid
fig, axes = plotter.subplots(['ch1', 'ch2', 'ch3', 'ch4'], rows=2, cols=2)

# With shared Y axis
fig, axes = plotter.subplots(['ch1', 'ch2'], sharey=True)
```

### `compare()`

Compares the same column across multiple files.

```python
compare(
    *loaders: DataLoader,
    column: str,
    labels: list = None,
    title: str = None,
    figsize: tuple = None,
    **kwargs
) -> tuple[Figure, Axes]
```

**Parameters:**
- `*loaders`: Additional DataLoader instances to compare
- `column`: Column name to compare
- `labels`: Labels for each loader (default: filenames)
- `title`: Plot title
- `figsize`: Figure size
- `**kwargs`: Passed to matplotlib's `plot()`

**Example:**
```python
loader1 = DataLoader('before.xlsx')
loader2 = DataLoader('after.xlsx')
loader3 = DataLoader('final.xlsx')

plotter = Plotter(loader1)
fig, ax = plotter.compare(
    loader2, loader3,
    column='NN_01',
    labels=['Before', 'After', 'Final'],
    title='Channel 01 Comparison'
)
```

### `heatmap()`

Creates a heatmap visualization of multiple channels.

```python
heatmap(
    columns: list = None,
    title: str = None,
    figsize: tuple = None,
    cmap: str = 'RdYlBu_r'
) -> tuple[Figure, Axes]
```

**Parameters:**
- `columns`: Columns to include (default: all)
- `title`: Plot title
- `figsize`: Figure size
- `cmap`: Matplotlib colormap name

**Example:**
```python
# All channels
fig, ax = plotter.heatmap()

# Selected channels
fig, ax = plotter.heatmap(
    columns=loader.columns[:20],
    title='First 20 Channels',
    cmap='viridis'
)
```

### `quick()`

Quick visualization of the first N columns.

```python
quick(n_columns: int = 10) -> tuple[Figure, ndarray]
```

**Example:**
```python
# See first 10 channels
fig, axes = plotter.quick()

# See first 5 channels
fig, axes = plotter.quick(5)
```

### `show()`

Displays all created plots.

```python
plotter.show()
```

### `save()`

Saves the current figure to a file.

```python
save(filename: str, dpi: int = 150, **kwargs)
```

**Example:**
```python
plotter.plot(['ch1', 'ch2'])
plotter.save('my_plot.png', dpi=300)
plotter.save('my_plot.pdf')
```

### `apply_style()`

Applies a matplotlib style.

```python
apply_style(style: str = 'seaborn-v0_8-whitegrid')
```

**Example:**
```python
plotter.apply_style('ggplot')
plotter.plot('ch1')
```

## Customization Tips

### Using matplotlib kwargs

All plot methods accept `**kwargs` that are passed to matplotlib:

```python
# Line style
plotter.plot('ch1', linestyle='--', linewidth=2)

# Colors
plotter.plot('ch1', color='red')
plotter.plot(['ch1', 'ch2'], color=['red', 'blue'])

# Markers
plotter.plot('ch1', marker='o', markersize=3)
```

### Post-plot modifications

Since methods return Figure and Axes, you can customize further:

```python
fig, ax = plotter.plot('ch1')

# Add horizontal line
ax.axhline(y=5, color='r', linestyle='--', label='Threshold')

# Change limits
ax.set_xlim(0, 100)
ax.set_ylim(-1, 15)

# Add annotations
ax.annotate('Peak', xy=(50, 12), xytext=(60, 14),
            arrowprops=dict(arrowstyle='->'))

plotter.show()
```
