import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()


methods = ['Diff1', 'Hampel', 'STL', 'Wavelet-strong']
method_colors = ['C3', 'C4', 'C1', 'C2']

alpha = 0.8
lw = 1.1

for it, method in enumerate(methods):
    fig, axes = plt.subplots(2, 1, figsize=(12, 5))

    ax1, ax2 = axes.flatten()

    # Load CSV
    df = pd.read_csv(f"./data/1/{method}.csv")

    time = pd.to_datetime(df.iloc[:, 0])
    value_names = ['Date', r'$\mathrm{COD_{MBR}}$', method, 'Upper threshold', 'Lower threshold', f'{method} flag']

    idx = 0

    colors = ['C0', 'C2', 'C3']
    linestyles = ['-', '--', '--']
    for idx in range(4):
        value = df.iloc[:, idx + 1]
        value_name = value_names[idx + 1]
        if idx == 0:
            ax1.plot(time, value, clip_on=False, color='C0', label=r'Raw $\mathrm{COD_{MBR}}$', alpha=alpha, lw=lw)
        else:
            ax2.plot(time, value, linestyles[idx-1], clip_on=False, color=colors[idx-1], label=value_name, alpha=alpha, lw=lw)

    idx = 4
    value_name = value_names[idx + 1]
    mask = df.iloc[:, idx + 1] == 1
    ax1.plot(time[mask], df.loc[mask, df.columns[1]], 'o', color=method_colors[it], markersize=3, label=value_name, clip_on=False)

    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.6, lw=lw)

    ax1.set_xticklabels([])
    ax2.set_xlabel(value_names[0], labelpad=5)
    ax1.set_ylabel(value_names[1], labelpad=12)
    ax2.set_ylabel('Score + thresholds')

    ax1.set_ylim(bottom=0)

    ticks = ax1.get_xticks()

    ax1.set_xlim(left=time.min()-pd.Timedelta(days=31), right=time.max()+pd.Timedelta(days=31))
    ax2.set_xlim(left=time.min()-pd.Timedelta(days=31), right=time.max()+pd.Timedelta(days=31))
    ax1.set_xticks(ticks)
    ax2.set_xticks(ticks)

    ax1.legend(ncol=2, frameon=False)
    ax2.legend(ncol=3, frameon=False)
    # ax.grid(True, alpha=0.2)

    ax1.text(-0.05, 1.10, '(a)', transform=ax1.transAxes, fontsize=15, va='top', ha='right')
    ax2.text(-0.05, 1.10, '(b)', transform=ax2.transAxes, fontsize=15, va='top', ha='right')

    plt.subplots_adjust(
        # wspace=0.12,   # width space between columns
        hspace=0.15   # height space between rows
    )
    # plt.show()
    plt.savefig(f"figs/1_{method}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
