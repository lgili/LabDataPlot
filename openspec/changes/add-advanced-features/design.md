# Design Document: Advanced Features

## Context

LabDataPlot is a Python library for reading and plotting laboratory measurement data. The current implementation provides basic loading and plotting capabilities. This design document covers the architecture for adding advanced analysis, visualization, processing, export, and CLI features.

### Stakeholders
- Laboratory engineers analyzing test data
- Quality engineers generating reports
- Automation scripts processing batch data

### Constraints
- Must maintain backward compatibility with existing API
- Minimal required dependencies (heavy deps should be optional)
- Support Python 3.10+
- Performance: handle files with 1M+ data points

## Goals / Non-Goals

### Goals
- Provide comprehensive statistical analysis without leaving Python
- Enable interactive data exploration with Plotly
- Allow signal processing (filters, resampling) without external tools
- Generate professional reports (PDF, Excel, HTML)
- Enable automation via CLI

### Non-Goals
- Real-time data acquisition
- Database storage
- Web-based dashboard (out of scope for v1)
- Machine learning / predictive analytics

## Architecture

### Module Structure

```
labdataplot/
├── __init__.py           # Public API
├── loader.py             # DataLoader (existing)
├── plotter.py            # Plotter (existing + enhancements)
├── analysis/
│   ├── __init__.py       # Analysis exports
│   ├── statistics.py     # Statistical functions
│   ├── anomaly.py        # Anomaly detection
│   ├── fft.py            # Frequency analysis
│   └── correlation.py    # Correlation analysis
├── processing/
│   ├── __init__.py       # Processing exports
│   ├── filters.py        # Digital filters
│   ├── resample.py       # Resampling functions
│   ├── time_ops.py       # Trim, split, align
│   ├── merge.py          # File merging
│   └── math.py           # Channel math operations
├── visualization/
│   ├── __init__.py       # Visualization exports
│   ├── interactive.py    # Plotly-based plots
│   ├── annotations.py    # Plot annotations
│   ├── multiaxis.py      # Multi Y-axis support
│   └── scatter.py        # Scatter/correlation plots
├── export/
│   ├── __init__.py       # Export exports
│   ├── pdf.py            # PDF report generation
│   ├── excel.py          # Excel export
│   ├── html.py           # HTML report generation
│   └── batch.py          # Batch plot export
└── cli/
    ├── __init__.py       # CLI entry point
    ├── info.py           # Info commands
    ├── plot.py           # Plot commands
    ├── analyze.py        # Analysis commands
    ├── process.py        # Processing commands
    └── export.py         # Export commands
```

### Class Diagram

```
┌─────────────┐     ┌─────────────┐
│ DataLoader  │────>│  DataInfo   │
└─────────────┘     └─────────────┘
       │
       │ has-a
       ▼
┌─────────────┐     ┌─────────────┐
│  Analyzer   │────>│  Statistics │
└─────────────┘     │  Anomalies  │
       │            │  FFT        │
       │            │  Correlation│
       │            └─────────────┘
       │
┌─────────────┐
│  Processor  │────> filters, resample, trim, merge, math
└─────────────┘
       │
┌─────────────┐     ┌─────────────────┐
│   Plotter   │────>│ InteractivePlot │ (Plotly)
└─────────────┘     └─────────────────┘
       │
┌─────────────┐
│  Exporter   │────> PDF, Excel, HTML, Batch
└─────────────┘
```

## Decisions

### Decision 1: Lazy Loading of Optional Dependencies
**What**: Optional dependencies (plotly, scipy, reportlab) are imported only when needed.
**Why**: Keeps base installation lightweight. Users only install what they need.
**How**:
```python
def iplot(self, channels):
    try:
        import plotly.graph_objects as go
    except ImportError:
        raise ImportError("Install plotly: pip install labdataplot[interactive]")
```

