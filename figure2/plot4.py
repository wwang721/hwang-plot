import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()


methods = ['Savgol', 'Hampel', 'STL', 'Wavelet-strong']
method_colors = ['C3', 'C4', 'C1', 'C2']

alpha = 0.8
lw = 1.1

for it, method in enumerate(methods):
    fig, axes = plt.subplots(3, 1, figsize=(12, 5))

    ax1, ax2, ax3 = axes.flatten()

    # Load CSV
    df = pd.read_csv(f"./data/4/{method}.csv")

    time = pd.to_datetime(df.iloc[:, 0])
    value_names = ['Date', r'$\mathrm{COD_{MBR}}$', 'Raw', method]

    idx = 0

    ax1.plot(time, df.iloc[:, 1], clip_on=False, color='C0', label=df.columns[1], alpha=alpha, lw=lw)
    ax2.plot(time, df.iloc[:, 2], clip_on=False, color='C0', label=df.columns[2], alpha=alpha, lw=lw)
    ax3.plot(time, df.iloc[:, 3], clip_on=False, color='C0', label=df.columns[3], alpha=alpha, lw=lw)


    ax3.axhline(y=0, color='k', linestyle='--', alpha=0.6, lw=lw)

    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ax1.set_ylabel(df.columns[1] if df.columns[1] != 'NH3NMBR' else r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$')
    ax2.set_ylabel(df.columns[2] if df.columns[2] != 'NH3NMBR' else r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$', labelpad=8)
    ax3.set_ylabel(df.columns[3] if df.columns[3] != 'NH3NMBR' else r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$')
    ax3.set_xlabel(df.columns[0], labelpad=5)

    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    ticks = ax1.get_xticks()

    ax1.set_xlim(left=time.min()-pd.Timedelta(days=31), right=time.max()+pd.Timedelta(days=31))
    ax2.set_xlim(left=time.min()-pd.Timedelta(days=31), right=time.max()+pd.Timedelta(days=31))
    ax3.set_xlim(left=time.min()-pd.Timedelta(days=31), right=time.max()+pd.Timedelta(days=31))
    ax1.set_xticks(ticks)
    ax2.set_xticks(ticks)
    ax3.set_xticks(ticks)

    # ax1.legend(ncol=2, frameon=False)
    # ax2.legend(ncol=3, frameon=False)
    # ax3.legend(ncol=2, frameon=False)
    # ax.grid(True, alpha=0.2)

    ax1.text(-0.05, 1.10, '(a)', transform=ax1.transAxes, fontsize=15, va='top', ha='right')
    ax2.text(-0.05, 1.10, '(b)', transform=ax2.transAxes, fontsize=15, va='top', ha='right')
    ax3.text(-0.05, 1.10, '(c)', transform=ax3.transAxes, fontsize=15, va='top', ha='right')

    plt.subplots_adjust(
        # wspace=0.12,   # width space between columns
        hspace=0.15   # height space between rows
    )
    # plt.show()
    plt.savefig(f"figs/4_{method}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
