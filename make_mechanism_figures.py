from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle


OUT = Path(__file__).resolve().parent / "figures"

COL = {
    "ink": "#243142",
    "muted": "#64748b",
    "blue": "#3b82f6",
    "blue_l": "#dbeafe",
    "teal": "#14b8a6",
    "teal_l": "#ccfbf1",
    "orange": "#f59e0b",
    "orange_l": "#fef3c7",
    "red": "#ef4444",
    "red_l": "#fee2e2",
    "green": "#22c55e",
    "green_l": "#dcfce7",
    "gray": "#e5e7eb",
    "gray_l": "#f8fafc",
    "violet": "#8b5cf6",
    "violet_l": "#ede9fe",
}


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 9,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(path)


def setup(width=7.2, height=3.6):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc, ec=None, lw=1.0, fs=8, weight="normal", radius=0.025):
    ec = ec or COL["ink"]
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        color=COL["ink"],
        fontweight=weight,
        zorder=3,
        linespacing=1.08,
    )
    return patch


def label(ax, x, y, text, fs=8, color=None, weight="normal", ha="center", va="center"):
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va=va,
        fontsize=fs,
        color=color or COL["ink"],
        fontweight=weight,
        linespacing=1.08,
        zorder=5,
    )


def arrow(ax, x1, y1, x2, y2, color=None, lw=1.0, rad=0.0, ms=8, style="-|>"):
    arr = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle=style,
        mutation_scale=ms,
        linewidth=lw,
        color=color or COL["ink"],
        connectionstyle=f"arc3,rad={rad}",
        zorder=4,
    )
    ax.add_patch(arr)
    return arr


def diamond(ax, cx, cy, w, h, text, fc, ec=None, fs=7.5):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    poly = Polygon(pts, closed=True, facecolor=fc, edgecolor=ec or COL["ink"], linewidth=1.0, zorder=2)
    ax.add_patch(poly)
    label(ax, cx, cy, text, fs=fs)
    return poly


def section_title(ax, x, y, text, color):
    label(ax, x, y, text, fs=8.5, color=color, weight="bold")


def fig_task_residency():
    fig, ax = setup(7.4, 3.8)
    section_title(ax, 0.18, 0.93, "Task DAG", COL["blue"])
    section_title(ax, 0.52, 0.93, "Data objects", COL["teal"])
    section_title(ax, 0.82, 0.93, "Residency by GPU", COL["orange"])

    # DAG nodes.
    t1 = box(ax, 0.06, 0.70, 0.11, 0.08, "t1\nwrite A", COL["blue_l"], COL["blue"], fs=7)
    t2 = box(ax, 0.22, 0.70, 0.11, 0.08, "t2\nread A", COL["blue_l"], COL["blue"], fs=7)
    t3 = box(ax, 0.22, 0.49, 0.11, 0.08, "t3\nread B", COL["blue_l"], COL["blue"], fs=7)
    t4 = box(ax, 0.38, 0.60, 0.11, 0.08, "ready\ntask v", COL["violet_l"], COL["violet"], fs=7, weight="bold")
    arrow(ax, 0.17, 0.74, 0.22, 0.74, COL["blue"], lw=1.1)
    arrow(ax, 0.33, 0.74, 0.38, 0.65, COL["blue"], lw=1.1)
    arrow(ax, 0.33, 0.53, 0.38, 0.63, COL["blue"], lw=1.1)

    # Data objects.
    box(ax, 0.48, 0.73, 0.10, 0.06, "A", COL["teal_l"], COL["teal"], fs=8, weight="bold")
    box(ax, 0.48, 0.60, 0.10, 0.06, "B", COL["teal_l"], COL["teal"], fs=8, weight="bold")
    box(ax, 0.48, 0.47, 0.10, 0.06, "C", COL["teal_l"], COL["teal"], fs=8, weight="bold")
    label(ax, 0.54, 0.39, "access modes:\nread / write / read-write", fs=7, color=COL["muted"])

    # Residency table.
    x0, y0, w, h = 0.67, 0.43, 0.27, 0.39
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=COL["gray_l"], edgecolor=COL["ink"], linewidth=0.9))
    for i, txt in enumerate(["GPU 0", "GPU 1", "GPU 2"]):
        label(ax, x0 + 0.065 + i * 0.085, y0 + h + 0.035, txt, fs=7, weight="bold")
    for j, obj in enumerate(["A", "B", "C"]):
        label(ax, x0 - 0.025, y0 + h - 0.07 - j * 0.11, obj, fs=7, weight="bold")
    vals = [["M", "S", "I"], ["I", "S", "M"], ["S", "I", "I"]]
    for j in range(3):
        for i in range(3):
            cx = x0 + 0.065 + i * 0.085
            cy = y0 + h - 0.07 - j * 0.11
            fc = COL["green_l"] if vals[j][i] != "I" else "white"
            box(ax, cx - 0.027, cy - 0.022, 0.054, 0.044, vals[j][i], fc, COL["gray"], fs=7, radius=0.01)

    arrow(ax, 0.58, 0.76, 0.67, 0.74, COL["teal"], lw=1.0)
    arrow(ax, 0.58, 0.63, 0.67, 0.63, COL["teal"], lw=1.0)
    arrow(ax, 0.49, 0.63, 0.58, 0.63, COL["teal"], lw=0.0)

    # Candidate placement mini-panel.
    box(ax, 0.06, 0.19, 0.30, 0.15, "Candidate GPU d:\n$R_d(v)$ device readiness\n$K(v,d)$ copy cost", COL["gray_l"], COL["ink"], fs=7.2)
    box(ax, 0.40, 0.19, 0.25, 0.15, "$S_d(v)=\\max(A_d,R_d(v))$\n$F_d(v)=S_d(v)+T_d(v)$", COL["gray_l"], COL["ink"], fs=7.2)
    box(ax, 0.70, 0.19, 0.24, 0.15, "local data: $K=0$\nremote data: $K>0$", COL["orange_l"], COL["orange"], fs=7.2)
    arrow(ax, 0.36, 0.265, 0.40, 0.265, COL["ink"], lw=1.0)
    arrow(ax, 0.65, 0.265, 0.70, 0.265, COL["ink"], lw=1.0)
    save(fig, "theory_task_residency_model.pdf")