### Decision 2: Fluent API for Processing
**What**: Processing methods return new DataLoader instances, enabling chaining.
**Why**: Functional style, immutable data, easy to compose operations.
**How**:
```python
loader = DataLoader('file.xlsx')
processed = (loader
    .filter(lowpass(cutoff=100))
    .resample(rate=1000)
    .trim(start=0, end=60))
```

### Decision 3: Analysis as Mixin
**What**: Add analysis methods directly to DataLoader via mixin class.
**Why**: Convenient access without creating separate objects.
**How**:
```python
class AnalysisMixin:
    def stats(self, channels=None): ...
    def detect_anomalies(self): ...
    def fft(self, channel): ...

class DataLoader(AnalysisMixin):
    ...
```

### Decision 4: Click for CLI
**What**: Use Click library for CLI implementation.
**Why**: Well-documented, decorator-based, supports subcommands.
**Alternative**: argparse (stdlib but verbose), typer (requires type hints everywhere)

### Decision 5: Jinja2 for Report Templates
**What**: Use Jinja2 templates for PDF/HTML report generation.
**Why**: Flexible, widely used, separates content from presentation.
**How**: Templates stored in `labdataplot/templates/`

## Risks / Trade-offs

### Risk 1: Dependency Bloat
**Risk**: Too many optional dependencies confuse users
**Mitigation**:
- Clear extras groups: `[interactive]`, `[analysis]`, `[export]`, `[cli]`, `[all]`
- Document which features require which extras
- Core features work with base install

### Risk 2: Performance with Large Files
**Risk**: FFT, filtering on 1M+ points may be slow
**Mitigation**:
- Use numpy vectorized operations
- Optional chunked processing for very large files
- Progress bars for long operations

### Risk 3: API Surface Growth
**Risk**: Too many methods make API hard to learn
**Mitigation**:
- Group related methods in sub-objects: `loader.analysis.stats()`, `loader.process.filter()`
- Alternatively, keep flat but use clear naming prefixes
- Comprehensive documentation with examples

### Trade-off: Mixin vs Composition
**Chosen**: Mixin approach for analysis (methods on DataLoader)
**Alternative**: Composition (`Analyzer(loader).stats()`)
**Rationale**: Mixin is more convenient for interactive use, which is primary use case

## API Examples

### Analysis
```python
from labdataplot import DataLoader

loader = DataLoader('data.xlsx')

# Statistics
stats = loader.stats()  # All channels
stats = loader.stats(['CH1', 'CH2'])  # Specific channels
# Returns: {'CH1': {'min': 0.1, 'max': 5.2, 'mean': 2.3, 'std': 0.5, 'rms': 2.4}, ...}

# Anomaly detection
anomalies = loader.detect_anomalies(threshold=3.0)
# Returns: [{'channel': 'CH1', 'type': 'spike', 'index': 1234, 'value': 15.2}, ...]

# FFT
freq, magnitude = loader.fft('CH1')
dominant = loader.dominant_frequencies('CH1', n=5)

# Correlation
corr_matrix = loader.correlation(['CH1', 'CH2', 'CH3'])
```

### Processing
```python
from labdataplot import DataLoader
from labdataplot.processing import lowpass, highpass, moving_average

loader = DataLoader('data.xlsx')

# Filtering
filtered = loader.apply_filter('CH1', lowpass(cutoff=100, order=4))
filtered = loader.apply_filter('CH1', moving_average(window=10))

# Resampling
resampled = loader.resample(new_rate=1000)
downsampled = loader.downsample(factor=10)

# Time operations
trimmed = loader.trim(start_time=10, end_time=60)
segments = loader.split(time_points=[30, 60, 90])

# Merging
from labdataplot import merge
combined = merge(loader1, loader2, loader3)

# Channel math
loader.add_channel('Power', 'Voltage * Current')
loader.add_channel('Delta_T', 'T2 - T1')
```

