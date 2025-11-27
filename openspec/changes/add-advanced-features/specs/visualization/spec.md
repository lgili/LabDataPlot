# Visualization Capability

## ADDED Requirements

### Requirement: Interactive Plots with Plotly
The system SHALL provide interactive plots using Plotly with zoom, pan, hover, and export capabilities.

#### Scenario: Create interactive line plot
- **WHEN** user calls `plotter.iplot(['CH1', 'CH2'])`
- **THEN** returns a Plotly Figure object with interactive line traces
- **AND** hover shows timestamp and value for each point
- **AND** legend allows toggling visibility of each channel

#### Scenario: Create interactive subplots
- **WHEN** user calls `plotter.isubplots(['CH1', 'CH2', 'CH3'], rows=3)`
- **THEN** returns Plotly Figure with vertically stacked subplots
- **AND** subplots share x-axis for synchronized zooming

#### Scenario: Create interactive heatmap
- **WHEN** user calls `plotter.iheatmap()`
- **THEN** returns Plotly Figure with heatmap visualization
- **AND** hover shows channel name, time, and value

#### Scenario: Add range slider
- **WHEN** user calls `plotter.iplot(['CH1'], range_slider=True)`
- **THEN** figure includes a range slider below the main plot
- **AND** slider allows selecting time range without zooming

#### Scenario: Export interactive plot to HTML
- **WHEN** user calls `fig.write_html('plot.html')` on returned figure
- **THEN** creates standalone HTML file with embedded JavaScript
- **AND** file can be opened in any browser without Python

#### Scenario: Plotly not installed
- **WHEN** user calls `plotter.iplot()` and Plotly is not installed
- **THEN** raises ImportError with message: "Install plotly: pip install labdataplot[interactive]"

---

### Requirement: Plot Annotations
The system SHALL provide methods to annotate plots with markers, lines, and regions.

#### Scenario: Annotate min/max values
- **WHEN** user calls `plotter.annotate_minmax('CH1')`
- **THEN** adds markers at minimum and maximum points
- **AND** markers include labels showing the value

#### Scenario: Add horizontal threshold line
- **WHEN** user calls `plotter.annotate_threshold(value=3.3, label='Limit')`
- **THEN** adds horizontal dashed line at specified value
- **AND** line includes text label

#### Scenario: Add multiple threshold lines
- **WHEN** user calls `plotter.annotate_threshold([3.0, 3.3, 3.6], labels=['Min', 'Nom', 'Max'])`
- **THEN** adds horizontal lines for each value with corresponding labels

#### Scenario: Highlight time region
- **WHEN** user calls `plotter.annotate_region(start=10, end=20, label='Test Phase')`
- **THEN** adds shaded vertical region between start and end times
- **AND** region includes text label

#### Scenario: Add event markers
- **WHEN** user calls `plotter.annotate_events(times=[5, 15, 25], labels=['Start', 'Mid', 'End'])`
- **THEN** adds vertical lines at specified times
- **AND** each line has its corresponding label

#### Scenario: Annotate anomalies automatically
- **WHEN** user calls `plotter.annotate_anomalies('CH1', threshold=3.0)`
- **THEN** marks all detected spikes and drops on the plot
- **AND** uses different colors for spikes (red) and drops (blue)

---

### Requirement: Multiple Y-Axes
The system SHALL support plots with multiple Y-axes for comparing signals with different scales.

#### Scenario: Create dual Y-axis plot
- **WHEN** user calls `plotter.plot_dual_axis('Voltage', 'Current')`
- **THEN** plots Voltage on left Y-axis and Current on right Y-axis
- **AND** each axis has independent scaling
- **AND** legend indicates which trace belongs to which axis

#### Scenario: Customize dual axis labels
- **WHEN** user calls `plotter.plot_dual_axis('V', 'I', left_label='Voltage (V)', right_label='Current (A)')`
- **THEN** left Y-axis shows "Voltage (V)" label
- **AND** right Y-axis shows "Current (A)" label

#### Scenario: Create multi-axis plot with N axes
- **WHEN** user calls `plotter.plot_multi_axis(['V', 'I', 'T'], positions=['left', 'right', 'right'])`
- **THEN** creates plot with voltage on left, current and temperature on right
- **AND** multiple right axes are offset for visibility

#### Scenario: Auto-scale each axis independently
- **WHEN** user creates multi-axis plot
- **THEN** each Y-axis scales to fit its data range
- **AND** axes do not interfere with each other's scaling

---

### Requirement: Scatter and Correlation Plots
The system SHALL provide scatter plots and correlation visualizations between channels.

#### Scenario: Create XY scatter plot
- **WHEN** user calls `plotter.scatter('CH1', 'CH2')`
- **THEN** creates scatter plot with CH1 on X-axis and CH2 on Y-axis
- **AND** each point represents a simultaneous measurement

#### Scenario: Add trend line to scatter plot
- **WHEN** user calls `plotter.scatter('CH1', 'CH2', trend='linear')`
- **THEN** adds linear regression trend line to the plot
- **AND** displays R² value on the plot

#### Scenario: Add polynomial trend line
- **WHEN** user calls `plotter.scatter('CH1', 'CH2', trend='poly', degree=2)`
- **THEN** adds polynomial trend line of specified degree
- **AND** displays R² value on the plot

#### Scenario: Create scatter matrix
- **WHEN** user calls `plotter.scatter_matrix(['CH1', 'CH2', 'CH3'])`
- **THEN** creates NxN grid of scatter plots for all pairs
- **AND** diagonal shows histogram for each channel

#### Scenario: Plot correlation matrix as heatmap
- **WHEN** user calls `plotter.plot_correlation(['CH1', 'CH2', 'CH3'])`
- **THEN** creates heatmap visualization of correlation matrix
- **AND** color scale ranges from -1 (negative) to +1 (positive)
- **AND** cells display correlation coefficient values

---

### Requirement: Statistical Overlays
The system SHALL provide plot overlays showing statistical information.

#### Scenario: Plot with mean line
- **WHEN** user calls `plotter.plot_with_mean('CH1')`
- **THEN** plots channel data with horizontal mean line overlay
- **AND** mean line is dashed and labeled

#### Scenario: Plot with standard deviation bands
- **WHEN** user calls `plotter.plot_with_std_bands('CH1', n_sigma=2)`
- **THEN** plots channel data with shaded region at mean ± n_sigma*std
- **AND** band is semi-transparent

#### Scenario: Plot with envelope
- **WHEN** user calls `plotter.plot_with_envelope('CH1', window=100)`
- **THEN** plots channel data with rolling min/max envelope
- **AND** envelope is shown as shaded region

#### Scenario: Plot with moving average overlay
- **WHEN** user calls `plotter.plot_with_moving_average('CH1', window=50)`
- **THEN** plots raw data with moving average line overlay
- **AND** moving average line is smooth and different color

#### Scenario: Plot with percentile bands
- **WHEN** user calls `plotter.plot_with_percentiles('CH1', lower=10, upper=90)`
- **THEN** plots channel with shaded region between percentiles
- **AND** percentile values are calculated using rolling window