def fig_residual_gate():
    fig, ax = plt.subplots(figsize=(6.9, 3.6))
    ax.set_xlim(-0.002, 0.026)
    ax.set_ylim(0.0, 0.34)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, color="#e5e7eb", linewidth=0.6, zorder=0)
    ax.set_xlabel("Normalized finish-time penalty $\\rho_F$")
    ax.set_ylabel("Normalized copy gain $\\rho_K$")

    # Accepted regions: non-critical larger, critical smaller.
    noncrit = Rectangle((0, 0.10), 0.020, 0.24, facecolor=COL["blue_l"], edgecolor=COL["blue"], alpha=0.65, linewidth=1.0)
    crit = Rectangle((0, 0.20), 0.004, 0.14, facecolor=COL["teal_l"], edgecolor=COL["teal"], alpha=0.85, linewidth=1.2)
    ax.add_patch(noncrit)
    ax.add_patch(crit)
    ax.axvline(0.004, color=COL["teal"], linestyle="--", linewidth=1.0)
    ax.axhline(0.20, color=COL["teal"], linestyle="--", linewidth=1.0)
    ax.axvline(0.020, color=COL["blue"], linestyle="--", linewidth=1.0)
    ax.axhline(0.10, color=COL["blue"], linestyle="--", linewidth=1.0)

    pts = [
        (0.002, 0.26, "accepted\ncritical", COL["teal"]),
        (0.014, 0.17, "accepted\nnon-critical", COL["blue"]),
        (0.006, 0.07, "copy gain\ntoo small", COL["orange"]),
        (0.023, 0.24, "penalty\ntoo large", COL["red"]),
    ]
    for x, y, txt, c in pts:
        ax.scatter([x], [y], s=42, color=c, edgecolor="white", linewidth=0.6, zorder=3)
        ax.text(x + 0.001, y + 0.012, txt, fontsize=7, color=COL["ink"], va="bottom")

    ax.text(0.0032, 0.323, "critical gate", color=COL["teal"], fontsize=7, ha="right")
    ax.text(0.0195, 0.323, "non-critical gate", color=COL["blue"], fontsize=7, ha="right")
    ax.text(0.0135, 0.302, "accepted region", color=COL["ink"], fontsize=8, fontweight="bold", ha="center")
    save(fig, "theory_residual_gate_region.pdf")


