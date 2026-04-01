import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

datasets = [
    (
        'cod_test_residual_plot_data_r2_081.csv',
        'cod_test_qq_plot_data_r2_081.csv',
        'Residual',
        'Theoretical_Quantiles', 'Sample_Quantiles', 'Reference_Line_Y',
        r'$\mathrm{COD_{MBR}}$',
        '3_COD',
    ),
    (
        'nh3n_test_residual_plot_data_r2_064.csv',
        'nh3n_test_qq_plot_data_r2_064.csv',
        'Residual',
        'Theoretical_Quantiles', 'Sample_Quantiles', 'Reference_Line_Y',
        r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$',
        '3_NH3N',
    ),
]

for (res_file, qq_file, res_col, tq_col, sq_col, ref_col, target_label, outname) in datasets:
    df_res = pd.read_csv(f"./data/3/{res_file}")
    df_qq  = pd.read_csv(f"./data/3/{qq_file}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # ── (a) Residual histogram ──
    residuals = df_res[res_col].dropna()
    hist_color = '#E88080'
    counts, bin_edges, _ = ax1.hist(residuals, bins=30, color=hist_color,
                                     edgecolor=hist_color, linewidth=0.4, alpha=0.85, density=False)

    # overlay KDE scaled to frequency
    kde = stats.gaussian_kde(residuals)
    xs = np.linspace(residuals.min(), residuals.max(), 300)
    bin_width = bin_edges[1] - bin_edges[0]
    ax1.plot(xs, kde(xs) * len(residuals) * bin_width, color='C3', lw=1.6)
    ax1.axvline(x=0, color='k', linestyle='--', lw=0.9, alpha=0.8)

    ax1.set_xlabel(f'Residual ({target_label})', labelpad=5)
    ax1.set_ylabel('Frequency', labelpad=5)
    ax1.text(-0.08, 1.03, '(a)', transform=ax1.transAxes, fontsize=15, va='top', ha='right')

    # ── (b) Q-Q plot ──
    ax2.scatter(df_qq[tq_col], df_qq[sq_col], s=6, color='C0', alpha=0.7, edgecolors='none', zorder=3)
    ax2.plot(df_qq[tq_col], df_qq[ref_col], color='C3', lw=1.5, zorder=2)

    ax2.set_xlabel('Theoretical quantiles', labelpad=5)
    ax2.set_ylabel('Sample quantiles', labelpad=5)
    ax2.text(-0.08, 1.03, '(b)', transform=ax2.transAxes, fontsize=15, va='top', ha='right')

    plt.tight_layout(w_pad=3.0)
    plt.savefig(f"figs/{outname}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved figs/{outname}.png")
