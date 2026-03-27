import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

# (filename, acf/pacf column name, y-axis label, subplot title, panel label)
plots = [
    ('subtrain_raw_target_acf_plot.csv',   'acf',  'Autocorrelation',         r'ACF of Subtrain Raw Target Series ($\mathrm{COD_{MBR}}$)',         '(a)'),
    ('subtrain_raw_target_pacf_plot.csv',  'pacf', 'Partial Autocorrelation', r'PACF of Subtrain Raw Target Series ($\mathrm{COD_{MBR}}$)',        '(b)'),
    ('subtrain_target_diff1_acf_plot.csv', 'acf',  'Autocorrelation',         r'ACF of Subtrain Diff-1 Target Series ($\mathrm{COD_{MBR}}$)',  '(c)'),
    ('subtrain_target_diff1_pacf_plot.csv','pacf', 'Partial Autocorrelation', r'PACF of Subtrain Diff-1 Target Series ($\mathrm{COD_{MBR}}$)', '(d)'),
]

fig, axes = plt.subplots(2, 2, figsize=(14, 7))

for ax, (fname, col, ylabel, title, panel_label) in zip(axes.flatten(), plots):
    df = pd.read_csv(f"./data/3/{fname}")
    lags   = df['lag'].values
    values = df[col].values
    ci_low = df['ci_low'].values
    ci_high= df['ci_high'].values

    # Symmetric CI half-width (significance boundary centered at 0)
    ci_half = (ci_high - ci_low) / 2

    # Stem plot
    markerline, stemlines, baseline = ax.stem(lags, values, linefmt='C0-', markerfmt='C0o', basefmt='C0-')
    plt.setp(stemlines,   lw=0.8)
    plt.setp(markerline,  markersize=4)
    plt.setp(baseline,    lw=0.8)

    # Confidence interval shading (skip lag 0 where ci_half=0)
    mask = lags > 0
    ax.fill_between(lags[mask], -ci_half[mask], ci_half[mask], alpha=0.15, color='C0')

    ax.set_xlabel('Lag', labelpad=5)
    ax.set_ylabel(ylabel, labelpad=8)
    ax.set_title(title)
    ax.grid(True, alpha=0.2, axis='y')
    ax.text(-0.05, 1.10, panel_label, transform=ax.transAxes, fontsize=15, va='top', ha='right')

plt.subplots_adjust(hspace=0.45, wspace=0.28)
plt.savefig("figs/3_COD_acf_pacf.png", dpi=300, bbox_inches='tight')
plt.close(fig)
