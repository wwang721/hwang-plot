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
    'CODMBR':  r'$\mathrm{COD_{MBR}}$',
    'NH3NMBR': r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$',
}

df_cod  = pd.read_csv("./data/1/CODMBR_correlation_matrix.csv",  index_col=0)
df_nh3n = pd.read_csv("./data/1/NH3NMBR_correlation_matrix.csv", index_col=0)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, df, title, panel in zip(
    axes,
    [df_cod, df_nh3n],
    [r'$\mathrm{COD_{MBR}}$ Correlation Matrix',
     r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$ Correlation Matrix'],
    ['(a)', '(b)'],
):
    im = ax.imshow(df.values, cmap='BrBG', vmin=-1, vmax=1, aspect='auto')

    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            ax.text(j, i, f'{df.values[i, j]:.2f}',
                    ha='center', va='center', fontsize=7,
                    color='white' if abs(df.values[i, j]) > 0.6 else 'black')

    ax.set_xticks(range(len(df.columns)))
    ax.set_yticks(range(len(df.index)))
    ax.set_xticklabels([LABEL_MAP.get(c, c) for c in df.columns], rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels([LABEL_MAP.get(c, c) for c in df.index], fontsize=9)
    ax.set_title(title)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.text(-0.15, 1.08, panel, transform=ax.transAxes, fontsize=15, va='top', ha='right')

plt.subplots_adjust(wspace=0.45)
plt.savefig("figs/1_correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.close(fig)
