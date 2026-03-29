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
    'P':      r'$\Delta\mathrm{P}$',
    'DO':     'DO',
    'COD2i':  r'$\mathrm{COD_i}$',
    'CODo':   r'$\mathrm{COD_o}$',
    'NH3N2i': r'$\mathrm{NH_3}$-$\mathrm{N_i}$',
    'NH3NO':  r'$\mathrm{NH_3}$-$\mathrm{N_o}$',
}

targets = [
    ('CODMBR',  r'Partial dependence ($\mathrm{COD_{MBR}}$, mg/L)',              ['COD2i', 'CODo', 'DO', 'P']),
    ('NH3NMBR', r'Partial dependence ($\mathrm{NH_3}$-$\mathrm{N_{MBR}}$, mg/L)', ['DO', 'NH3N2i', 'NH3NO', 'P']),
]
panel_labels = ['(a)', '(b)', '(c)', '(d)']

ice_color  = 'C0'
mean_color = '#003399'

for target_prefix, ylabel, features in targets:
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))

    for i, (ax, feature, panel) in enumerate(zip(axes.flatten(), features, panel_labels)):
        df = pd.read_csv(f"./data/6/{target_prefix}_{feature}_ICE_original_scale.csv")
        x = df['feature_value_original'].values
        sample_cols = [c for c in df.columns if c.startswith('sample_')]

        for col in sample_cols:
            ax.plot(x, df[col].values, color=ice_color, lw=0.5, alpha=0.3)

        mean_vals = df[sample_cols].mean(axis=1).values
        ax.plot(x, mean_vals, color=mean_color, lw=1.8, label='Mean')

        ax.set_xlabel(LABEL_MAP.get(feature, feature), labelpad=5)
        if i % 2 == 0:   # left column only
            ax.set_ylabel(ylabel, labelpad=8)
        ax.text(0.02, 0.98, panel, transform=ax.transAxes,
                fontsize=15, va='top', ha='left')

    plt.tight_layout(h_pad=3.0, w_pad=2.5)
    plt.savefig(f"figs/6_{target_prefix}_ICE.png", dpi=300)
    plt.close(fig)