def fig_dvfs_timeline():
    fig, ax = setup(7.4, 3.3)
    label(ax, 0.17, 0.92, "Window k: collect intents", fs=8.5, weight="bold", color=COL["blue"])
    label(ax, 0.56, 0.92, "Window k+1: use committed level", fs=8.5, weight="bold", color=COL["teal"])
    label(ax, 0.86, 0.92, "Guardrail recovery", fs=8.5, weight="bold", color=COL["red"])

    # Window backgrounds.
    ax.add_patch(Rectangle((0.05, 0.16), 0.33, 0.68, facecolor=COL["blue_l"], edgecolor="none", alpha=0.5))
    ax.add_patch(Rectangle((0.41, 0.16), 0.33, 0.68, facecolor=COL["teal_l"], edgecolor="none", alpha=0.55))
    ax.add_patch(Rectangle((0.77, 0.16), 0.18, 0.68, facecolor=COL["red_l"], edgecolor="none", alpha=0.35))

    # Task lane.
    label(ax, 0.04, 0.73, "tasks", fs=7, color=COL["muted"], ha="right")
    tasks = [
        (0.07, 0.69, 0.08, "compute"),
        (0.16, 0.69, 0.08, "copy"),
        (0.25, 0.69, 0.10, "wait"),
        (0.43, 0.69, 0.09, "compute"),
        (0.53, 0.69, 0.07, "copy"),
        (0.61, 0.69, 0.11, "compute"),
        (0.80, 0.69, 0.12, "HIGH"),
    ]
    for x, y, w, txt in tasks:
        fc = COL["orange_l"] if txt in ("copy", "wait") else COL["gray_l"]
        box(ax, x, y, w, 0.08, txt, fc, COL["muted"], fs=6.6, radius=0.01)

    # Intent and commit.
    label(ax, 0.04, 0.54, "intent", fs=7, color=COL["muted"], ha="right")
    for x, txt, c in [(0.10, "HIGH", COL["gray_l"]), (0.20, "MID", COL["green_l"]), (0.30, "MID", COL["green_l"])]:
        box(ax, x - 0.035, 0.50, 0.07, 0.055, txt, c, COL["muted"], fs=6.5, radius=0.01)
    arrow(ax, 0.31, 0.50, 0.47, 0.42, COL["ink"], lw=1.0, rad=-0.22)
    label(ax, 0.39, 0.45, "commit after\nwindow", fs=7, color=COL["muted"])

    # Frequency lane.
    label(ax, 0.04, 0.32, "frequency", fs=7, color=COL["muted"], ha="right")
    ax.plot([0.06, 0.42], [0.38, 0.38], color=COL["ink"], linewidth=1.4)
    ax.plot([0.42, 0.47], [0.38, 0.28], color=COL["ink"], linewidth=1.4)
    ax.plot([0.47, 0.74], [0.28, 0.28], color=COL["teal"], linewidth=2.0)
    ax.plot([0.74, 0.80], [0.28, 0.38], color=COL["ink"], linewidth=1.4)
    ax.plot([0.80, 0.95], [0.38, 0.38], color=COL["red"], linewidth=1.8)
    label(ax, 0.22, 0.415, "HIGH", fs=7)
    label(ax, 0.60, 0.245, "MID", fs=7, color=COL["teal"])
    label(ax, 0.875, 0.415, "HIGH", fs=7, color=COL["red"])

    # Transition amortization.
    box(ax, 0.43, 0.18, 0.14, 0.06, "$L_{tr}$ transition", COL["orange_l"], COL["orange"], fs=7, radius=0.01)
    ax.plot([0.43, 0.56], [0.17, 0.17], color=COL["orange"], linewidth=3)
    ax.plot([0.56, 0.61], [0.17, 0.17], color=COL["red"], linewidth=3)
    label(ax, 0.49, 0.115, "hidden by copy/wait/slack", fs=7, color=COL["orange"])
    label(ax, 0.60, 0.115, "visible", fs=7, color=COL["red"])
    save(fig, "theory_dvfs_timeline.pdf")


