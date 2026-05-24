from __future__ import annotations

import csv
from pathlib import Path
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
PREVIEW = OUT / "_preview"
WRITE_PREVIEW = "--preview" in sys.argv
CHOLESKY_LOCAL_COPY_CSV = OUT / "data" / "cholesky_local_copy_window.csv"


BENCH = ["FDTD", "CG", "MiniWeather", "Cholesky", "LU"]
BENCH_SHORT = ["FDTD", "CG", "MiniW.", "Chol.", "LU"]

TASKS = np.array([491712, 34, 57600, 2600, 318549], dtype=float)
COPY_BYTES = np.array(
    [353009664, 654311738, 241833733942, 15221178776, 22258961026],
    dtype=float,
)

PLACEMENT_LAT_DELTA = np.array([-6.530, -13.733, 0.019, -10.063, -18.539])
PLACEMENT_BANDIT_NORM = 100.0 + PLACEMENT_LAT_DELTA

LOC_BENCH = ["FDTD", "CG", "MiniWeather", "Cholesky", "LU"]
COPY_DELTA = np.array([-12.030, -7.692, 0.0, -38.220, -23.905])
LOC_LAT_DELTA = np.array([-6.530, -13.733, 0.019, -10.063, -18.539])

DVFS_BENCH = ["FDTD", "CG", "MiniWeather", "LU", "Cholesky"]
DVFS_SHORT = ["FDTD", "CG", "MiniW.", "LU", "Chol."]
LAT_DELTA = np.array([0.130, -0.471, -0.050, 1.498, 1.303])
ENERGY_DELTA = np.array([-6.208, -10.106, -1.656, -4.982, -3.421])
EDP_DELTA = np.array([-6.086, -10.529, -1.705, -3.559, -2.162])
EDP = np.array([0.939138, 0.894706, 0.982951, 0.964413, 0.978376])

CLOCK_BENCH = ["FDTD", "MiniWeather", "CG", "LU", "Cholesky"]
CLOCK_SHORT = ["FDTD", "MiniW.", "CG", "LU", "Chol."]
CLOCK_ENERGY_DELTA = np.array([-3.829, -3.079, -5.587, -3.287, -1.411])
CLOCK_MID_SAMPLES = np.array([91.903, 0.0, 98.912, 58.685, 58.654])
CLOCK_EFF_MID_SHARE = np.array([1.000, 0.000, 0.333, 0.697, 0.637])
CLOCK_COMMIT_SWITCHES = np.array([8, 0, 512, 290, 57])
CLOCK_FORCE_HIGH = np.array([0, 0, 0, 127, 23])
CLOCK_SLOWDOWN = np.array([0, 0, 0, 127, 23])

OVER_LABELS = ["Compact\nlog", "Force-\nnoop", "All-HIGH\nno-request"]
OVER_LATENCY = np.array([0.724, -1.144, -0.884])
OVER_ENERGY = np.array([0.620, -0.574, -0.494])
OVER_EDP = np.array([0.790, -0.925, 0.126])


COLORS = {
    "latency": "#2F5F98",
    "latency_light": "#84A9CF",
    "energy": "#3A8C6E",
    "power": "#B5682D",
    "baseline": "#A7A9AC",
    "optimized": "#3A8C6E",
    "copy": "#6F7782",
    "mid": "#6A4C93",
    "guard": "#6A4C93",
    "grid": "#D7DCE2",
    "text": "#202124",
}


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.0,
            "axes.labelsize": 8.0,
            "axes.titlesize": 8.5,
            "xtick.labelsize": 7.2,
            "ytick.labelsize": 7.2,
            "legend.fontsize": 7.0,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "mathtext.fontset": "dejavusans",
            "figure.dpi": 180,
            "savefig.dpi": 300,
            "text.color": COLORS["text"],
            "axes.labelcolor": COLORS["text"],
            "axes.edgecolor": COLORS["text"],
            "xtick.color": COLORS["text"],
            "ytick.color": COLORS["text"],
        }
    )


def polish_axes(ax: plt.Axes, grid_axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis=grid_axis, color=COLORS["grid"], linewidth=0.55, alpha=0.75)
    ax.set_axisbelow(True)


