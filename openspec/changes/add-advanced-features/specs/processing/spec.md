# Processing Capability

## ADDED Requirements

### Requirement: Digital Filters
The system SHALL provide digital signal processing filters for noise reduction and signal conditioning.

#### Scenario: Apply low-pass Butterworth filter
- **WHEN** user calls `loader.filter('CH1', 'lowpass', cutoff=100, order=4)`
- **THEN** returns new DataLoader with filtered CH1 data
- **AND** frequencies above cutoff are attenuated
- **AND** original loader is not modified

#### Scenario: Apply high-pass Butterworth filter
- **WHEN** user calls `loader.filter('CH1', 'highpass', cutoff=10, order=4)`
- **THEN** returns new DataLoader with filtered CH1 data
- **AND** frequencies below cutoff are attenuated

#### Scenario: Apply band-pass filter
- **WHEN** user calls `loader.filter('CH1', 'bandpass', low=10, high=100, order=4)`
- **THEN** returns new DataLoader with filtered CH1 data
- **AND** only frequencies between low and high pass through

#### Scenario: Apply moving average filter
- **WHEN** user calls `loader.filter('CH1', 'moving_average', window=10)`
- **THEN** returns new DataLoader with smoothed CH1 data
- **AND** each point is average of surrounding window points

#### Scenario: Apply median filter for spike removal
- **WHEN** user calls `loader.filter('CH1', 'median', window=5)`
- **THEN** returns new DataLoader with filtered CH1 data
- **AND** spikes are replaced by median of surrounding values

#### Scenario: Apply filter to all channels
- **WHEN** user calls `loader.filter_all('lowpass', cutoff=100)`
- **THEN** returns new DataLoader with all channels filtered
- **AND** time column is preserved unchanged

#### Scenario: Filter without scipy
- **WHEN** user applies Butterworth filter and scipy is not installed
- **THEN** raises ImportError with message: "Install scipy: pip install labdataplot[analysis]"

---

### Requirement: Resampling
The system SHALL provide methods to change the sampling rate of data.

#### Scenario: Resample to new rate
- **WHEN** user calls `loader.resample(new_rate=1000)`
- **THEN** returns new DataLoader with data at 1000 samples/second
- **AND** uses linear interpolation by default

#### Scenario: Resample with cubic interpolation
- **WHEN** user calls `loader.resample(new_rate=1000, method='cubic')`
- **THEN** returns new DataLoader with cubic-interpolated data
- **AND** produces smoother result than linear

#### Scenario: Downsample by factor
- **WHEN** user calls `loader.downsample(factor=10)`
- **THEN** returns new DataLoader with 1/10th the samples
- **AND** applies anti-aliasing filter before downsampling

#### Scenario: Upsample by factor
- **WHEN** user calls `loader.upsample(factor=2, method='linear')`
- **THEN** returns new DataLoader with 2x the samples
- **AND** new samples are interpolated values

#### Scenario: Decimate with anti-aliasing
- **WHEN** user calls `loader.decimate(factor=10)`
- **THEN** applies low-pass filter then downsamples
- **AND** cutoff frequency is set to prevent aliasing

#### Scenario: Resample without sample rate
- **WHEN** user calls `loader.resample(new_rate=1000)` and sample_rate is None
- **THEN** raises ValueError with message indicating sample_rate is required

---

### Requirement: Time Operations
The system SHALL provide methods to manipulate the time range of data.

#### Scenario: Trim by time values
- **WHEN** user calls `loader.trim(start=10.0, end=60.0)`
- **THEN** returns new DataLoader with data between 10 and 60 time units
- **AND** time column is adjusted to start at 0 if `reset_time=True`

#### Scenario: Trim by index
- **WHEN** user calls `loader.trim_index(start=100, end=500)`
- **THEN** returns new DataLoader with samples 100 through 500
- **AND** supports negative indices (e.g., end=-1 for last sample)

#### Scenario: Trim from start only
- **WHEN** user calls `loader.trim(start=10.0)`
- **THEN** returns new DataLoader with data from time 10 to end

