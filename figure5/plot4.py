import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

PURPLE = '#7B2D8B'
PURPLE_LIGHT = '#C084D4'
RESID_COLOR = '#9B59B6'

datasets = [
    (
        'cod_test_only_timeseries_plot_data_r2_081.csv',
        'Measured_CODMBR', 'Predicted_CODMBR', 'Residual',
        r'$\mathrm{COD_{MBR}}$ (mg/L)',
        '4_COD',
    ),
    (
        'nh3n_test_only_timeseries_plot_data_r2_064.csv',
        'Measured_NH3NMBR', 'Predicted_NH3NMBR', 'Residual',
        r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$ (mg/L)',
        '4_NH3N',
    ),
]

for (filename, meas_col, pred_col, resid_col, ylabel, outname) in datasets:
    df = pd.read_csv(f"./data/4/{filename}")
    time = pd.to_datetime(df['X'])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

    # ── (a) Measured vs Predicted ──
    ax1.plot(time, df[meas_col], color=PURPLE,       lw=1.3, alpha=0.85, label='Measured')
    ax1.plot(time, df[pred_col], color=PURPLE_LIGHT, lw=1.3, alpha=0.85, linestyle='--', label='Predicted')
    ax1.set_ylabel(ylabel, labelpad=5)
    ax1.set_xticklabels([])
    ax1.legend(frameon=False, ncol=2)
    ax1.set_xlim(time.min(), time.max())

    # ── (b) Residuals ──
    ax2.bar(time, df[resid_col], color=RESID_COLOR, alpha=0.7, width=0.8)
    ax2.axhline(0, color='k', lw=0.8, linestyle='--', alpha=0.5)
    ax2.set_ylabel('Residual', labelpad=5)
    ax2.set_xlabel('Date', labelpad=5)
    ax2.set_xlim(time.min(), time.max())

    ax1.text(-0.05, 1.08, '(a)', transform=ax1.transAxes, fontsize=15, va='top', ha='right')
    ax2.text(-0.05, 1.08, '(b)', transform=ax2.transAxes, fontsize=15, va='top', ha='right')

    plt.subplots_adjust(hspace=0.12)
    plt.savefig(f"figs/{outname}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved figs/{outname}.png")