def save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.55)
    fig.savefig(OUT / name, bbox_inches="tight", pad_inches=0.018)
    if WRITE_PREVIEW:
        PREVIEW.mkdir(parents=True, exist_ok=True)
        fig.savefig(PREVIEW / name.replace(".pdf", ".png"), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def zero_line(ax: plt.Axes, axis: str = "y") -> None:
    if axis == "y":
        ax.axhline(0, color="#2B2B2B", linewidth=0.75, zorder=1)
    else:
        ax.axvline(0, color="#2B2B2B", linewidth=0.75, zorder=1)


def bar_labels(ax: plt.Axes, bars, fmt: str = "{:.1f}", dy: float = 1.8) -> None:
    ymin, ymax = ax.get_ylim()
    span = ymax - ymin
    for b in bars:
        h = b.get_height()
        if abs(h) < 0.03:
            continue
        y = h + (dy / 100.0) * span if h >= 0 else h - (dy / 100.0) * span
        va = "bottom" if h >= 0 else "top"
        ax.text(
            b.get_x() + b.get_width() / 2,
            y,
            fmt.format(h),
            ha="center",
            va=va,
            fontsize=6.1,
            color=COLORS["text"],
        )


def grouped_bars(
    name: str,
    labels: list[str],
    series: list[tuple[str, np.ndarray, str]],
    ylabel: str,
    ylim: tuple[float, float] | None = None,
    hline: float | None = 0.0,
    width: float = 5.25,
    height: float = 2.55,
    legend_cols: int | None = None,
    annotate: bool = False,
) -> None:
    fig, ax = plt.subplots(figsize=(width, height))
    x = np.arange(len(labels))
    n = len(series)
    bw = min(0.72 / n, 0.28)
    offsets = (np.arange(n) - (n - 1) / 2) * bw
    all_bars = []
    for off, (label, values, color) in zip(offsets, series):
        bars = ax.bar(
            x + off,
            values,
            width=bw * 0.92,
            label=label,
            color=color,
            edgecolor="#1F2933",
            linewidth=0.35,
        )
        all_bars.append(bars)
    if hline is not None:
        ax.axhline(hline, color="#2B2B2B", linewidth=0.75, linestyle="-" if hline == 0 else "--")
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=18, ha="right", rotation_mode="anchor")
    if ylim is not None:
        ax.set_ylim(*ylim)
    polish_axes(ax)
    cols = legend_cols or len(series)
    ax.legend(frameon=False, ncols=cols, loc="upper center", bbox_to_anchor=(0.5, 1.12), columnspacing=1.0)
    if annotate:
        for bars in all_bars:
            bar_labels(ax, bars)
    save(fig, name)


