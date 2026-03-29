import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import pandas as pd
from pathlib import Path
from scipy.stats import gaussian_kde

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init, parula_map, shap_cmap

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
    'pHO':     r'$\mathrm{pH_o}$',
    'CODo':    r'$\mathrm{COD_o}$',
    'NH3-NO':  r'$\mathrm{NH_3}$-$\mathrm{N_o}$',
    'TempO':   r'$\mathrm{Temp_o}$',
    'pHMBR':   r'$\mathrm{pH_{MBR}}$',
}

def fmt(name):
    return LABEL_MAP.get(name.replace('_raw', ''), name.replace('_raw', ''))


PREFIX       = 'CODMBR'
MODEL        = 'XGBoost'
TARGET_LABEL = r'$\mathrm{COD_{MBR}}$'

rng = np.random.default_rng(42)


def kde_violin_swarm(x_vals, max_spread=0.34, n_grid=200):
    x_vals = np.asarray(x_vals, dtype=float)
    if len(x_vals) == 0:
        return np.array([]), np.array([]), np.array([])

    lo, hi = np.percentile(x_vals, [0.5, 99.5])
    if np.isclose(lo, hi):
        return np.array([lo, hi]), np.array([0.0, 0.0]), rng.uniform(-0.02, 0.02, len(x_vals))

    x_grid = np.linspace(lo, hi, n_grid)
    if np.unique(x_vals).size < 2:
        density_grid = np.ones_like(x_grid)
    else:
        density_grid = gaussian_kde(x_vals)(x_grid)

    density_grid /= density_grid.max() + 1e-12
    widths_grid = max_spread * density_grid
    offsets = rng.uniform(-1, 1, len(x_vals)) * np.interp(x_vals, x_grid, widths_grid) * 0.95
    return x_grid, widths_grid, offsets

# -----------------------------------------------------------------------
# Figure 1: Beeswarm of SHAP interaction values for key pairs
# Each row = one interaction pair; dots colored by main feature value
# -----------------------------------------------------------------------
pair_files = sorted(Path("./data/9").glob(f"{PREFIX}_{MODEL}_*_x_*.csv"))
dfs        = [pd.read_csv(f) for f in pair_files]

row_labels = [f"{fmt(df.columns[0])} × {fmt(df.columns[1])}" for df in dfs]
n_rows     = len(dfs)

# Normalize each feature's values to [0,1] for a shared "feature value" colormap
cmap_feat = shap_cmap

fig, ax = plt.subplots(figsize=(9, 1.2 * n_rows + 1.5))

for y_pos, df in enumerate(dfs):
    shap_vals = df.iloc[:, 2].values          # interaction_shap_value
    feat_vals = df.iloc[:, 0].values          # main feature raw value
    x_grid, widths_grid, offsets = kde_violin_swarm(shap_vals)

    # Normalize feature values to [0, 1] independently per row
    vlo, vhi = np.percentile(feat_vals, 2), np.percentile(feat_vals, 98)
    norm_vals = np.clip((feat_vals - vlo) / (vhi - vlo + 1e-9), 0, 1)

    if len(x_grid) > 0:
        ax.fill_between(
            x_grid,
            y_pos - widths_grid,
            y_pos + widths_grid,
            color='#d8d8d8',
            alpha=0.18,
            linewidth=0,
            zorder=0,
        )

    ax.scatter(shap_vals, y_pos + offsets,
               c=norm_vals, cmap=cmap_feat,
               vmin=0, vmax=1,
               s=5, alpha=0.75, linewidths=0, zorder=1)

ax.axvline(x=0, color='k', linestyle='--', lw=0.8, alpha=0.6)
ax.set_yticks(range(n_rows))
ax.set_yticklabels(row_labels, fontsize=10)
ax.set_xlabel('SHAP interaction value', labelpad=5)
ax.set_title(f'{TARGET_LABEL} — Key Feature Interaction Beeswarm', pad=8)

# Shared colorbar: low → high feature value
sm = cm.ScalarMappable(cmap=shap_cmap, norm=mcolors.Normalize(vmin=0, vmax=1))
sm.set_array([])
cb = plt.colorbar(sm, ax=ax, pad=0.03)
cb.set_label('Feature value\n(low → high)', fontsize=8)
cb.set_ticks([0, 0.5, 1])
cb.set_ticklabels(['Low', 'Mid', 'High'])
cb.ax.tick_params(labelsize=8)

plt.tight_layout()
plt.savefig(f"figs/9_{PREFIX}_interaction_beeswarm.png", dpi=300, bbox_inches='tight')
plt.close(fig)

# -----------------------------------------------------------------------
# Figure 2: Key pair interaction scatter plots (2×2)
# x = main feature raw value, y = SHAP interaction, color = partner feature value
# -----------------------------------------------------------------------
panel_labels = ['(a)', '(b)', '(c)', '(d)']

fig, axes = plt.subplots(2, 2, figsize=(11, 8))

for ax, df, panel in zip(axes.flatten(), dfs, panel_labels):
    feat_a   = fmt(df.columns[0])
    feat_b   = fmt(df.columns[1])
    shap_col = df.columns[2]

    sc = ax.scatter(df.iloc[:, 0], df[shap_col], c=df.iloc[:, 1],
                    cmap=parula_map, s=8, alpha=0.7)
    cb = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(feat_b, fontsize=8)
    cb.ax.tick_params(labelsize=7)
    ax.set_xlabel(feat_a, labelpad=5)
    ax.set_ylabel(f'SHAP interaction\nfor {feat_a}', labelpad=8)
    ax.axhline(y=0, color='k', linestyle='--', lw=0.7, alpha=0.6)
    ax.text(-0.1, 1.10, panel, transform=ax.transAxes,
            fontsize=15, va='top', ha='right')

plt.subplots_adjust(hspace=0.42, wspace=0.42)
plt.savefig(f"figs/9_{PREFIX}_interaction_pairs.png", dpi=300, bbox_inches='tight')
plt.close(fig)
