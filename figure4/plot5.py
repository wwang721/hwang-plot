import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init, shap_cmap

plt_init()
Path("figs").mkdir(exist_ok=True)

LABEL_MAP = {
    'Q2i':     r'$\mathrm{Q_i}$',
    'Q2mbr':   r'$\mathrm{Q_{MBR}}$',
    'P':       r'$\Delta\mathrm{P}$',
    'DO':      'DO',
    'pH2i':    r'$\mathrm{pH_i}$',
    'COD2i':   r'$\mathrm{COD_i}$',
    'NH3-N2i': r'$\mathrm{NH_3}$-$\mathrm{N_i}$',
    'NH3N2i':  r'$\mathrm{NH_3}$-$\mathrm{N_i}$',
    'pHO':     r'$\mathrm{pH_o}$',
    'CODo':    r'$\mathrm{COD_o}$',
    'NH3-NO':  r'$\mathrm{NH_3}$-$\mathrm{N_o}$',
    'NH3NO':   r'$\mathrm{NH_3}$-$\mathrm{N_o}$',
    'TempO':   r'$\mathrm{Temp_o}$',
    'pHMBR':   r'$\mathrm{pH_{MBR}}$',
}

models = ['RF', 'LightGBM', 'SVM', 'XGBoost']

rng = np.random.default_rng(42)


def beeswarm_panel(ax, csv_path, title, panel_label):
    """Beeswarm plot using per-sample SHAP values from the folder-4 heatmap matrix."""
    df = pd.read_csv(csv_path)
    feature_cols = df.columns[2:]           # drop sample_id and f_x
    shap_matrix  = df[feature_cols].values  # (n_samples, n_features)

    # Sort features by mean |SHAP| — least important at bottom (y=0)
    importance = np.abs(shap_matrix).mean(axis=0)
    order      = np.argsort(importance)     # ascending → most important at top
    feat_labels = [LABEL_MAP.get(c, c) for c in feature_cols[order]]

    vmax = np.percentile(np.abs(shap_matrix), 99)

    for y_pos, feat_idx in enumerate(order):
        shap_vals = shap_matrix[:, feat_idx]
        jitter    = rng.uniform(-0.35, 0.35, len(shap_vals))
        ax.scatter(shap_vals, y_pos + jitter,
                   c=shap_vals, cmap=shap_cmap,
                   vmin=-vmax, vmax=vmax,
                   s=4, alpha=0.5, linewidths=0)

    ax.axvline(x=0, color='k', linestyle='--', lw=0.8, alpha=0.6)
    ax.set_yticks(range(len(feat_labels)))
    ax.set_yticklabels(feat_labels, fontsize=9)
    ax.set_xlabel('SHAP value (impact on output)', labelpad=5)
    ax.set_title(title)
    ax.text(0.02, 0.98, panel_label, transform=ax.transAxes,
            fontsize=15, va='top', ha='left')

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=shap_cmap,
                               norm=plt.Normalize(vmin=-vmax, vmax=vmax))
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.03)
    cb.set_label('SHAP value', fontsize=9)
    cb.ax.tick_params(labelsize=8)


for model in models:
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    beeswarm_panel(axes[0],
                   f"./data/4/{model}_CODMBR_before_heatmap_matrix.csv",
                   r'$\mathrm{COD_{MBR}}$', '(a)')
    beeswarm_panel(axes[1],
                   f"./data/4/{model}_NH3NMBR_before_heatmap_matrix.csv",
                   r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$', '(b)')

    fig.suptitle(f'{model} — SHAP Beeswarm (Before)', fontsize=13)
    plt.subplots_adjust(wspace=0.45)
    plt.savefig(f"figs/5_{model}_beeswarm.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