### Visualization
```python
from labdataplot import DataLoader, Plotter

loader = DataLoader('data.xlsx')
plotter = Plotter(loader)

# Interactive plot (Plotly)
plotter.iplot(['CH1', 'CH2'])  # Opens in browser

# Multi-axis
plotter.plot_dual_axis('Voltage', 'Current',
    left_label='Voltage (V)', right_label='Current (A)')

# Scatter with trend
plotter.scatter('CH1', 'CH2', trend='linear', show_r2=True)

# Annotated plot
plotter.plot('CH1')
plotter.annotate_minmax('CH1')
plotter.annotate_threshold(3.3, label='Limit')
plotter.show()

# Statistical overlay
plotter.plot_with_std_bands('CH1', n_sigma=2)
```

### Export
```python
from labdataplot import DataLoader
from labdataplot.export import ReportGenerator

loader = DataLoader('data.xlsx')

# PDF Report
report = ReportGenerator(loader)
report.add_title_page()
report.add_statistics_table()
report.add_plot('CH1', 'CH2')
report.add_anomaly_summary()
report.save('report.pdf')

# Excel with charts
loader.to_excel('output.xlsx', include_stats=True, include_charts=True)

# HTML interactive report
loader.to_html('report.html', interactive=True)

# Batch export
plotter.save_all('plots/', format='png', dpi=300)
```

### CLI
```bash
# Info
labdataplot info data.xlsx
labdataplot list-channels data.xlsx
labdataplot stats data.xlsx --channels CH1,CH2 --format table

# Plot
labdataplot plot data.xlsx --channels CH1,CH2 --output plot.png
labdataplot plot data.xlsx --channels CH1 --interactive
labdataplot quick data.xlsx --n 10 --output quick.png
labdataplot heatmap data.xlsx --output heatmap.png

# Analysis
labdataplot analyze data.xlsx --channel CH1
labdataplot fft data.xlsx --channel CH1 --output fft.png
labdataplot anomalies data.xlsx --threshold 3.0

# Processing
labdataplot filter data.xlsx --channel CH1 --type lowpass --cutoff 100 --output filtered.csv
labdataplot resample data.xlsx --rate 1000 --output resampled.csv
labdataplot trim data.xlsx --start 10 --end 60 --output trimmed.csv
labdataplot merge file1.xlsx file2.xlsx --output merged.csv

# Export
labdataplot export data.xlsx --format pdf --output report.pdf
labdataplot export data.xlsx --format xlsx --output data_with_stats.xlsx
labdataplot export data.xlsx --format html --output report.html
```

## Migration Plan

### Phase 1: Analysis (v0.2.0)
- Add `analysis/` module
- Integrate stats, anomaly, FFT, correlation
- Update documentation

### Phase 2: Processing (v0.3.0)
- Add `processing/` module
- Implement filters, resample, trim, merge, math
- Update documentation

### Phase 3: Visualization (v0.4.0)
- Add `visualization/` module
- Implement interactive plots, annotations, multi-axis, scatter
- Update documentation

### Phase 4: Export (v0.5.0)
- Add `export/` module
- Implement PDF, Excel, HTML, batch export
- Update documentation

### Phase 5: CLI (v0.6.0)
- Add `cli/` module
- Implement all CLI commands
- Update documentation

### Phase 6: Polish (v1.0.0)
- Complete test coverage
- Performance optimization
- Final documentation review
- Stable API

## Open Questions

1. **Should processing return new DataLoader or modify in place?**
   - Leaning toward new instance (immutable) for safety
   - In-place could be offered as `inplace=True` parameter

2. **How to handle very large files (>1GB)?**
   - Chunked reading?
   - Memory-mapped files?
   - Dask integration?

3. **Should interactive plots open browser automatically or return figure?**
   - Default: return figure, let user call `.show()`
   - Option: `auto_show=True` parameter

4. **Report template customization?**
   - Allow users to provide custom Jinja2 templates?
   - Or fixed templates with configuration options?
