"""Small helpers for writing the Markdown report and its figures."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Categorical slots 1-6 of the reference palette (dataviz skill), in its validated order.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
SURFACE = "#fcfcfb"
WINDOW_ORDER = ["F", "Q1", "Q2", "Q3", "L", "C0", "ALL"]


def md_table(df: pd.DataFrame, floatfmt: str = ".1f", index: bool = False) -> str:
    """Render a DataFrame as a GitHub Markdown table without extra dependencies."""
    if index:
        df = df.reset_index()
    cols = [str(c) for c in df.columns]

    def cell(v):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return ""
        if isinstance(v, float):
            return f"{v:{floatfmt}}" if abs(v - round(v)) > 1e-9 or abs(v) >= 1e6 else f"{v:.0f}"
        return str(v).replace("|", "\\|")

    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(cell(v) for v in row.tolist()) + " |")
    return "\n".join(lines)


def style_axes(ax) -> None:
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.xaxis.label.set_color(INK_2)
    ax.yaxis.label.set_color(INK_2)
    ax.title.set_color(INK)


def line_figure(
    series: dict[str, list[float]],
    title: str,
    xlabel: str,
    ylabel: str,
    path: Path,
    colors: list[str] | None = None,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=130)
    fig.patch.set_facecolor(SURFACE)
    colors = colors or SERIES
    for i, (name, values) in enumerate(series.items()):
        ax.plot(
            range(len(values)), values, linewidth=1.6, color=colors[i % len(colors)], label=name
        )
        if values:
            ax.text(len(values) - 1 + 0.3, values[-1], name, fontsize=7, color=INK_2, va="center")
    style_axes(ax)
    ax.set_title(title, fontsize=10, loc="left")
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    if len(series) >= 2:
        ax.legend(fontsize=7, frameon=False, labelcolor=INK_2)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def bar_figure(labels: list[str], values: list[float], title: str, ylabel: str, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=130)
    fig.patch.set_facecolor(SURFACE)
    ax.bar(range(len(values)), values, color=SERIES[0], width=0.6)
    for i, v in enumerate(values):
        ax.text(i, v, f"{v:.0f}", ha="center", va="bottom", fontsize=7, color=INK_2)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=7)
    style_axes(ax)
    ax.set_title(title, fontsize=10, loc="left")
    ax.set_ylabel(ylabel, fontsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
