# Export Capability

## ADDED Requirements

### Requirement: PDF Report Generation
The system SHALL generate professional PDF reports with plots, statistics, and analysis results.

#### Scenario: Generate basic PDF report
- **WHEN** user calls `loader.to_pdf('report.pdf')`
- **THEN** creates PDF file with default sections: title page, data summary, all-channel plot
- **AND** includes file metadata (name, equipment, acquisition date)

#### Scenario: Generate PDF with custom configuration
- **WHEN** user calls:
```python
report = ReportGenerator(loader)
report.add_title_page(title='Test Report', subtitle='Thermal Analysis')
report.add_statistics_table(channels=['T1', 'T2', 'T3'])
report.add_plot(['T1', 'T2'], title='Temperature')
report.add_anomaly_summary()
report.save('report.pdf')
```
- **THEN** creates PDF with sections in specified order
- **AND** each section is formatted professionally

#### Scenario: Add multiple plot sections
- **WHEN** user calls `report.add_plot()` multiple times with different channels
- **THEN** each plot appears on its own page or section
- **AND** plots maintain aspect ratio and quality

#### Scenario: Add statistics table to report
- **WHEN** user calls `report.add_statistics_table()`
- **THEN** adds formatted table with min, max, mean, std for each channel
- **AND** table spans multiple pages if many channels

#### Scenario: Add anomaly summary
- **WHEN** user calls `report.add_anomaly_summary(threshold=3.0)`
- **THEN** adds section listing all detected anomalies
- **AND** groups anomalies by type and channel

#### Scenario: Use custom template
- **WHEN** user calls `report.set_template('my_template.html')`
- **THEN** uses Jinja2 template for PDF layout
- **AND** template receives context with loader, plots, stats

#### Scenario: PDF generation without dependencies
- **WHEN** user calls `to_pdf()` and reportlab/weasyprint not installed
- **THEN** raises ImportError with message: "Install export dependencies: pip install labdataplot[export]"

---

### Requirement: Excel Export
The system SHALL export data to Excel format with formatting, statistics, and optional charts.

#### Scenario: Export data to Excel
- **WHEN** user calls `loader.to_excel('output.xlsx')`
- **THEN** creates Excel file with data in 'Data' sheet
- **AND** column headers are formatted bold
- **AND** time column has appropriate date/number format

#### Scenario: Export with statistics sheet
- **WHEN** user calls `loader.to_excel('output.xlsx', include_stats=True)`
- **THEN** adds 'Statistics' sheet with summary table
- **AND** includes min, max, mean, std, rms for each channel

#### Scenario: Export with embedded charts
- **WHEN** user calls `loader.to_excel('output.xlsx', include_charts=True)`
- **THEN** adds 'Charts' sheet with Excel line charts
- **AND** creates one chart per channel or grouped charts

#### Scenario: Export with conditional formatting
- **WHEN** user calls `loader.to_excel('output.xlsx', highlight_anomalies=True)`
- **THEN** applies conditional formatting to anomalous values
- **AND** spikes are highlighted in red, drops in blue

#### Scenario: Export specific channels
- **WHEN** user calls `loader.to_excel('output.xlsx', channels=['CH1', 'CH2'])`
- **THEN** only exports specified channels to Excel

#### Scenario: Export with custom sheet name
- **WHEN** user calls `loader.to_excel('output.xlsx', sheet_name='Measurements')`
- **THEN** data sheet is named 'Measurements' instead of 'Data'

---

### Requirement: HTML Report Generation
The system SHALL generate interactive HTML reports with embedded Plotly charts.

#### Scenario: Generate basic HTML report
- **WHEN** user calls `loader.to_html('report.html')`
- **THEN** creates standalone HTML file with embedded data and charts
- **AND** file can be opened in any browser without server

#### Scenario: Generate HTML with interactive plots
- **WHEN** user calls `loader.to_html('report.html', interactive=True)`
- **THEN** embeds Plotly charts with zoom, pan, hover
- **AND** includes Plotly.js library inline

#### Scenario: Generate HTML with static images
- **WHEN** user calls `loader.to_html('report.html', interactive=False)`
- **THEN** embeds matplotlib plots as base64 PNG images
- **AND** file size is smaller but no interactivity

#### Scenario: Apply dark theme
- **WHEN** user calls `loader.to_html('report.html', theme='dark')`
- **THEN** uses dark color scheme for background and text
- **AND** charts use dark theme as well

#### Scenario: Apply responsive layout
- **WHEN** user opens HTML report on mobile device
- **THEN** layout adjusts to screen size
- **AND** charts are scrollable and readable

#### Scenario: Include table of contents
- **WHEN** user calls `loader.to_html('report.html', toc=True)`
- **THEN** includes clickable table of contents at top
- **AND** links navigate to corresponding sections

---

### Requirement: Batch Plot Export
The system SHALL export multiple plots at once to a directory.

#### Scenario: Save all channel plots
- **WHEN** user calls `plotter.save_all('plots/')`
- **THEN** creates one plot file per channel in plots/ directory
- **AND** files are named by channel: 'CH1.png', 'CH2.png', etc.

#### Scenario: Save plots in specific format
- **WHEN** user calls `plotter.save_all('plots/', format='pdf')`
- **THEN** creates PDF files instead of PNG

#### Scenario: Save plots with custom DPI
- **WHEN** user calls `plotter.save_all('plots/', dpi=300)`
- **THEN** creates high-resolution images at 300 DPI

#### Scenario: Save plots with naming template
- **WHEN** user calls `plotter.save_all('plots/', naming='{filename}_{channel}')`
- **THEN** uses template: 'myfile_CH1.png', 'myfile_CH2.png'

#### Scenario: Save grouped plots
- **WHEN** user calls `plotter.save_all('plots/', group_size=4)`
- **THEN** creates plots with 4 channels each
- **AND** files named: 'group_1.png', 'group_2.png'

#### Scenario: Generate thumbnails
- **WHEN** user calls `plotter.save_all('plots/', thumbnails=True)`
- **THEN** creates additional thumbnail images
- **AND** thumbnails are in 'plots/thumbs/' subdirectory
- **AND** thumbnails are 200px wide

#### Scenario: Skip existing files
- **WHEN** user calls `plotter.save_all('plots/', skip_existing=True)`
- **THEN** does not overwrite existing files
- **AND** only creates new plot files

---

### Requirement: CSV/Data Export
The system SHALL export processed data to various text formats.

#### Scenario: Export to CSV
- **WHEN** user calls `loader.to_csv('output.csv')`
- **THEN** creates CSV file with all data
- **AND** uses comma as delimiter by default

#### Scenario: Export to CSV with specific delimiter
- **WHEN** user calls `loader.to_csv('output.tsv', delimiter='\t')`
- **THEN** creates tab-separated file

#### Scenario: Export specific channels to CSV
- **WHEN** user calls `loader.to_csv('output.csv', channels=['CH1', 'CH2'])`
- **THEN** only exports time and specified channels

#### Scenario: Export without time column
- **WHEN** user calls `loader.to_csv('output.csv', include_time=False)`
- **THEN** exports only data columns without time

#### Scenario: Export with specific encoding
- **WHEN** user calls `loader.to_csv('output.csv', encoding='utf-8-sig')`
- **THEN** creates file with BOM for Excel compatibility