def fig_runtime_pipeline():
    fig, ax = setup(7.8, 3.5)
    ax.add_patch(Rectangle((0.03, 0.55), 0.61, 0.33, facecolor=COL["blue_l"], edgecolor="none", alpha=0.45))
    ax.add_patch(Rectangle((0.36, 0.13), 0.51, 0.31, facecolor=COL["teal_l"], edgecolor="none", alpha=0.45))
    ax.add_patch(Rectangle((0.76, 0.55), 0.18, 0.33, facecolor=COL["orange_l"], edgecolor="none", alpha=0.45))
    label(ax, 0.06, 0.85, "placement path", fs=7.5, weight="bold", color=COL["blue"], ha="left")
    label(ax, 0.39, 0.40, "DVFS path", fs=7.5, weight="bold", color=COL["teal"], ha="left")
    label(ax, 0.79, 0.85, "diagnostics", fs=7.5, weight="bold", color=COL["orange"], ha="left")

    boxes = [
        (0.05, 0.66, 0.10, 0.09, "Ready\ntask", COL["gray_l"]),
        (0.18, 0.66, 0.12, 0.09, "Evaluate\nGPUs", COL["blue_l"]),
        (0.33, 0.66, 0.10, 0.09, "HEFT\n$g_0$", COL["blue_l"]),
        (0.46, 0.66, 0.12, 0.09, "Residual\ngate", COL["blue_l"]),
        (0.61, 0.66, 0.10, 0.09, "GPU\n$g^*$", COL["violet_l"]),
        (0.05, 0.23, 0.13, 0.09, "Update\nready + residency", COL["gray_l"]),
        (0.38, 0.23, 0.12, 0.09, "DVFS\nproposer", COL["teal_l"]),
        (0.53, 0.23, 0.12, 0.09, "Per-GPU\nwindow", COL["teal_l"]),
        (0.68, 0.23, 0.12, 0.09, "Committer\n+ guardrails", COL["teal_l"]),
        (0.83, 0.23, 0.11, 0.09, "Frequency\nannotation", COL["teal_l"]),
        (0.79, 0.66, 0.12, 0.09, "Trace\nlogs", COL["orange_l"]),
    ]
    for b in boxes:
        box(ax, *b, ec=COL["ink"], fs=7.0, radius=0.012)
    for x1, y1, x2, y2 in [
        (0.15, 0.705, 0.18, 0.705),
        (0.30, 0.705, 0.33, 0.705),
        (0.43, 0.705, 0.46, 0.705),
        (0.58, 0.705, 0.61, 0.705),
        (0.66, 0.66, 0.66, 0.32),
        (0.18, 0.275, 0.38, 0.275),
        (0.50, 0.275, 0.53, 0.275),
        (0.65, 0.275, 0.68, 0.275),
        (0.80, 0.275, 0.83, 0.275),
        (0.71, 0.705, 0.79, 0.705),
    ]:
        arrow(ax, x1, y1, x2, y2, COL["ink"], lw=1.0)
    arrow(ax, 0.61, 0.66, 0.18, 0.29, COL["muted"], lw=0.9, rad=-0.2)
    label(ax, 0.30, 0.44, "state feeds the next task", fs=7, color=COL["muted"])
    save(fig, "methods_runtime_pipeline.pdf")


