import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

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

models     = ['RF', 'LightGBM', 'SVM', 'XGBoost']
model_file = {'RF': 'RF', 'LightGBM': 'LightGBM', 'SVM': 'SVM', 'XGBoost': 'XGB'}

targets = [
    ('CODMBR',  r'$\mathrm{COD_{MBR}}$'),
    ('NH3NMBR', r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$'),
]
versions      = ['before', 'after']
panel_labels  = ['(a)', '(b)', '(c)', '(d)']


def load_df(model_key, target, version):
    df = pd.read_csv(f"./data/3/{model_key}fig_{target}_{version}_plot_data.csv")
    df.columns = ['feature', 'shap_val', 'pct']
    return df


def draw_panel(ax, df, panel_label, ylabel):
    df = df.sort_values('shap_val', ascending=True).reset_index(drop=True)
    y  = np.arange(len(df))

    ax.barh(y, df['shap_val'], color='C0', edgecolor='none')
    ax.set_yticks(y)
    ax.set_yticklabels([LABEL_MAP.get(f, f) for f in df['feature']], fontsize=9)
    ax.set_xlabel('Mean |SHAP value| (Impact on output)', labelpad=4)
    if ylabel:
        ax.set_ylabel('Feature', labelpad=4)
    ax.text(-0.08, 1.03, panel_label, transform=ax.transAxes,
            fontsize=15, va='top', ha='right')


for model in models:
    mk  = model_file[model]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    idx = 0
    for row, (target, target_label) in enumerate(targets):
        for col, version in enumerate(versions):
            ax = axes[row, col]
            df = load_df(mk, target, version)
            # Show y-label only on left column to avoid clipping
            draw_panel(ax, df, panel_labels[idx], ylabel=(col == 0))
            idx += 1

    plt.tight_layout(h_pad=3.5, w_pad=3.0)
    plt.savefig(f"figs/3_{model}_shap_importance.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