#### Scenario: Trim to end only
- **WHEN** user calls `loader.trim(end=60.0)`
- **THEN** returns new DataLoader with data from start to time 60

#### Scenario: Split data at time points
- **WHEN** user calls `loader.split(times=[30, 60, 90])`
- **THEN** returns list of 4 DataLoaders: [0-30], [30-60], [60-90], [90-end]
- **AND** each segment has its time reset to start at 0

#### Scenario: Align time to zero
- **WHEN** user calls `loader.align_to_zero()`
- **THEN** returns new DataLoader with time column starting at 0
- **AND** all time values are shifted by subtracting minimum

#### Scenario: Shift time by offset
- **WHEN** user calls `loader.shift_time(offset=5.0)`
- **THEN** returns new DataLoader with all time values increased by 5

---

### Requirement: File Merging
The system SHALL provide methods to combine multiple data files.

#### Scenario: Merge files vertically (concatenate)
- **WHEN** user calls `merge(loader1, loader2, loader3)`
- **THEN** returns new DataLoader with all data concatenated
- **AND** time column continues from where previous ended
- **AND** all loaders must have matching columns

#### Scenario: Merge with time gap
- **WHEN** user calls `merge(loader1, loader2, gap=10.0)`
- **THEN** inserts 10 time unit gap between datasets
- **AND** useful for separating distinct test phases

#### Scenario: Join files horizontally (add columns)
- **WHEN** user calls `join(loader1, loader2, on='time', suffixes=('_1', '_2'))`
- **THEN** returns new DataLoader with columns from both files
- **AND** aligns data by time column
- **AND** adds suffixes to distinguish duplicate column names

#### Scenario: Append data to existing loader
- **WHEN** user calls `loader1.append(loader2)`
- **THEN** returns new DataLoader with loader2 data added after loader1
- **AND** equivalent to `merge(loader1, loader2)`

#### Scenario: Merge with column mismatch
- **WHEN** user calls `merge(loader1, loader2)` with different columns
- **THEN** raises ValueError with message listing mismatched columns
- **OR** if `ignore_missing=True`, fills missing columns with NaN

---

### Requirement: Channel Math Operations
The system SHALL provide methods for mathematical operations on channels.

#### Scenario: Add calculated channel with formula
- **WHEN** user calls `loader.add_channel('Power', 'Voltage * Current')`
- **THEN** adds new column 'Power' calculated as product of Voltage and Current
- **AND** formula supports +, -, *, /, **, parentheses

#### Scenario: Add channel with constant
- **WHEN** user calls `loader.add_channel('Celsius', '(Fahrenheit - 32) * 5/9')`
- **THEN** adds new column with temperature conversion
- **AND** supports numeric constants in formula

#### Scenario: Calculate derivative
- **WHEN** user calls `loader.diff('CH1')` or `loader.derivative('CH1')`
- **THEN** returns new DataLoader with derivative of CH1
- **AND** uses central difference method
- **AND** result is in units per time unit

#### Scenario: Calculate integral
- **WHEN** user calls `loader.integrate('CH1')`
- **THEN** returns new DataLoader with cumulative integral of CH1
- **AND** uses trapezoidal rule
- **AND** result is in units * time unit

#### Scenario: Scale channel linearly
- **WHEN** user calls `loader.scale('CH1', factor=2.0, offset=1.0)`
- **THEN** returns new DataLoader with CH1 transformed as: new = factor * old + offset

#### Scenario: Apply custom function
- **WHEN** user calls `loader.apply('CH1', func=np.abs)`
- **THEN** returns new DataLoader with function applied element-wise to CH1

#### Scenario: Remove channel
- **WHEN** user calls `loader.drop('CH1')` or `loader.drop(['CH1', 'CH2'])`
- **THEN** returns new DataLoader without specified channels

#### Scenario: Rename channel
- **WHEN** user calls `loader.rename({'CH1': 'Voltage', 'CH2': 'Current'})`
- **THEN** returns new DataLoader with renamed columns
