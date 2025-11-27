# CLI Capability

## ADDED Requirements

### Requirement: Info Commands
The system SHALL provide CLI commands to display file information and metadata.

#### Scenario: Show file info
- **WHEN** user runs `labdataplot info data.xlsx`
- **THEN** displays:
  - Filename and path
  - Detected equipment type
  - Number of channels and samples
  - Time range (if available)
  - Acquisition date (if available)
  - Sample rate (if available)

#### Scenario: List channels
- **WHEN** user runs `labdataplot list-channels data.xlsx`
- **THEN** displays list of all channel names, one per line

#### Scenario: List channels with units
- **WHEN** user runs `labdataplot list-channels data.xlsx --with-units`
- **THEN** displays channel names with their units: "CH1 (V)", "T1 (°C)"

#### Scenario: Show statistics
- **WHEN** user runs `labdataplot stats data.xlsx`
- **THEN** displays statistics table for all channels
- **AND** shows min, max, mean, std for each

#### Scenario: Show statistics for specific channels
- **WHEN** user runs `labdataplot stats data.xlsx --channels CH1,CH2`
- **THEN** displays statistics only for CH1 and CH2

#### Scenario: Output as JSON
- **WHEN** user runs `labdataplot info data.xlsx --format json`
- **THEN** outputs JSON object with file information
- **AND** suitable for parsing by scripts

#### Scenario: Output as CSV
- **WHEN** user runs `labdataplot stats data.xlsx --format csv`
- **THEN** outputs statistics in CSV format
- **AND** includes header row

---

### Requirement: Plot Commands
The system SHALL provide CLI commands to generate and save plots.

#### Scenario: Create basic plot
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1,CH2 --output plot.png`
- **THEN** creates PNG file with line plot of specified channels

#### Scenario: Create plot with title
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1 --title "Voltage" --output plot.png`
- **THEN** plot includes "Voltage" as title

#### Scenario: Create plot with axis labels
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1 --xlabel "Time (s)" --ylabel "V"`
- **THEN** plot has specified axis labels

#### Scenario: Create plot with custom size
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1 --figsize 12x8 --output plot.png`
- **THEN** creates plot with 12 inches width and 8 inches height

#### Scenario: Create quick view
- **WHEN** user runs `labdataplot quick data.xlsx --n 10 --output quick.png`
- **THEN** creates plot showing first 10 channels

#### Scenario: Create heatmap
- **WHEN** user runs `labdataplot heatmap data.xlsx --output heatmap.png`
- **THEN** creates heatmap visualization of all channels

#### Scenario: Create interactive plot
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1 --interactive`
- **THEN** opens interactive Plotly plot in browser
- **OR** saves as HTML if --output specified

#### Scenario: Create subplots
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1,CH2,CH3 --subplots --rows 3`
- **THEN** creates vertically stacked subplots