def results_overview() -> None:
    fig, ax = plt.subplots(figsize=(4.35, 2.4))
    labels = ["Placement\nlatency", "DVFS\nenergy"]
    baseline = np.array([1.0, 1.0])
    optimized = np.array([0.900113, 0.946816])
    x = np.array([0.0, 1.35])
    bw = 0.18
    ax.bar(x - bw / 2, baseline, width=bw, color=COLORS["baseline"], edgecolor="#333333", linewidth=0.35, label="Baseline")
    bars = ax.bar(x + bw / 2, optimized, width=bw, color=COLORS["optimized"], edgecolor="#333333", linewidth=0.35, label="Optimized")
    ax.axhline(1.0, color="#333333", linewidth=0.7, linestyle="--")
    ax.set_ylim(0.90, 1.028)
    ax.set_ylabel("Normalized value")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    polish_axes(ax)
    for bar, text in zip(bars, ["9.989% lower", "5.318% lower"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.004,
            text,
            ha="center",
            va="bottom",
            fontsize=6.4,
            color=COLORS["optimized"],
        )
    ax.legend(frameon=False, ncols=2, loc="upper center", bbox_to_anchor=(0.5, 1.14), columnspacing=1.2)
    save(fig, "results_overview.pdf")


def benchmark_copy_volume() -> None:
    fig, ax = plt.subplots(figsize=(5.05, 2.45))
    y = np.arange(len(BENCH_SHORT))
    bars = ax.barh(y, COPY_BYTES, color=COLORS["copy"], edgecolor="#1F2933", linewidth=0.35)
    ax.set_xscale("log")
    ax.set_xlim(2e8, 5e11)
    ax.set_yticks(y)
    ax.set_yticklabels(BENCH_SHORT)
    ax.invert_yaxis()
    ax.set_xlabel("")
    polish_axes(ax, grid_axis="x")
    for bar, value in zip(bars, COPY_BYTES):
        label = f"{value / 1e9:.1f} GB" if value >= 1e9 else f"{value / 1e6:.1f} MB"
        ax.text(value * 1.14, bar.get_y() + bar.get_height() / 2, label, va="center", fontsize=6.2)
    save(fig, "benchmark_copy_volume.pdf")


def placement_deltas() -> None:
    fig, ax = plt.subplots(figsize=(5.55, 2.6))
    x = np.arange(len(BENCH_SHORT))
    bw = 0.28
    ax.bar(
        x - bw / 2,
        np.full(len(BENCH_SHORT), 100.0),
        width=bw,
        label="HEFT",
        color=COLORS["baseline"],
        edgecolor="#1F2933",
        linewidth=0.35,
    )
    bars = ax.bar(
        x + bw / 2,
        PLACEMENT_BANDIT_NORM,
        width=bw,
        label="Bandit",
        color=COLORS["latency"],
        edgecolor="#1F2933",
        linewidth=0.35,
    )
    ax.axhline(100.0, color="#333333", linewidth=0.7, linestyle="--")
    ax.set_ylabel("Normalized latency (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(BENCH_SHORT, rotation=18, ha="right", rotation_mode="anchor")
    ax.set_ylim(78, 104)
    polish_axes(ax)
    ax.legend(frameon=False, ncols=2, loc="upper center", bbox_to_anchor=(0.5, 1.12), columnspacing=1.0)
    for bar, delta in zip(bars, PLACEMENT_LAT_DELTA):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() - 1.2 if delta < -2.0 else bar.get_height() + 0.55,
            f"{delta:+.1f}%",
            ha="center",
            va="top" if delta < -2.0 else "bottom",
            fontsize=6.2,
            color="white" if delta < -2.0 else COLORS["text"],
        )
    save(fig, "placement_deltas.pdf")


def copy_latency_scatter() -> None:
    fig, ax = plt.subplots(figsize=(4.25, 2.9))
    ax.scatter(COPY_DELTA, LOC_LAT_DELTA, s=34, color=COLORS["latency"], edgecolor="white", linewidth=0.45, zorder=3)
    ax.axhline(0, color="#333333", linewidth=0.7, linestyle="--")
    ax.axvline(0, color="#333333", linewidth=0.7, linestyle="--")
    offsets = {
        "FDTD": (5, 5),
        "CG": (5, -9),
        "MiniWeather": (-58, -11),
        "Cholesky": (5, 5),
        "LU": (5, -10),
    }
    for x, y, label in zip(COPY_DELTA, LOC_LAT_DELTA, LOC_BENCH):
        dx, dy = offsets[label]
        ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=6.4)
    ax.set_xlabel("Copy bytes delta (%)")
    ax.set_ylabel("Latency delta (%)")
    ax.set_xlim(-42, 4)
    ax.set_ylim(-20.5, 2.1)
    polish_axes(ax, grid_axis="both")
    save(fig, "copy_latency_scatter.pdf")


