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
    'II_2_O': 'II-2-O',
    'II_2_M': 'II-2-M',
    'II_1_O': 'II-1-O',
    'II_1_M': 'II-1-M',
}
SAMPLES = list(SAMPLE_LABELS.keys())

# Keep top N taxa (including Others bucket)
TOP_N = 12

# Carefully chosen palette: muted, harmonious, inspired by scientific journals
TAXON_COLORS = [
    '#6BAF75',  # sage green
    '#5B8DB8',  # steel blue
    '#E07B54',  # terracotta
    '#8B6FAE',  # soft purple
    '#D4A84B',  # warm gold
    '#5BA8A0',  # muted teal
    '#C95F6E',  # dusty rose
    '#7A9E7E',  # fern green
    '#B07B4F',  # warm brown
    '#5F8DBF',  # cornflower blue
    '#A8A45A',  # olive
    '#9E7B9B',  # mauve
    '#6AABB8',  # sky teal
    '#D4865A',  # warm sienna
    '#7CA46B',  # medium green
]


def strip_prefix(name):
    """Remove taxonomic prefix (p_, g_, etc.) for cleaner legend labels."""
    for prefix in ('p_', 'g_', 'f_', 'o_', 'c_', 'k_'):
        if name.lower().startswith(prefix):
            return name[2:]
    return name


def plot_stacked_bar(ax, df, colors):
    x = np.arange(len(SAMPLES))
    bottom = np.zeros(len(SAMPLES))

    for i, (taxon, row) in enumerate(df.iterrows()):
        vals = row[SAMPLES].values.astype(float) * 100  # to percent
        ax.bar(x, vals, bottom=bottom, color=colors[i],
               width=0.55, edgecolor='white', linewidth=0.5)
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels([SAMPLE_LABELS[s] for s in SAMPLES], fontsize=10)
    ax.set_ylabel('Relative abundance (%)', labelpad=5)
    ax.set_ylim(0, 100)
    ax.set_xlabel('Sample', labelpad=5)

    return colors


def load_and_trim(filepath):
    df = pd.read_csv(filepath, comment='#', header=0)
    df.columns = [df.columns[0]] + SAMPLES
    df = df.set_index(df.columns[0])
    # sort by mean abundance descending
    df['_mean'] = df[SAMPLES].mean(axis=1)
    df = df.sort_values('_mean', ascending=False).drop(columns='_mean')
    # pool tail into Others (skip if row already named Others)
    named = df[df.index != 'Others']
    already_others = df[df.index == 'Others']
    if len(named) > TOP_N - 1:
        top = named.iloc[:TOP_N - 1]
        tail_sum = named.iloc[TOP_N - 1:][SAMPLES].sum(axis=0)
        if not already_others.empty:
            tail_sum = tail_sum + already_others.iloc[0][SAMPLES].values
        others_row = tail_sum.to_frame().T
        others_row.index = ['Others']
        df = pd.concat([top, others_row])
    elif not already_others.empty:
        df = pd.concat([named, already_others])
    else:
        df = named
    return df


for level, filepath, outname in [
    ('phylum', './data/5/phylum.csv', '5_phylum'),
    ('genus',  './data/5/genus.csv',  '5_genus'),
]:
    df = load_and_trim(filepath)
    colors = TAXON_COLORS[:len(df)]

    fig, ax = plt.subplots(figsize=(6, 5))
    plot_stacked_bar(ax, df, colors)

    # Legend with cleaned taxon names
    handles = [
        mpatches.Patch(color=colors[i], label=strip_prefix(taxon))
        for i, taxon in enumerate(df.index)
    ]
    ax.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left',
              frameon=False, fontsize=8, ncol=1, handlelength=1.2, handleheight=1.0)

    plt.tight_layout()
    plt.savefig(f"figs/{outname}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved figs/{outname}.png")
