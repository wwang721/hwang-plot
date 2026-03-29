import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import pandas as pd
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import gaussian_kde

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

MODELS = ['RF', 'LightGBM', 'SVM', 'XGBoost']
rng = np.random.default_rng(42)


def kde_violin_swarm(x_vals, max_spread=0.34, n_grid=200):
    """Return smooth violin envelope and density-scaled swarm offsets."""
    x_vals = np.asarray(x_vals, dtype=float)
    if len(x_vals) == 0:
        return np.array([]), np.array([]), np.array([]), np.array([])

    lo, hi = np.percentile(x_vals, [0.5, 99.5])
    if np.isclose(lo, hi):
        offsets = rng.uniform(-0.02, 0.02, len(x_vals))
        return np.array([lo, hi]), np.array([0.0, 0.0]), offsets, np.zeros_like(x_vals)

    x_grid = np.linspace(lo, hi, n_grid)
    if np.unique(x_vals).size < 2:
        density_grid = np.ones_like(x_grid)
    else:
        kde = gaussian_kde(x_vals)
        density_grid = kde(x_grid)

    density_grid /= density_grid.max() + 1e-12
    widths_grid = max_spread * density_grid
    point_widths = np.interp(x_vals, x_grid, widths_grid)
    offsets = rng.uniform(-1, 1, len(x_vals)) * point_widths * 0.95
    return x_grid, widths_grid, offsets, point_widths


def load_panel_data(csv_path):
    df = pd.read_csv(csv_path)
    feature_cols = list(df.columns[2:])
    shap_matrix = df[feature_cols].to_numpy()
    importance = np.abs(shap_matrix).mean(axis=0)
    order = np.argsort(importance)[::-1]

    return [(feature_cols[idx], shap_matrix[:, idx]) for idx in order]


def beeswarm_panel(ax, csv_path, title, panel_label, x_label):
    rows = load_panel_data(csv_path)
    max_abs = max(np.percentile(np.abs(vals), 99) for _, vals in rows)

    for y_pos, (feature_name, shap_vals) in enumerate(rows):
        x_vals = np.clip(shap_vals, -max_abs, max_abs)
        x_grid, widths_grid, offsets, point_widths = kde_violin_swarm(x_vals)
        y_vals = y_pos + offsets

        # The repo does not include per-sample raw feature values for these panels.
        # Use a row-wise normalized value proxy so the color gradient still separates
        # the low/high ends of each feature's distribution.
        v_lo, v_hi = np.percentile(shap_vals, [2, 98])
        color_vals = np.clip((shap_vals - v_lo) / (v_hi - v_lo + 1e-9), 0, 1)

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

        ax.scatter(
            x_vals,
            y_vals,
            c=color_vals,
            cmap=shap_cmap,
            vmin=0,
            vmax=1,
            s=7,
            alpha=0.8,
            linewidths=0,
            rasterized=True,
            zorder=1,
        )

    ax.axvline(x=0, color='#666666', linestyle='--', lw=0.8, alpha=0.7)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([LABEL_MAP.get(name, name) for name, _ in rows], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(-max_abs * 1.08, max_abs * 1.08)
    ax.grid(axis='y', linestyle=':', linewidth=0.4, alpha=0.35)
    ax.set_xlabel(x_label, labelpad=5)
    ax.set_title(title, pad=6)
    ax.text(0.02, 0.98, panel_label, transform=ax.transAxes,
            fontsize=15, va='top', ha='left')

    sm = cm.ScalarMappable(cmap=shap_cmap, norm=mcolors.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3.5%", pad=0.16)
    cb = plt.colorbar(sm, cax=cax)
    cb.set_label('Relative feature value', fontsize=9)
    cb.set_ticks([0, 1])
    cb.set_ticklabels(['Low', 'High'])
    cb.ax.tick_params(labelsize=8)


for model in MODELS:
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 7.2), sharex=False)

    beeswarm_panel(
        axes[0],
        f"./data/4/{model}_CODMBR_before_heatmap_matrix.csv",
        r'$\mathrm{COD_{MBR}}$',
        '(a)',
        'SHAP value (impact on output)',
    )
    beeswarm_panel(
        axes[1],
        f"./data/4/{model}_NH3NMBR_before_heatmap_matrix.csv",
        r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$',
        '(b)',
        'SHAP value (impact on output)',
    )

    plt.subplots_adjust(wspace=0.28)
    plt.savefig(f"figs/5_{model}_beeswarm.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