def fig_residual_flow():
    fig, ax = setup(7.0, 3.9)
    box(ax, 0.37, 0.86, 0.26, 0.07, "Ready task $t$", COL["gray_l"], fs=8)
    box(ax, 0.31, 0.73, 0.38, 0.08, "Select profile $p_W$ and evaluate all GPUs", COL["blue_l"], COL["blue"], fs=7.5)
    box(ax, 0.31, 0.60, 0.38, 0.08, "Choose HEFT baseline $g_0$ and compute $q(t)$", COL["blue_l"], COL["blue"], fs=7.5)
    diamond(ax, 0.50, 0.46, 0.36, 0.11, "$q(t)>\\theta_q$?", COL["violet_l"], COL["violet"], fs=7.3)
    box(ax, 0.08, 0.34, 0.27, 0.08, "Critical gate\nsmall $\\delta$, high $\\tau$", COL["teal_l"], COL["teal"], fs=7)
    box(ax, 0.65, 0.34, 0.27, 0.08, "Non-critical gate\nlarger $\\delta$, lower $\\tau$", COL["blue_l"], COL["blue"], fs=7)
    box(ax, 0.28, 0.21, 0.44, 0.075, "Filter non-HEFT candidates with $\\rho_F\\leq\\delta$ and $\\rho_K\\geq\\tau$", COL["orange_l"], COL["orange"], fs=7.0)
    diamond(ax, 0.50, 0.105, 0.34, 0.095, "Feasible set empty?", COL["orange_l"], COL["orange"], fs=7.2)
    box(ax, 0.05, 0.04, 0.26, 0.07, "Fallback to HEFT\n$g^*=g_0$", COL["gray_l"], COL["ink"], fs=7.2)
    box(ax, 0.69, 0.04, 0.26, 0.07, "Choose max score\n$g^*=\\arg\\max H(t,g)$", COL["green_l"], COL["green"], fs=7.2)

    for x1, y1, x2, y2 in [
        (0.50, 0.86, 0.50, 0.81),
        (0.50, 0.73, 0.50, 0.68),
        (0.50, 0.60, 0.50, 0.515),
        (0.39, 0.46, 0.22, 0.42),
        (0.61, 0.46, 0.78, 0.42),
        (0.22, 0.34, 0.42, 0.285),
        (0.78, 0.34, 0.58, 0.285),
        (0.50, 0.21, 0.50, 0.153),
        (0.38, 0.105, 0.27, 0.105),
        (0.62, 0.105, 0.73, 0.105),
    ]:
        arrow(ax, x1, y1, x2, y2, COL["ink"], lw=0.9)
    label(ax, 0.32, 0.45, "yes", fs=7, color=COL["teal"])
    label(ax, 0.68, 0.45, "no", fs=7, color=COL["blue"])
    label(ax, 0.34, 0.14, "yes", fs=7, color=COL["muted"])
    label(ax, 0.66, 0.14, "no", fs=7, color=COL["muted"])

    box(ax, 0.04, 0.18, 0.18, 0.075, "copy-only score:\n$H(t,g)=\\rho_K(t,g)$", COL["gray_l"], COL["ink"], fs=6.8)
    box(ax, 0.78, 0.18, 0.18, 0.075, "HEFT remains\nsafe fallback", COL["gray_l"], COL["ink"], fs=6.8)
    save(fig, "methods_residual_decision_flow.pdf")


def fig_bandit_loop():
    fig, ax = setup(7.3, 3.5)
    box(ax, 0.05, 0.60, 0.17, 0.10, "Completed\nwindow stats", COL["gray_l"], fs=7.5)
    box(ax, 0.29, 0.60, 0.18, 0.10, "Context vector\n$x(W)$", COL["blue_l"], COL["blue"], fs=7.5)
    box(ax, 0.54, 0.60, 0.17, 0.10, "LinUCB\nscores", COL["blue_l"], COL["blue"], fs=7.5)
    box(ax, 0.78, 0.60, 0.16, 0.10, "Gate profile\nfor next window", COL["violet_l"], COL["violet"], fs=7.2)
    box(ax, 0.57, 0.23, 0.18, 0.10, "Residual gate\nexecutes tasks", COL["green_l"], COL["green"], fs=7.5)
    box(ax, 0.31, 0.23, 0.17, 0.10, "Relative\nreward", COL["orange_l"], COL["orange"], fs=7.5)
    box(ax, 0.06, 0.23, 0.16, 0.10, "Update\nactive arm", COL["orange_l"], COL["orange"], fs=7.5)

    for x1, y1, x2, y2 in [
        (0.22, 0.65, 0.29, 0.65),
        (0.47, 0.65, 0.54, 0.65),
        (0.71, 0.65, 0.78, 0.65),
        (0.86, 0.60, 0.70, 0.33),
        (0.57, 0.28, 0.48, 0.28),
        (0.31, 0.28, 0.22, 0.28),
        (0.14, 0.33, 0.10, 0.60),
    ]:
        arrow(ax, x1, y1, x2, y2, COL["ink"], lw=1.0, rad=0.0 if x1 < x2 else 0.12)

    label(ax, 0.38, 0.82, "$\\overline{q}$, $\\phi_{high}$, $\\overline{K}_0$, $\\overline{B}_{in}$,\n$\\overline{d}$, $\\overline{C}$, $\\overline{L}_{imb}$, $\\phi_{dev}$", fs=7, color=COL["muted"])
    label(ax, 0.63, 0.48, "default / aggressive\nprofile scores", fs=7, color=COL["muted"])
    box(ax, 0.74, 0.13, 0.22, 0.105, "Bandit selects a\nprofile, not a GPU.", COL["red_l"], COL["red"], fs=7.2, weight="bold")
    label(ax, 0.23, 0.12, "$r^{rel}=r^{active}-r^{default}$", fs=7.5, color=COL["orange"])
    save(fig, "methods_bandit_window_loop.pdf")


