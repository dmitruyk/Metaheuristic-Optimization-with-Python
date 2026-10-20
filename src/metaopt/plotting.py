"""Matplotlib helpers.

Lines differ by style and marker so a plot stays readable in grayscale.
Nothing in this module is marked as a reproduction of a handbook figure.
Generated files belong in ``figures/generated/`` and are labeled as
library output.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Okabe-Ito, paired with distinct linestyles and markers.
_COLORS = ["#000000", "#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442"]
_STYLES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)), (0, (5, 1)), (0, (1, 1)), (0, (3, 1))]
_MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]


def plot_convergence(
    histories: dict[str, list[float]],
    *,
    xlabel: str = "generation",
    ylabel: str = "best objective value",
    title: str | None = None,
    log_scale: bool = False,
    path: str | Path | None = None,
):
    """Plot best-so-far histories. Returns the Matplotlib figure."""

    figure, axis = plt.subplots(figsize=(7.0, 4.5))
    for index, (label, history) in enumerate(histories.items()):
        y = np.asarray(history, dtype=float)
        x = np.arange(1, y.size + 1)
        axis.plot(
            x,
            y,
            label=label,
            color=_COLORS[index % len(_COLORS)],
            linestyle=_STYLES[index % len(_STYLES)],
            marker=_MARKERS[index % len(_MARKERS)],
            markevery=max(1, y.size // 8),
            linewidth=1.6,
        )
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    if title:
        axis.set_title(title)
    if log_scale:
        positive = [np.asarray(values, dtype=float) for values in histories.values()]
        if positive and all(np.all(values > 0) for values in positive):
            axis.set_yscale("log")
    axis.grid(True, which="both", color="0.85", linewidth=0.6)
    axis.legend(frameon=False)
    figure.tight_layout()
    if path is not None:
        figure.savefig(path, dpi=150)
    return figure


def plot_xy(
    series: dict[str, tuple[np.ndarray, np.ndarray]],
    *,
    xlabel: str,
    ylabel: str,
    title: str | None = None,
    path: str | Path | None = None,
):
    figure, axis = plt.subplots(figsize=(6.5, 4.5))
    for index, (label, (x, y)) in enumerate(series.items()):
        axis.plot(
            np.asarray(x, dtype=float),
            np.asarray(y, dtype=float),
            label=label,
            color=_COLORS[index % len(_COLORS)],
            linestyle=_STYLES[index % len(_STYLES)],
            linewidth=1.6,
        )
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    if title:
        axis.set_title(title)
    axis.grid(True, color="0.85", linewidth=0.6)
    axis.legend(frameon=False)
    figure.tight_layout()
    if path is not None:
        figure.savefig(path, dpi=150)
    return figure
