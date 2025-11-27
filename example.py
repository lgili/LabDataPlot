"""
LabDataPlot usage examples.

Run this file to see examples in action.
"""

# Add parent directory to path (if running directly)
if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

from labdataplot import DataLoader, Plotter, list_parsers


def basic_example():
    """Basic usage example."""
    print("=== Basic Example ===\n")

    # List available parsers
    print("Available parsers:", list_parsers())

    # Load file (automatic format detection)
    loader = DataLoader('Heater - 4 20ma - USB - POE - LED_Hot soak functional.xlsx')

    # View information
    print(f"\nFile: {loader.info.filename}")
    print(f"Equipment: {loader.info.equipment}")
    print(f"Acquisition date: {loader.info.acquisition_date}")
    print(f"Columns: {len(loader.columns)}")
    print(f"Samples: {len(loader.data)}")


def simple_plot_example():
    """Simple plot example."""
    print("\n=== Simple Plot ===\n")

    loader = DataLoader('Heater - 4 20ma - USB - POE - LED_Hot soak functional.xlsx')
    plotter = Plotter(loader)

    # Single column plot
    fig, ax = plotter.plot('101 (VDC)', title='Channel 101', ylabel='Voltage (V)')

    # Multiple columns plot
    fig, ax = plotter.plot(
        ['101 (VDC)', '102 (VDC)', '103 (VDC)'],
        title='Channels 101-103',
        ylabel='Voltage (V)'
    )

    plotter.show()


def subplots_example():
    """Subplots example."""
    print("\n=== Subplots ===\n")

    loader = DataLoader('Heater - 4 20ma - USB - POE - LED_Hot soak functional.xlsx')
    plotter = Plotter(loader)

    # Vertical subplots
    fig, axes = plotter.subplots(
        ['101 (VDC)', '201 (VDC)', '301 (VDC)'],
        rows=3,
        title='One channel from each slot'
    )

    plotter.show()


def quick_view_example():
    """Quick data visualization."""
    print("\n=== Quick View ===\n")

    loader = DataLoader('Funcional pré TPC_Datalogger 1.xlsx')
    plotter = Plotter(loader)

    # View first 6 channels
    fig, axes = plotter.quick(n_columns=6)

    plotter.show()


def channel_search_example():
    """Search for channels by pattern."""
    print("\n=== Channel Search ===\n")

    loader = DataLoader('Heater - 4 20ma - USB - POE - LED_Hot soak functional.xlsx')

    # Search slot 1 channels (10x)
    slot1 = loader.get_channel(r'^10')
    print(f"Slot 1 channels: {slot1[:5]}...")

    # Search slot 2 channels (20x)
    slot2 = loader.get_channel(r'^20')
    print(f"Slot 2 channels: {slot2[:5]}...")


def data_access_example():
    """Direct data access."""
    print("\n=== Data Access ===\n")

    loader = DataLoader('Funcional pré TPC_Datalogger 1.xlsx')

    # Direct column access
    channel_01 = loader['NN_01']
    print(f"Channel 01 - mean: {channel_01.mean():.6f}")
    print(f"Channel 01 - std: {channel_01.std():.6f}")

    # Full DataFrame
    df = loader.data
    print(f"\nStatistical summary:\n{loader.describe().iloc[:, :3]}")


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')  # Use GUI backend

    # Run examples
    basic_example()
    channel_search_example()
    data_access_example()

    # Uncomment to see plots:
    # simple_plot_example()
    # subplots_example()
    # quick_view_example()
