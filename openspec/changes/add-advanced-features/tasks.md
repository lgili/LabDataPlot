# Implementation Tasks

## 1. Analysis Capabilities

### 1.1 Statistical Analysis
- [ ] 1.1.1 Create `analysis.py` module with `Statistics` class
- [ ] 1.1.2 Implement `stats()` method returning dict with min, max, mean, std, rms, peak_to_peak
- [ ] 1.1.3 Add `stats_table()` method for formatted DataFrame output
- [ ] 1.1.4 Add `describe_channel(channel)` for detailed single-channel analysis
- [ ] 1.1.5 Integrate with DataLoader via `loader.stats()` property
- [ ] 1.1.6 Write unit tests for statistical functions

### 1.2 Anomaly Detection
- [ ] 1.2.1 Implement `detect_spikes(channel, threshold)` method
- [ ] 1.2.2 Implement `detect_drops(channel, threshold)` method
- [ ] 1.2.3 Implement `detect_outliers(channel, method='zscore|iqr')` method
- [ ] 1.2.4 Implement `detect_flatlines(channel, duration)` method
- [ ] 1.2.5 Add `anomalies` property returning all detected issues
- [ ] 1.2.6 Write unit tests for anomaly detection

### 1.3 FFT/Frequency Analysis
- [ ] 1.3.1 Implement `fft(channel)` returning frequency and magnitude arrays
- [ ] 1.3.2 Implement `dominant_frequency(channel)` returning top N frequencies
- [ ] 1.3.3 Implement `power_spectrum(channel)` for power spectral density
- [ ] 1.3.4 Add `plot_fft(channel)` to Plotter class
- [ ] 1.3.5 Write unit tests for FFT functions

### 1.4 Correlation Analysis
- [ ] 1.4.1 Implement `correlation_matrix(channels)` returning correlation DataFrame
- [ ] 1.4.2 Implement `cross_correlation(ch1, ch2, lag)` for time-shifted correlation
- [ ] 1.4.3 Add `plot_correlation_matrix()` to Plotter class
- [ ] 1.4.4 Write unit tests for correlation functions

## 2. Visualization Enhancements

### 2.1 Interactive Plots (Plotly)
- [ ] 2.1.1 Create `interactive.py` module with `InteractivePlotter` class
- [ ] 2.1.2 Implement `iplot(channels)` for interactive line plots
- [ ] 2.1.3 Implement `isubplots(channels)` for interactive subplots
- [ ] 2.1.4 Implement `iheatmap(channels)` for interactive heatmap
- [ ] 2.1.5 Add hover tooltips with timestamp and value
- [ ] 2.1.6 Add range slider for time selection
- [ ] 2.1.7 Add export to HTML functionality
- [ ] 2.1.8 Write unit tests for interactive plots

### 2.2 Annotations
- [ ] 2.2.1 Implement `annotate_minmax(channel)` to mark min/max on plots
- [ ] 2.2.2 Implement `annotate_threshold(value, label)` for horizontal lines
- [ ] 2.2.3 Implement `annotate_region(start, end, label)` for time regions
- [ ] 2.2.4 Implement `annotate_events(timestamps, labels)` for vertical markers
- [ ] 2.2.5 Write unit tests for annotations

### 2.3 Multiple Y-Axes
- [ ] 2.3.1 Implement `plot_dual_axis(ch1, ch2)` with left/right Y-axes
- [ ] 2.3.2 Implement `plot_multi_axis(channels, axes_config)` for N axes
- [ ] 2.3.3 Add automatic scaling per axis
- [ ] 2.3.4 Add legend with axis association
- [ ] 2.3.5 Write unit tests for multi-axis plots

### 2.4 Scatter/Correlation Plots
- [ ] 2.4.1 Implement `scatter(ch_x, ch_y)` for X-Y scatter plot
- [ ] 2.4.2 Implement `scatter_matrix(channels)` for pairwise scatter
- [ ] 2.4.3 Add trend line option (linear, polynomial)
- [ ] 2.4.4 Add R² display on scatter plots
- [ ] 2.4.5 Write unit tests for scatter plots