def cholesky_local_copy_footprint() -> None:
    rows: list[dict[str, str]] = []
    with CHOLESKY_LOCAL_COPY_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    order = np.arange(1, len(rows) + 1)
    heft_copy_kib = np.array([int(float(row["heft_copy_bytes"])) / 1024.0 for row in rows])
    bandit_copy_kib = np.array([int(float(row["bandit_copy_bytes"])) / 1024.0 for row in rows])
    saved_copy_kib = np.array([int(float(row["saved_copy_bytes"])) / 1024.0 for row in rows])
    cumulative_saved_mib = np.cumsum(saved_copy_kib) / 1024.0
    heft_dev = np.array([int(float(row["heft_dev"])) for row in rows])
    bandit_dev = np.array([int(float(row["bandit_dev"])) for row in rows])

    total_heft_mib = float(np.sum(heft_copy_kib) / 1024.0)
    total_bandit_mib = float(np.sum(bandit_copy_kib) / 1024.0)
    total_saved_mib = float(np.sum(saved_copy_kib) / 1024.0)
    saved_pct = total_saved_mib / total_heft_mib * 100.0 if total_heft_mib else 0.0

    fig = plt.figure(figsize=(5.85, 3.18))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.55, 1.5, 1.0], hspace=0.13)
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex=ax0)
    ax2 = fig.add_subplot(gs[2], sharex=ax0)

    device_cmap = mpl.colors.ListedColormap(
        ["#4B6F9F", "#D88C3D", "#4F8D5A", "#BA4A4A", "#6FA9A0", "#8B6F9F", "#C77886", "#8A725E"]
    )
    ax0.imshow(np.vstack([heft_dev, bandit_dev]), aspect="auto", cmap=device_cmap, vmin=0, vmax=7)
    ax0.set_yticks([0, 1])
    ax0.set_yticklabels(["HEFT", "Bandit"])
    ax0.set_xticks([])
    ax0.tick_params(axis="x", bottom=False, labelbottom=False)
    for spine in ax0.spines.values():
        spine.set_linewidth(0.6)
    ax0.text(
        0.995,
        1.15,
        "64-task Cholesky window",
        transform=ax0.transAxes,
        ha="right",
        va="bottom",
        fontsize=7.0,
    )

    bw = 0.38
    ax1.bar(order - bw / 2, heft_copy_kib, width=bw, color=COLORS["baseline"], label="HEFT", linewidth=0)
    ax1.bar(order + bw / 2, bandit_copy_kib, width=bw, color=COLORS["latency"], label="Bandit", linewidth=0)
    ax1.set_ylabel("Copy per task (KiB)")
    ax1.set_ylim(0, max(heft_copy_kib) * 1.22)
    ax1.tick_params(axis="x", bottom=False, labelbottom=False)
    ax1.legend(frameon=False, ncols=2, loc="upper right", handlelength=1.2)
    polish_axes(ax1)

    ax2.bar(order, saved_copy_kib, color=COLORS["energy"], width=0.72, linewidth=0, label="Saved copy")
    ax2b = ax2.twinx()
    ax2b.plot(order, cumulative_saved_mib, color=COLORS["text"], linewidth=1.05, label="Cumulative saved")
    ax2.set_ylabel("Saved (KiB)")
    ax2b.set_ylabel("Cumulative (MiB)")
    ax2.set_xlabel("Local task order")
    ax2.set_xlim(0.2, len(rows) + 0.8)
    ax2.set_xticks([1, 16, 32, 48, 64])
    polish_axes(ax2)
    ax2b.spines["top"].set_visible(False)
    ax2b.grid(False)

    ax2.text(
        0.015,
        0.93,
        f"HEFT {total_heft_mib:.2f} MiB; Bandit {total_bandit_mib:.2f} MiB; saved {saved_pct:.1f}%",
        transform=ax2.transAxes,
        ha="left",
        va="top",
        fontsize=6.2,
        bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
    )
    save(fig, "cholesky_local_copy_footprint.pdf")


def dvfs_deltas() -> None:
    grouped_bars(
        "dvfs_deltas.pdf",
        DVFS_SHORT,
        [
            ("Latency", LAT_DELTA, COLORS["latency"]),
            ("Energy", ENERGY_DELTA, COLORS["energy"]),
            ("EDP", EDP_DELTA, COLORS["power"]),
        ],
        "Delta vs no-DVFS (%)",
        ylim=(-11.5, 2.4),
        width=5.75,
        height=2.65,
    )


def dvfs_tradeoff() -> None:
    fig, ax = plt.subplots(figsize=(4.25, 2.9))
    ax.scatter(LAT_DELTA, ENERGY_DELTA, s=36, color=COLORS["energy"], edgecolor="white", linewidth=0.45, zorder=3)
    ax.axhline(0, color="#333333", linewidth=0.7, linestyle="--")
    ax.axvline(0, color="#333333", linewidth=0.7, linestyle="--")
    ax.axvline(1.0, color="#333333", linewidth=0.7, linestyle=":")
    ax.text(1.03, 0.19, "1% latency", fontsize=6.2, va="bottom")
    offsets = {
        "FDTD": (5, -10),
        "MiniWeather": (5, 5),
        "CG": (5, -2),
        "LU": (5, 5),
        "Cholesky": (-54, 5),
    }
    for x, y, label in zip(LAT_DELTA, ENERGY_DELTA, DVFS_BENCH):
        dx, dy = offsets[label]
        ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=6.4)
    ax.set_xlabel("Latency delta (%)")
    ax.set_ylabel("Energy delta (%)")
    ax.set_xlim(-1.0, 2.15)
    ax.set_ylim(-10.9, 0.55)
    polish_axes(ax, grid_axis="both")
    save(fig, "dvfs_tradeoff.pdf")