def fig_dvfs_state_machine():
    fig, ax = setup(7.7, 4.2)
    ax.add_patch(Rectangle((0.03, 0.12), 0.40, 0.78, facecolor=COL["teal_l"], edgecolor="none", alpha=0.35))
    ax.add_patch(Rectangle((0.50, 0.12), 0.45, 0.78, facecolor=COL["blue_l"], edgecolor="none", alpha=0.35))
    label(ax, 0.07, 0.86, "Task-level proposer", fs=8.5, weight="bold", color=COL["teal"], ha="left")
    label(ax, 0.54, 0.86, "Per-GPU committer", fs=8.5, weight="bold", color=COL["blue"], ha="left")

    box(ax, 0.07, 0.72, 0.28, 0.08, "task features:\ncriticality, cost, wait, slack", COL["gray_l"], fs=7)
    diamond(ax, 0.21, 0.58, 0.24, 0.10, "force HIGH?", COL["red_l"], COL["red"], fs=7.2)
    diamond(ax, 0.21, 0.43, 0.26, 0.10, "lower level\neligible?", COL["teal_l"], COL["teal"], fs=7.2)
    box(ax, 0.07, 0.24, 0.12, 0.07, "HIGH\nintent", COL["gray_l"], fs=7)
    box(ax, 0.23, 0.24, 0.12, 0.07, "MID/LOW\nintent", COL["green_l"], COL["green"], fs=7)
    arrow(ax, 0.21, 0.72, 0.21, 0.63, COL["ink"])
    arrow(ax, 0.21, 0.53, 0.13, 0.31, COL["red"], rad=0.2)
    arrow(ax, 0.21, 0.53, 0.21, 0.48, COL["ink"])
    arrow(ax, 0.16, 0.39, 0.13, 0.31, COL["ink"])
    arrow(ax, 0.26, 0.39, 0.29, 0.31, COL["green"])

    # State machine.
    box(ax, 0.56, 0.62, 0.14, 0.09, "HIGH", COL["gray_l"], COL["ink"], fs=8, weight="bold")
    box(ax, 0.75, 0.62, 0.14, 0.09, "MID", COL["green_l"], COL["green"], fs=8, weight="bold")
    box(ax, 0.75, 0.36, 0.14, 0.09, "LOW", COL["orange_l"], COL["orange"], fs=8, weight="bold")
    arrow(ax, 0.70, 0.665, 0.75, 0.665, COL["green"], lw=1.2)
    arrow(ax, 0.82, 0.62, 0.82, 0.45, COL["orange"], lw=1.2)
    arrow(ax, 0.75, 0.405, 0.64, 0.62, COL["red"], lw=1.2, rad=0.25)
    arrow(ax, 0.75, 0.62, 0.64, 0.62, COL["red"], lw=1.0, rad=-0.35)
    label(ax, 0.73, 0.72, "consecutive\neligible windows", fs=6.8, color=COL["green"])
    label(ax, 0.91, 0.51, "stricter\neligibility", fs=6.8, color=COL["orange"])
    label(ax, 0.62, 0.49, "guardrail,\nbacklog,\ncritical mass", fs=6.8, color=COL["red"])

    box(ax, 0.53, 0.18, 0.39, 0.10, "Current task uses the already committed level;\nnew votes affect a later window.", COL["gray_l"], COL["ink"], fs=7.2)
    arrow(ax, 0.35, 0.275, 0.53, 0.23, COL["ink"], lw=1.0)
    label(ax, 0.45, 0.31, "weighted votes\nper GPU", fs=7, color=COL["muted"])
    save(fig, "methods_dvfs_state_machine.pdf")


def main():
    fig_task_residency()
    fig_residual_gate()
    fig_dvfs_timeline()
    fig_runtime_pipeline()
    fig_residual_flow()
    fig_bandit_loop()
    fig_dvfs_state_machine()


if __name__ == "__main__":
    main()
