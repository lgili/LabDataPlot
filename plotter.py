"""
Plotter - Simplified matplotlib wrapper for equipment data visualization.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Sequence
from .loader import DataLoader


class Plotter:
    """
    Simple wrapper for creating plots from equipment data.

    Basic usage:
        loader = DataLoader('file.xlsx')
        plotter = Plotter(loader)

        # Simple plot
        plotter.plot('channel_01')

        # Multiple channels
        plotter.plot(['channel_01', 'channel_02', 'channel_03'])

        # Subplots
        plotter.subplots(['channel_01', 'channel_02'], rows=2)

        # Customization
        plotter.plot('channel_01', title='My Plot', ylabel='Voltage (V)')
    """

    def __init__(self, loader: DataLoader, figsize: tuple = (12, 6)):
        """
        Initializes the plotter.

        Args:
            loader: DataLoader with loaded data
            figsize: Default figure size (width, height)
        """
        self.loader = loader
        self.figsize = figsize
        self._style_applied = False

    def apply_style(self, style: str = 'seaborn-v0_8-whitegrid'):
        """Applies a matplotlib style."""
        try:
            plt.style.use(style)
        except OSError:
            plt.style.use('ggplot')
        self._style_applied = True

    def plot(
        self,
        columns: str | Sequence[str],
        x: str | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        legend: bool = True,
        grid: bool = True,
        figsize: tuple | None = None,
        **kwargs
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Plots one or more columns.

        Args:
            columns: Column name or list of columns to plot
            x: Column for X axis (default: time column or index)
            title: Plot title
            xlabel: X axis label
            ylabel: Y axis label
            legend: Show legend
            grid: Show grid
            figsize: Figure size
            **kwargs: Additional arguments for plt.plot()

        Returns:
            tuple: (Figure, Axes)
        """
        if isinstance(columns, str):
            columns = [columns]

        # Determine X axis
        if x is None:
            x_data = self.loader.time
            if x_data is None:
                x_data = self.loader.data.index
                xlabel = xlabel or 'Index'
            else:
                xlabel = xlabel or 'Time'
        else:
            x_data = self.loader[x]
            xlabel = xlabel or x

        # Create figure
        fig, ax = plt.subplots(figsize=figsize or self.figsize)

        # Plot each column
        for col in columns:
            y_data = self.loader[col]
            label = self._simplify_label(col)
            ax.plot(x_data, y_data, label=label, **kwargs)

        # Configure plot
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if legend and len(columns) > 1:
            ax.legend()
        if grid:
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig, ax

    def subplots(
        self,
        columns: Sequence[str],
        rows: int | None = None,
        cols: int = 1,
        x: str | None = None,
        sharex: bool = True,
        sharey: bool = False,
        title: str | None = None,
        figsize: tuple | None = None,
        **kwargs
    ) -> tuple[plt.Figure, np.ndarray]:
        """
        Creates multiple subplots.

        Args:
            columns: List of columns to plot
            rows: Number of rows (calculated automatically if None)
            cols: Number of columns
            x: Column for X axis
            sharex: Share X axis between subplots
            sharey: Share Y axis between subplots
            title: Overall figure title
            figsize: Figure size
            **kwargs: Additional arguments for plt.plot()

        Returns:
            tuple: (Figure, array of Axes)
        """
        n_plots = len(columns)

        if rows is None:
            rows = (n_plots + cols - 1) // cols

        # Determine X axis
        if x is None:
            x_data = self.loader.time
            if x_data is None:
                x_data = self.loader.data.index
        else:
            x_data = self.loader[x]

        # Calculate figure size
        if figsize is None:
            figsize = (self.figsize[0], 3 * rows)

        # Create subplots
        fig, axes = plt.subplots(rows, cols, figsize=figsize, sharex=sharex, sharey=sharey)

        # Ensure axes is always an array
        if n_plots == 1:
            axes = np.array([axes])
        axes = axes.flatten()

        # Plot each column
        for i, col in enumerate(columns):
            if i >= len(axes):
                break

            ax = axes[i]
            y_data = self.loader[col]
            label = self._simplify_label(col)

            ax.plot(x_data, y_data, **kwargs)
            ax.set_ylabel(label)
            ax.grid(True, alpha=0.3)

        # Hide unused axes
        for i in range(n_plots, len(axes)):
            axes[i].set_visible(False)

        # Overall title
        if title:
            fig.suptitle(title)

        plt.tight_layout()
        return fig, axes

    def compare(
        self,
        *loaders: DataLoader,
        column: str,
        labels: Sequence[str] | None = None,
        title: str | None = None,
        figsize: tuple | None = None,
        **kwargs
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Compares the same column across multiple files.

        Args:
            *loaders: DataLoaders to compare
            column: Column name to compare
            labels: Labels for each loader
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments for plt.plot()

        Returns:
            tuple: (Figure, Axes)
        """
        all_loaders = [self.loader] + list(loaders)

        if labels is None:
            labels = [l.filepath.stem for l in all_loaders]

        fig, ax = plt.subplots(figsize=figsize or self.figsize)

        for loader, label in zip(all_loaders, labels):
            x_data = loader.time if loader.time is not None else loader.data.index
            y_data = loader[column]
            ax.plot(x_data, y_data, label=label, **kwargs)

        ax.set_title(title or f'Comparison: {column}')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig, ax

    def heatmap(
        self,
        columns: Sequence[str] | None = None,
        title: str | None = None,
        figsize: tuple | None = None,
        cmap: str = 'RdYlBu_r'
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Creates a heatmap of the data.

        Args:
            columns: Columns to include (default: all)
            title: Plot title
            figsize: Figure size
            cmap: Colormap

        Returns:
            tuple: (Figure, Axes)
        """
        if columns is None:
            columns = self.loader.columns

        data = self.loader.data[columns].T

        fig, ax = plt.subplots(figsize=figsize or (self.figsize[0], len(columns) * 0.3 + 2))

        im = ax.imshow(data, aspect='auto', cmap=cmap)
        plt.colorbar(im, ax=ax)

        # Labels
        ax.set_yticks(range(len(columns)))
        ax.set_yticklabels([self._simplify_label(c) for c in columns])
        ax.set_xlabel('Sample')

        if title:
            ax.set_title(title)

        plt.tight_layout()
        return fig, ax

    def quick(self, n_columns: int = 10) -> tuple[plt.Figure, np.ndarray]:
        """
        Quick visualization of the first N columns.

        Args:
            n_columns: Number of columns to plot

        Returns:
            tuple: (Figure, array of Axes)
        """
        columns = self.loader.columns[:n_columns]
        return self.subplots(columns, title=f'Quick View: {self.loader.filepath.name}')

    def _simplify_label(self, column: str) -> str:
        """Simplifies column name for use as label."""
        # Remove common prefixes
        import re
        match = re.search(r'_(\d+)', str(column))
        if match:
            return f'Ch {match.group(1)}'

        # For Keysight, extract channel number
        match = re.match(r'(\d+)', str(column))
        if match:
            return f'Ch {match.group(1)}'

        return str(column)

    def show(self):
        """Shows all plots."""
        plt.show()

    def save(self, filename: str, dpi: int = 150, **kwargs):
        """Saves the current figure."""
        plt.savefig(filename, dpi=dpi, bbox_inches='tight', **kwargs)