#### Scenario: Set time step
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1 --time-step 1.0 --display-unit min`
- **THEN** generates time axis at 1 second intervals, displayed in minutes

---

### Requirement: Analysis Commands
The system SHALL provide CLI commands for data analysis.

#### Scenario: Full channel analysis
- **WHEN** user runs `labdataplot analyze data.xlsx --channel CH1`
- **THEN** displays comprehensive analysis:
  - Statistics (min, max, mean, std, rms)
  - Detected anomalies
  - Dominant frequencies (if FFT available)

#### Scenario: FFT analysis with plot
- **WHEN** user runs `labdataplot fft data.xlsx --channel CH1 --output fft.png`
- **THEN** creates frequency spectrum plot
- **AND** displays dominant frequencies in console

#### Scenario: Detect anomalies
- **WHEN** user runs `labdataplot anomalies data.xlsx`
- **THEN** lists all detected anomalies for all channels
- **AND** groups by channel and type

#### Scenario: Detect anomalies with threshold
- **WHEN** user runs `labdataplot anomalies data.xlsx --threshold 2.5`
- **THEN** uses 2.5 sigma threshold instead of default 3.0

#### Scenario: Correlation analysis
- **WHEN** user runs `labdataplot correlate data.xlsx --channels CH1,CH2,CH3`
- **THEN** displays correlation matrix in table format

---

### Requirement: Processing Commands
The system SHALL provide CLI commands for data processing.

#### Scenario: Apply filter
- **WHEN** user runs `labdataplot filter data.xlsx --type lowpass --cutoff 100 --output filtered.csv`
- **THEN** applies low-pass filter to all channels
- **AND** saves result to CSV file

#### Scenario: Apply filter to specific channel
- **WHEN** user runs `labdataplot filter data.xlsx --channel CH1 --type moving_average --window 10`
- **THEN** applies moving average only to CH1

#### Scenario: Resample data
- **WHEN** user runs `labdataplot resample data.xlsx --rate 1000 --output resampled.csv`
- **THEN** resamples data to 1000 Hz and saves

#### Scenario: Trim data by time
- **WHEN** user runs `labdataplot trim data.xlsx --start 10 --end 60 --output trimmed.csv`
- **THEN** extracts data from 10 to 60 time units

#### Scenario: Merge multiple files
- **WHEN** user runs `labdataplot merge file1.xlsx file2.xlsx file3.xlsx --output merged.csv`
- **THEN** concatenates files and saves result

#### Scenario: Downsample data
- **WHEN** user runs `labdataplot downsample data.xlsx --factor 10 --output downsampled.csv`
- **THEN** reduces sample count by factor of 10

---

### Requirement: Export Commands
The system SHALL provide CLI commands for exporting reports and data.

#### Scenario: Export PDF report
- **WHEN** user runs `labdataplot export data.xlsx --format pdf --output report.pdf`
- **THEN** generates PDF report with default template

#### Scenario: Export Excel with stats
- **WHEN** user runs `labdataplot export data.xlsx --format xlsx --include-stats --output data.xlsx`
- **THEN** creates Excel file with data and statistics sheets

#### Scenario: Export HTML report
- **WHEN** user runs `labdataplot export data.xlsx --format html --interactive --output report.html`
- **THEN** creates HTML report with interactive Plotly charts

#### Scenario: Batch export plots
- **WHEN** user runs `labdataplot export-plots data.xlsx --output-dir plots/ --format png --dpi 300`
- **THEN** creates one PNG per channel in plots/ directory

#### Scenario: Export to CSV
- **WHEN** user runs `labdataplot export data.xlsx --format csv --output data.csv`
- **THEN** exports data to CSV format

---

### Requirement: Global Options
The system SHALL support global options applicable to all commands.

#### Scenario: Specify parser format
- **WHEN** user runs `labdataplot info data.csv --parser tektronix`
- **THEN** uses Tektronix parser instead of auto-detection

#### Scenario: Verbose output
- **WHEN** user runs `labdataplot --verbose plot data.xlsx --channels CH1`
- **THEN** displays additional information during processing

#### Scenario: Quiet mode
- **WHEN** user runs `labdataplot --quiet export data.xlsx --format pdf`
- **THEN** suppresses non-essential output

#### Scenario: Version info
- **WHEN** user runs `labdataplot --version`
- **THEN** displays LabDataPlot version number

#### Scenario: Help
- **WHEN** user runs `labdataplot --help` or `labdataplot plot --help`
- **THEN** displays usage information and available options

---

### Requirement: Error Handling
The system SHALL provide clear error messages for CLI operations.

#### Scenario: File not found
- **WHEN** user runs `labdataplot info nonexistent.xlsx`
- **THEN** displays error: "Error: File not found: nonexistent.xlsx"
- **AND** exits with code 1

#### Scenario: Unknown file format
- **WHEN** user runs `labdataplot info unknown.xyz`
- **THEN** displays error: "Error: Could not detect file format for unknown.xyz"
- **AND** suggests using --parser option

#### Scenario: Invalid channel
- **WHEN** user runs `labdataplot plot data.xlsx --channels INVALID`
- **THEN** displays error: "Error: Channel 'INVALID' not found. Available: CH1, CH2, ..."

#### Scenario: Missing required option
- **WHEN** user runs `labdataplot plot data.xlsx` without --output
- **THEN** displays error: "Error: --output is required for plot command"
- **OR** displays plot to screen if in interactive environment

#### Scenario: Invalid option value
- **WHEN** user runs `labdataplot plot data.xlsx --channels CH1 --figsize invalid`
- **THEN** displays error: "Error: Invalid figsize format. Use WxH (e.g., 12x8)"
