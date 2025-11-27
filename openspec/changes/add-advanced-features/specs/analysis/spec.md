# Analysis Capability

## ADDED Requirements

### Requirement: Statistical Analysis
The system SHALL provide statistical analysis for measurement channels including minimum, maximum, mean, standard deviation, RMS, and peak-to-peak values.

#### Scenario: Get statistics for all channels
- **WHEN** user calls `loader.stats()` without arguments
- **THEN** returns a dictionary with statistics for all data channels
- **AND** each channel entry contains min, max, mean, std, rms, peak_to_peak keys

#### Scenario: Get statistics for specific channels
- **WHEN** user calls `loader.stats(['CH1', 'CH2'])`
- **THEN** returns statistics only for the specified channels
- **AND** raises KeyError if channel does not exist

#### Scenario: Get formatted statistics table
- **WHEN** user calls `loader.stats_table()`
- **THEN** returns a pandas DataFrame with channels as rows and statistics as columns
- **AND** values are formatted with appropriate precision

#### Scenario: Calculate RMS value
- **WHEN** user calls `loader.rms('CH1')`
- **THEN** returns the root mean square value calculated as sqrt(mean(x²))

---

### Requirement: Anomaly Detection
The system SHALL detect anomalies in measurement data including spikes, drops, outliers, and flatlines.

#### Scenario: Detect spikes above threshold
- **WHEN** user calls `loader.detect_spikes('CH1', threshold=3.0)`
- **THEN** returns list of indices where value exceeds mean + threshold * std
- **AND** each result includes index, timestamp (if available), and value

#### Scenario: Detect drops below threshold
- **WHEN** user calls `loader.detect_drops('CH1', threshold=3.0)`
- **THEN** returns list of indices where value falls below mean - threshold * std

#### Scenario: Detect outliers using Z-score method
- **WHEN** user calls `loader.detect_outliers('CH1', method='zscore', threshold=3.0)`
- **THEN** returns list of indices where |z-score| exceeds threshold

#### Scenario: Detect outliers using IQR method
- **WHEN** user calls `loader.detect_outliers('CH1', method='iqr', factor=1.5)`
- **THEN** returns list of indices outside [Q1 - factor*IQR, Q3 + factor*IQR]

#### Scenario: Detect flatlines
- **WHEN** user calls `loader.detect_flatlines('CH1', min_duration=10)`
- **THEN** returns list of regions where value remains constant for min_duration samples
- **AND** each region includes start_index, end_index, value, duration

#### Scenario: Get all anomalies summary
- **WHEN** user calls `loader.anomalies(threshold=3.0)`
- **THEN** returns dictionary with all detected anomalies grouped by type
- **AND** includes counts and details for each anomaly type

---

### Requirement: FFT/Frequency Analysis
The system SHALL provide frequency domain analysis using Fast Fourier Transform.

#### Scenario: Compute FFT of channel
- **WHEN** user calls `loader.fft('CH1')`
- **THEN** returns tuple of (frequencies, magnitudes) numpy arrays
- **AND** frequencies are in Hz based on sample_rate from DataInfo
- **AND** only positive frequencies are returned (single-sided spectrum)

#### Scenario: Get dominant frequencies
- **WHEN** user calls `loader.dominant_frequencies('CH1', n=5)`
- **THEN** returns list of n frequencies with highest magnitudes
- **AND** each entry includes frequency (Hz) and magnitude

#### Scenario: Compute power spectral density
- **WHEN** user calls `loader.power_spectrum('CH1')`
- **THEN** returns tuple of (frequencies, power) numpy arrays
- **AND** power is in units of V²/Hz (or appropriate unit squared per Hz)

#### Scenario: FFT without sample rate
- **WHEN** user calls `loader.fft('CH1')` and sample_rate is not available
- **THEN** raises ValueError with message indicating sample_rate is required
- **OR** uses index-based frequency (samples⁻¹) if `use_index=True`

---

### Requirement: Correlation Analysis
The system SHALL provide correlation analysis between measurement channels.

#### Scenario: Compute correlation matrix
- **WHEN** user calls `loader.correlation(['CH1', 'CH2', 'CH3'])`
- **THEN** returns pandas DataFrame with Pearson correlation coefficients
- **AND** DataFrame has channel names as both index and columns

#### Scenario: Compute correlation for all channels
- **WHEN** user calls `loader.correlation()` without arguments
- **THEN** returns correlation matrix for all data channels

#### Scenario: Compute cross-correlation with lag
- **WHEN** user calls `loader.cross_correlation('CH1', 'CH2', max_lag=100)`
- **THEN** returns tuple of (lags, correlation_values) arrays
- **AND** lags range from -max_lag to +max_lag samples

#### Scenario: Find lag of maximum correlation
- **WHEN** user calls `loader.find_delay('CH1', 'CH2', max_lag=100)`
- **THEN** returns the lag value (in samples) where correlation is maximum
- **AND** positive lag means CH2 lags behind CH1