### 2.5 Statistical Overlays
- [ ] 2.5.1 Implement `plot_with_mean(channel)` showing mean line
- [ ] 2.5.2 Implement `plot_with_std_bands(channel, n_sigma)` showing ±nσ bands
- [ ] 2.5.3 Implement `plot_with_envelope(channel)` showing min/max envelope
- [ ] 2.5.4 Implement `plot_with_moving_average(channel, window)` overlay
- [ ] 2.5.5 Write unit tests for statistical overlays

## 3. Data Processing

### 3.1 Digital Filters
- [ ] 3.1.1 Create `processing.py` module with `Filters` class
- [ ] 3.1.2 Implement `lowpass(channel, cutoff_freq, order)` Butterworth filter
- [ ] 3.1.3 Implement `highpass(channel, cutoff_freq, order)` Butterworth filter
- [ ] 3.1.4 Implement `bandpass(channel, low_freq, high_freq, order)` filter
- [ ] 3.1.5 Implement `moving_average(channel, window_size)` filter
- [ ] 3.1.6 Implement `median_filter(channel, window_size)` for spike removal
- [ ] 3.1.7 Add `apply_filter(loader, filter_func)` returning new DataLoader
- [ ] 3.1.8 Write unit tests for filters

### 3.2 Resampling
- [ ] 3.2.1 Implement `resample(new_rate)` for changing sample rate
- [ ] 3.2.2 Implement `downsample(factor)` for reducing data points
- [ ] 3.2.3 Implement `upsample(factor, method='linear|cubic')` for interpolation
- [ ] 3.2.4 Implement `decimate(factor)` with anti-aliasing filter
- [ ] 3.2.5 Write unit tests for resampling

### 3.3 Time Operations
- [ ] 3.3.1 Implement `trim(start_time, end_time)` for time-based cropping
- [ ] 3.3.2 Implement `trim_index(start_idx, end_idx)` for index-based cropping
- [ ] 3.3.3 Implement `split(time_points)` returning list of DataLoaders
- [ ] 3.3.4 Implement `align_to_zero()` shifting time to start at 0
- [ ] 3.3.5 Write unit tests for time operations

### 3.4 File Merging
- [ ] 3.4.1 Implement `merge(*loaders)` concatenating data vertically
- [ ] 3.4.2 Implement `join(*loaders, on='time')` for time-aligned merge
- [ ] 3.4.3 Implement `append(loader)` adding data to existing loader
- [ ] 3.4.4 Handle column name conflicts with suffixes
- [ ] 3.4.5 Write unit tests for merging

### 3.5 Channel Math
- [ ] 3.5.1 Implement `add_channel(name, formula)` for calculated channels
- [ ] 3.5.2 Support operators: +, -, *, /, ** between channels
- [ ] 3.5.3 Implement `diff(channel)` for derivative calculation
- [ ] 3.5.4 Implement `integrate(channel)` for cumulative sum
- [ ] 3.5.5 Implement `scale(channel, factor, offset)` for linear transform
- [ ] 3.5.6 Write unit tests for channel math

## 4. Export & Reporting

### 4.1 PDF Report Generation
- [ ] 4.1.1 Create `export.py` module with `ReportGenerator` class
- [ ] 4.1.2 Implement `generate_pdf(filename, config)` method
- [ ] 4.1.3 Add title page with file info and acquisition date
- [ ] 4.1.4 Add statistics table section
- [ ] 4.1.5 Add configurable plot sections
- [ ] 4.1.6 Add anomaly summary section
- [ ] 4.1.7 Support custom templates
- [ ] 4.1.8 Write unit tests for PDF generation

### 4.2 Excel Export
- [ ] 4.2.1 Implement `to_excel(filename, include_stats, include_charts)` method
- [ ] 4.2.2 Add data sheet with formatted columns
- [ ] 4.2.3 Add statistics sheet with summary tables
- [ ] 4.2.4 Add embedded charts (line, scatter)
- [ ] 4.2.5 Add conditional formatting for anomalies
- [ ] 4.2.6 Write unit tests for Excel export

