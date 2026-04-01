import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

SAMPLE_LABELS = {
    'II_2_O': '2024-O',
    'II_2_M': '2024-M',
    'II_1_O': '2025-O',
    'II_1_M': '2025-M',
}
SAMPLES = list(SAMPLE_LABELS.keys())

def make_palette(n):
    """Microbiome-style palette: high-abundance = distinctive warm/saturated,
    low-abundance = lighter/cooler, Others = grey."""
    colors = [
        '#7CB97C',  # sage green       (most abundant)
        '#4A90C4',  # steel blue
        '#E8875A',  # orange
        '#9B6BB5',  # purple
        '#F2C94C',  # yellow
        '#5BB8A8',  # teal
        '#E85C6E',  # coral red
        '#6AAF8A',  # medium green
        '#D4845A',  # sienna
        '#5A8FC4',  # cornflower
        '#C4A85A',  # warm tan
        '#B07AAE',  # mauve
        '#72B8C8',  # sky blue
        '#E8A05A',  # amber
        '#8CB87C',  # light green
        '#7A6BB5',  # periwinkle
        '#D4C87C',  # pale gold
        '#E87C9B',  # pink
        '#5A9B8A',  # dark teal
        '#A8784A',  # brown
        '#8CB4D4',  # powder blue
        '#C87C5A',  # terracotta
        '#9AC47C',  # lime green
        '#6A8AB5',  # dusty blue
        '#D4A87C',  # peach
        '#5A7A9B',  # slate
        '#B4C87C',  # yellow-green
        '#A87CA8',  # lilac
        '#7AAAD4',  # light blue
        '#C8B47C',  # straw
        '#E8D87A',  # warm yellow (Others)
    ]
    return colors[:n]


def strip_prefix(name):
    """Remove taxonomic prefix (p_, g_, etc.) for cleaner legend labels."""
    for prefix in ('p_', 'g_', 'f_', 'o_', 'c_', 'k_'):
        if name.lower().startswith(prefix):
            return name[2:]
    return name


def plot_stacked_bar(ax, df, colors):
    BAR_W = 0.55
    GAP   = 1 - BAR_W          # space between bars
    x = np.arange(len(SAMPLES))

    # Store per-taxon bottoms and tops for flow polygons
    all_bottoms = np.zeros((len(df), len(SAMPLES)))
    all_tops    = np.zeros((len(df), len(SAMPLES)))
    cum = np.zeros(len(SAMPLES))

    for i, (taxon, row) in enumerate(df.iterrows()):
        vals = row[SAMPLES].values.astype(float) * 100
        all_bottoms[i] = cum.copy()
        all_tops[i]    = cum + vals
        ax.bar(x, vals, bottom=cum, color=colors[i], width=BAR_W, edgecolor='none')
        cum += vals

    # Draw alluvial flow polygons between adjacent bars
    from matplotlib.patches import Polygon
    from matplotlib.collections import PatchCollection
    half = BAR_W / 2
    n_samples = len(SAMPLES)
    for i in range(len(df)):
        c = colors[i]
        for j in range(n_samples - 1):
            x0_r = x[j]     + half          # right edge of bar j
            x1_l = x[j + 1] - half          # left  edge of bar j+1
            b0, t0 = all_bottoms[i, j],     all_tops[i, j]
            b1, t1 = all_bottoms[i, j + 1], all_tops[i, j + 1]
            # cubic bezier-like via fill_between on a fine x grid
            t_vals = np.linspace(0, 1, 60)
            # smooth interpolation using a cosine ease
            s = (1 - np.cos(t_vals * np.pi)) / 2
            x_seg   = x0_r + (x1_l - x0_r) * t_vals
            bot_seg = b0   + (b1   - b0)    * s
            top_seg = t0   + (t1   - t0)    * s
            ax.fill_between(x_seg, bot_seg, top_seg,
                            color=c, alpha=0.35, linewidth=0, zorder=0)

    ax.set_xticks(x)
    ax.set_xticklabels([SAMPLE_LABELS[s] for s in SAMPLES], fontsize=10)
    ax.set_ylabel('Relative abundance (%)', labelpad=5)
    ax.set_ylim(0, 100)
    ax.set_xlabel('Sample', labelpad=5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(top=False, right=False, direction='out')

    return colors


def load_all(filepath):
    df = pd.read_csv(filepath)
    df.columns = [df.columns[0].lstrip('#')] + SAMPLES
    df = df.set_index(df.columns[0])
    # sort by mean abundance descending, Others always last
    others = df[df.index == 'Others']
    rest   = df[df.index != 'Others']
    rest = rest.copy()
    rest['_mean'] = rest[SAMPLES].mean(axis=1)
    rest = rest.sort_values('_mean', ascending=False).drop(columns='_mean')
    return pd.concat([rest, others]) if not others.empty else rest


for level, filepath, outname in [
    ('phylum', './data/5/phylum.csv', '5_phylum'),
    ('genus',  './data/5/genus.csv',  '5_genus'),
]:
    df = load_all(filepath)
    colors = make_palette(len(df))

    fig, ax = plt.subplots(figsize=(7, 5))
    plot_stacked_bar(ax, df, colors)

    # Legend with cleaned taxon names
    handles = [
        mpatches.Patch(color=colors[i], label=strip_prefix(taxon))
        for i, taxon in enumerate(df.index)
    ]
    ax.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left',
              frameon=False, fontsize=8, ncol=2, handlelength=1.2, handleheight=1.0)

    plt.tight_layout()
    plt.savefig(f"figs/{outname}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved figs/{outname}.png")
