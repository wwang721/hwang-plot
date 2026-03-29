import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init, shap_div_cmap

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
    'CODMBR':  r'$\mathrm{COD_{MBR}}$',
    'NH3NMBR': r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$',
}

models = ['RF', 'LightGBM', 'SVM', 'XGBoost']


def heatmap_panel(ax, csv_path, title, panel_label):
    df = pd.read_csv(csv_path)
    feature_cols = df.columns[2:]
    shap_matrix  = df[feature_cols].values

    # Sort features by mean |SHAP| (most important at top)
    importance = np.abs(shap_matrix).mean(axis=0)
    order = np.argsort(importance)[::-1]
    shap_matrix = shap_matrix[:, order]
    feat_labels = [LABEL_MAP.get(c, c) for c in feature_cols[order]]

    # Sort samples by model prediction f_x
    sample_order = np.argsort(df['f_x'].values)
    shap_matrix  = shap_matrix[sample_order, :]

    vmax = np.percentile(np.abs(shap_matrix), 98)
    im = ax.imshow(shap_matrix.T, cmap=shap_div_cmap, vmin=-vmax, vmax=vmax,
                   aspect='auto', interpolation='nearest')

    ax.set_yticks(range(len(feat_labels)))
    ax.set_yticklabels(feat_labels, fontsize=9)
    ax.set_xlabel('Samples (sorted by prediction)', labelpad=5)
    ax.set_title(title)
    ax.tick_params(bottom=False, labelbottom=False)
    plt.colorbar(im, ax=ax, fraction=0.03, pad=0.03, label='SHAP value')
    ax.text(-0.12, 1.08, panel_label, transform=ax.transAxes,
            fontsize=15, va='top', ha='right')


for model in models:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    heatmap_panel(axes[0], f"./data/4/{model}_CODMBR_before_heatmap_matrix.csv",
                  r'$\mathrm{COD_{MBR}}$ — SHAP Heatmap', '(a)')
    heatmap_panel(axes[1], f"./data/4/{model}_NH3NMBR_before_heatmap_matrix.csv",
                  r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$ — SHAP Heatmap', '(b)')

    fig.suptitle(model, fontsize=13)
    plt.subplots_adjust(wspace=0.4)
    plt.savefig(f"figs/4_{model}_shap_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