def dvfs_edp_ratios() -> None:
    grouped_bars(
        "dvfs_edp_ratios.pdf",
        DVFS_SHORT,
        [
            ("EDP", EDP, COLORS["energy"]),
        ],
        "Ratio to no-DVFS",
        ylim=(0.88, 1.018),
        hline=1.0,
        width=4.95,
        height=2.55,
    )


def mid_energy_scatter() -> None:
    fig, ax = plt.subplots(figsize=(4.25, 2.9))
    ax.scatter(CLOCK_MID_SAMPLES, CLOCK_ENERGY_DELTA, s=36, color=COLORS["energy"], edgecolor="white", linewidth=0.45, zorder=3)
    ax.axhline(0, color="#333333", linewidth=0.7, linestyle="--")
    ax.axvline(0, color="#333333", linewidth=0.7, linestyle="--")
    offsets = {
        "FDTD": (-35, 5),
        "MiniWeather": (5, -11),
        "CG": (-19, -11),
        "LU": (5, -10),
        "Cholesky": (5, 5),
    }
    for x, y, label in zip(CLOCK_MID_SAMPLES, CLOCK_ENERGY_DELTA, CLOCK_BENCH):
        dx, dy = offsets[label]
        ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=6.4)
    ax.set_xlabel("Middle-clock samples (%)")
    ax.set_ylabel("Energy delta (%)")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-6.25, 0.55)
    polish_axes(ax, grid_axis="both")
    save(fig, "mid_energy_scatter.pdf")


def dvfs_commit_share() -> None:
    grouped_bars(
        "dvfs_commit_share.pdf",
        CLOCK_SHORT,
        [
            ("Committed MID share", CLOCK_EFF_MID_SHARE * 100.0, COLORS["mid"]),
            ("Measured MID samples", CLOCK_MID_SAMPLES, COLORS["power"]),
        ],
        "Share (%)",
        ylim=(0, 110),
        hline=None,
        width=5.55,
        height=2.55,
    )


def dvfs_guardrail_events() -> None:
    fig, ax = plt.subplots(figsize=(5.55, 2.55))
    x = np.arange(len(CLOCK_SHORT))
    bw = 0.22
    series = [
        ("Commit switches", CLOCK_COMMIT_SWITCHES, COLORS["latency"]),
        ("Force-HIGH", CLOCK_FORCE_HIGH, COLORS["guard"]),
        ("Slowdown", CLOCK_SLOWDOWN, COLORS["power"]),
    ]
    for i, (label, values, color) in enumerate(series):
        ax.bar(
            x + (i - 1) * bw,
            values,
            width=bw * 0.92,
            label=label,
            color=color,
            edgecolor="#1F2933",
            linewidth=0.35,
        )
    ax.set_yscale("symlog", linthresh=1)
    ax.set_ylim(0, 850)
    ax.set_yticks([0, 1, 10, 100, 500])
    ax.set_yticklabels(["0", "1", "10", "100", "500"])
    ax.set_ylabel("Event count")
    ax.set_xticks(x)
    ax.set_xticklabels(CLOCK_SHORT, rotation=18, ha="right", rotation_mode="anchor")
    polish_axes(ax)
    ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, 1.12), columnspacing=0.9)
    save(fig, "dvfs_guardrail_events.pdf")


def overhead_snapshot() -> None:
    grouped_bars(
        "overhead_snapshot.pdf",
        OVER_LABELS,
        [
            ("Latency", OVER_LATENCY, COLORS["latency"]),
            ("Energy", OVER_ENERGY, COLORS["energy"]),
            ("EDP", OVER_EDP, COLORS["power"]),
        ],
        "Delta vs baseline (%)",
        ylim=(-1.7, 1.2),
        width=5.15,
        height=2.45,
        legend_cols=3,
    )


def main() -> None:
    configure_style()
    results_overview()
    benchmark_copy_volume()
    placement_deltas()
    copy_latency_scatter()
    cholesky_local_copy_footprint()
    dvfs_deltas()
    dvfs_tradeoff()
    dvfs_edp_ratios()
    mid_energy_scatter()
    dvfs_commit_share()
    dvfs_guardrail_events()
    overhead_snapshot()


if __name__ == "__main__":
    main()
