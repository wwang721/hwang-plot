import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from glob import glob
from scipy.stats import gaussian_kde

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

models = ['COD-NAIVE', 'COD-RIDGE', 'COD-WEIGHTED', 'COD-LSTM', 'COD-TCAN']
model_labels = {
    'COD-NAIVE':    'Naive Baseline',
    'COD-RIDGE':    'Ridge Regression',
    'COD-WEIGHTED': 'Weighted Average',
    'COD-LSTM':     'LSTM',
    'COD-TCAN':     'TCAN-Attention',
}

hist_color = '#E88080'   # salmon-red, matching example image
kde_color  = 'C3'
qq_color   = 'C0'
ref_color  = 'C3'


def find_file(folder, *patterns):
    """Return first file in folder matching any of the glob patterns."""
    for pat in patterns:
        matches = glob(str(Path(folder) / pat))
        if matches:
            return matches[0]
    raise FileNotFoundError(f"No file matching {patterns} in {folder}")


def plot_histogram(ax, csv_path, title):
    df = pd.read_csv(csv_path)
    if 'bin_left' in df.columns:
        # Pre-binned format
        centers = (df['bin_left'] + df['bin_right']) / 2
        widths  = df['bin_right'] - df['bin_left']
        counts  = df['count'].values
        ax.bar(centers, counts, width=widths, color=hist_color, edgecolor=hist_color, alpha=0.85)
        synthetic = np.repeat(centers.values, counts.astype(int))
    else:
        # Raw residuals format
        synthetic = df.iloc[:, 0].dropna().values
        counts, bin_edges = np.histogram(synthetic, bins='auto')
        centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        widths  = np.diff(bin_edges)
        ax.bar(centers, counts, width=widths, color=hist_color, edgecolor=hist_color, alpha=0.85)

    if len(synthetic) > 1:
        kde = gaussian_kde(synthetic, bw_method='scott')
        x_fine = np.linspace(synthetic.min(), synthetic.max(), 300)
        kde_vals = kde(x_fine) * len(synthetic) * widths.mean()
        ax.plot(x_fine, kde_vals, color=kde_color, lw=1.8)

    ax.axvline(x=0, color='k', linestyle='--', lw=0.9, alpha=0.8)
    ax.set_xlabel('Residual', labelpad=5)
    ax.set_ylabel('Frequency', labelpad=8)
    ax.set_title(title)
    ax.grid(True, alpha=0.2)


def plot_qq(ax, csv_path, title):
    df = pd.read_csv(csv_path)
    # Support both column naming conventions
    tcol = 'theoretical_quantiles' if 'theoretical_quantiles' in df.columns else 'theoretical_q'
    scol = 'sample_quantiles'      if 'sample_quantiles'      in df.columns else 'sample_q'
    tq = df[tcol].values
    sq = df[scol].values
    ax.scatter(tq, sq, s=6, color=qq_color, alpha=0.7, zorder=3)
    if 'qq_line' in df.columns:
        ax.plot(tq, df['qq_line'], color=ref_color, lw=1.5, zorder=2)
    else:
        # Compute reference line through the 25th–75th percentile range
        q25, q75   = np.percentile(sq, [25, 75])
        tq25, tq75 = np.percentile(tq, [25, 75])
        slope     = (q75 - q25) / (tq75 - tq25)
        intercept = q25 - slope * tq25
        ax.plot(tq, slope * tq + intercept, color=ref_color, lw=1.5, zorder=2)
    ax.set_xlabel('Theoretical Quantiles', labelpad=5)
    ax.set_ylabel('Sample Quantiles', labelpad=8)
    ax.set_title(title)
    ax.grid(True, alpha=0.2)


for model in models:
    folder = f"./data/COD/{model}"
    mlabel = model_labels[model]

    train_hist = find_file(folder, '*train*histogram*.csv', '*train*distribution*.csv')
    test_hist  = find_file(folder, '*test*histogram*.csv',  '*test*distribution*.csv')
    train_qq   = find_file(folder, '*train*qq*.csv')
    test_qq    = find_file(folder, '*test*qq*.csv')

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    (ax_th, ax_teh), (ax_tq, ax_teq) = axes

    plot_histogram(ax_th,  train_hist, f'Residuals (train) — {mlabel}')
    plot_histogram(ax_teh, test_hist,  f'Residuals (test) — {mlabel}')
    plot_qq(ax_tq,  train_qq, f'QQ Plot (train) — {mlabel}')
    plot_qq(ax_teq, test_qq,  f'QQ Plot (test) — {mlabel}')

    panel_labels = ['(a)', '(b)', '(c)', '(d)']
    for ax, lbl in zip(axes.flatten(), panel_labels):
        ax.text(-0.05, 1.10, lbl, transform=ax.transAxes, fontsize=15, va='top', ha='right')

    plt.subplots_adjust(hspace=0.45, wspace=0.32)
    plt.savefig(f"figs/5_{model}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
