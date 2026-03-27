import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from matplotlib.transforms import blended_transform_factory

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

# (filename, display label, is_tcan)
models = [
    ('COD-naive',          'Naive Baseline',   False),
    ('COD-ridge',          'Ridge Regression', False),
    ('COD-weighted',       'Weighted Average', False),
    ('COD-lstm',           'LSTM',             False),
    ('COD-TACN-ATTENTION', 'TCAN-Attention',   True),
]
model_colors = ['C0', 'C1', 'C2', 'C3', 'C4']

alpha = 0.8
lw = 1.1

for it, (fname, label, is_tcan) in enumerate(models):
    df = pd.read_csv(f"./data/1/{fname}.csv")

    if is_tcan:
        time     = pd.to_datetime(df['target_date'])
        y_true   = df['actual']
        y_pred   = df['blend_pred']
        residual = df['residual']
        split    = df['dataset_part']
    else:
        time     = pd.to_datetime(df['time_col_std'])
        y_true   = df['y_true_std']
        y_pred   = df['y_pred_std']
        residual = df['residual']
        split    = df['dataset']

    test_mask  = split == 'test'
    test_start = time[test_mask].iloc[0]
    train_mid  = time.iloc[0] + (time[~test_mask].iloc[-1] - time.iloc[0]) / 2
    test_mid   = test_start + (time.iloc[-1] - test_start) / 2

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 5))

    # --- top panel: true (gray line) + predicted (colored dots) ---
    ax1.plot(time, y_true, color='gray', lw=lw, alpha=alpha, label='Measured', zorder=2)
    ax1.plot(time, y_pred, '.', color=model_colors[it], markersize=2,
             alpha=alpha, label=label, clip_on=False, zorder=3)
    ax1.axvline(x=test_start, color='k', linestyle='--', lw=0.8, alpha=0.8)

    trans = blended_transform_factory(ax1.transData, ax1.transAxes)
    ax1.text(train_mid, 0.96, 'Training', transform=trans, ha='center', va='top', fontsize=11)
    ax1.text(test_mid,  0.96, 'Test',     transform=trans, ha='center', va='top', fontsize=11)

    # --- bottom panel: residuals ---
    ax2.plot(time, residual, color=model_colors[it], lw=lw * 0.8, alpha=alpha)
    ax2.fill_between(time, residual, 0, color=model_colors[it], alpha=0.2)
    ax2.axhline(y=0, color='k', linestyle='--', lw=0.8, alpha=0.8)
    ax2.axvline(x=test_start, color='k', linestyle='--', lw=0.8, alpha=0.8)

    ax1.set_xticklabels([])
    ax1.set_ylabel(r'$\mathrm{COD_{MBR}}$ (mg/L)', labelpad=12)
    ax2.set_ylabel('Residual (mg/L)', labelpad=12)
    ax2.set_xlabel('Date', labelpad=5)

    ax1.set_ylim(bottom=0)

    ticks = ax1.get_xticks()
    xlim = (time.min() - pd.Timedelta(days=31), time.max() + pd.Timedelta(days=31))
    for ax in (ax1, ax2):
        ax.set_xlim(*xlim)
        ax.set_xticks(ticks)

    ax1.legend(ncol=2, frameon=False)

    ax1.text(-0.05, 1.10, '(a)', transform=ax1.transAxes, fontsize=15, va='top', ha='right')
    ax2.text(-0.05, 1.10, '(b)', transform=ax2.transAxes, fontsize=15, va='top', ha='right')

    plt.subplots_adjust(hspace=0.15)
    plt.savefig(f"figs/1_{fname}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
