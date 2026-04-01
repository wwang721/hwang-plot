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

windows = [7, 14, 30]
win_colors = ['#9ECAE1', '#4292C6', '#08519C']   # light→dark blue (7→14→30 day)
RAW_COLOR  = '#CCCCCC'   # light grey for raw data

datasets = [
    ('2025TRAINCOD_rolling_mean_std_7_14_30.csv',  'CODMBR',  r'$\mathrm{COD_{MBR}}$ (mg/L)'),
    ('2025TRAINNH3N_rolling_mean_std_7_14_30.csv', 'NH3NMBR', r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$ (mg/L)'),
]
panel_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

for ds_idx, (filename, target, ylabel) in enumerate(datasets):
    df = pd.read_csv(f"./data/1/{filename}")
    time = pd.to_datetime(df['Date'])

    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
    ax_mean, ax_std = axes

    # Rolling mean
    ax_mean.plot(time, df[target], color=RAW_COLOR, lw=0.7, alpha=0.7, label='Raw')
    for w, c in zip(windows, win_colors):
        col = f"{target}_rolling_mean_{w}"
        ax_mean.plot(time, df[col], color=c, lw=1.4, label=f'{w}-day mean')
    ax_mean.set_ylabel(f'Rolling mean\n{ylabel}', labelpad=5)
    ax_mean.set_xticklabels([])
    ax_mean.legend(ncol=4, frameon=False, fontsize=12)
    ax_mean.set_xlim(time.min(), time.max())

    # Rolling std (filled)
    for w, c in zip(windows, win_colors):
        col = f"{target}_rolling_std_{w}"
        ax_std.plot(time, df[col], color=c, lw=1.2, label=f'{w}-day std')
    ax_std.set_ylabel(f'Rolling std\n{ylabel}', labelpad=5)
    ax_std.set_xlabel('Date', labelpad=5)
    ax_std.legend(ncol=3, frameon=False, fontsize=12)
    ax_std.set_xlim(time.min(), time.max())

    base = ds_idx * 2
    ax_mean.text(-0.05, 1.08, panel_labels[base],     transform=ax_mean.transAxes, fontsize=15, va='top', ha='right')
    ax_std.text( -0.05, 1.08, panel_labels[base + 1], transform=ax_std.transAxes,  fontsize=15, va='top', ha='right')

    plt.subplots_adjust(hspace=0.12)
    fname = f"figs/1_{target}_rolling.png"
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {fname}")