### 4.3 Batch Plot Export
- [ ] 4.3.1 Implement `save_all(directory, format, dpi)` method
- [ ] 4.3.2 Support PNG, PDF, SVG formats
- [ ] 4.3.3 Add naming convention options
- [ ] 4.3.4 Add thumbnail generation option
- [ ] 4.3.5 Write unit tests for batch export

### 4.4 HTML Report
- [ ] 4.4.1 Implement `generate_html(filename, config)` method
- [ ] 4.4.2 Embed interactive Plotly charts
- [ ] 4.4.3 Add responsive layout
- [ ] 4.4.4 Add dark/light theme support
- [ ] 4.4.5 Write unit tests for HTML generation

## 5. CLI Interface

### 5.1 Core CLI
- [ ] 5.1.1 Create `cli.py` module with Click framework
- [ ] 5.1.2 Implement `labdataplot info <file>` showing file info
- [ ] 5.1.3 Implement `labdataplot list-channels <file>` showing available channels
- [ ] 5.1.4 Implement `labdataplot stats <file> [--channels]` showing statistics
- [ ] 5.1.5 Add `--format json|table|csv` output option
- [ ] 5.1.6 Write unit tests for info commands

### 5.2 Plot Commands
- [ ] 5.2.1 Implement `labdataplot plot <file> --channels CH1,CH2 --output plot.png`
- [ ] 5.2.2 Implement `labdataplot quick <file> --n 10` for quick view
- [ ] 5.2.3 Implement `labdataplot heatmap <file> --output heatmap.png`
- [ ] 5.2.4 Add `--title`, `--xlabel`, `--ylabel` options
- [ ] 5.2.5 Add `--figsize WxH` option
- [ ] 5.2.6 Add `--interactive` flag for Plotly output
- [ ] 5.2.7 Write unit tests for plot commands

### 5.3 Analysis Commands
- [ ] 5.3.1 Implement `labdataplot analyze <file> --channels CH1` for full analysis
- [ ] 5.3.2 Implement `labdataplot fft <file> --channel CH1 --output fft.png`
- [ ] 5.3.3 Implement `labdataplot anomalies <file>` detecting issues
- [ ] 5.3.4 Write unit tests for analysis commands

### 5.4 Export Commands
- [ ] 5.4.1 Implement `labdataplot export <file> --format xlsx|pdf|html`
- [ ] 5.4.2 Implement `labdataplot report <file> --template default`
- [ ] 5.4.3 Add `--output` directory option
- [ ] 5.4.4 Write unit tests for export commands

### 5.5 Processing Commands
- [ ] 5.5.1 Implement `labdataplot filter <file> --type lowpass --cutoff 100`
- [ ] 5.5.2 Implement `labdataplot resample <file> --rate 1000`
- [ ] 5.5.3 Implement `labdataplot trim <file> --start 0 --end 100`
- [ ] 5.5.4 Implement `labdataplot merge <file1> <file2> --output merged.csv`
- [ ] 5.5.5 Write unit tests for processing commands

## 6. Documentation & Testing

### 6.1 Documentation
- [ ] 6.1.1 Update README.md with new features
- [ ] 6.1.2 Update docs/getting_started.md
- [ ] 6.1.3 Create docs/analysis.md
- [ ] 6.1.4 Create docs/visualization.md
- [ ] 6.1.5 Create docs/processing.md
- [ ] 6.1.6 Create docs/export.md
- [ ] 6.1.7 Create docs/cli.md
- [ ] 6.1.8 Add usage examples for each feature

### 6.2 Testing
- [ ] 6.2.1 Create test fixtures with sample data
- [ ] 6.2.2 Achieve >80% code coverage
- [ ] 6.2.3 Add integration tests
- [ ] 6.2.4 Add CLI tests with Click testing utilities

### 6.3 Dependencies
- [ ] 6.3.1 Update pyproject.toml with optional dependencies
- [ ] 6.3.2 Create extras: `[interactive]`, `[analysis]`, `[export]`, `[cli]`, `[all]`
- [ ] 6.3.3 Document installation options in README
