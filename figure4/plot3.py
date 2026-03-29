import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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

# Feature group assignment
# Group A: pre-treatment effluent quality (water quality output of pre-treatment)
# Group B: operational & influent inputs
GROUP_A = {'CODo', 'TempO', 'pHO', 'NH3NO', 'NH3-NO'}
GROUP_B = {'Q2i', 'Q2mbr', 'P', 'DO', 'pH2i', 'COD2i', 'NH3N2i', 'NH3-N2i', 'pHMBR'}

GROUP_LABEL = {
    'A': 'Pre-treatment effluent',
    'B': 'Operational & influent',
}

# Colors: group A = blues, group B = warm tones
_COLORS_A = ['#2166AC', '#4393C3', '#74ADD1', '#ABD9E9', '#E0F3F8']
_COLORS_B = ['#D73027', '#F46D43', '#FDAE61', '#FEE090', '#E6AB02',
             '#A6761D', '#666666']

def feat_group(f):
    return 'A' if f in GROUP_A else 'B'


models     = ['RF', 'LightGBM', 'SVM', 'XGBoost']
model_file = {'RF': 'RF', 'LightGBM': 'LightGBM', 'SVM': 'SVM', 'XGBoost': 'XGB'}

DONUT_THRESHOLD = 2.0
height = 0.6


def load_merged(model_key, version):
    cod  = pd.read_csv(f"./data/3/{model_key}fig_CODMBR_{version}_plot_data.csv")
    nh3n = pd.read_csv(f"./data/3/{model_key}fig_NH3NMBR_{version}_plot_data.csv")
    cod.columns  = ['feature', 'cod_shap',  'cod_pct']
    nh3n.columns = ['feature', 'nh3n_shap', 'nh3n_pct']
    merged = pd.merge(cod, nh3n, on='feature', how='outer').fillna(0)
    merged['total'] = merged['cod_shap'] + merged['nh3n_shap']
    merged = merged.sort_values('total', ascending=True).reset_index(drop=True)
    return merged


def bar_panel(fig, gs_bar, merged, title, panel_label):
    ax = fig.add_subplot(gs_bar)
    y  = np.arange(len(merged))

    # Overlapping bars at the same y — draw larger behind, smaller in front
    ax.barh(y, merged['cod_shap'],  height, color='C0', alpha=0.75,
            label=r'$\mathrm{COD_{MBR}}$')
    ax.barh(y, merged['nh3n_shap'], height, color='C3', alpha=0.75,
            label=r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$')

    ax.set_yticks(y)
    ax.set_yticklabels([LABEL_MAP.get(f, f) for f in merged['feature']], fontsize=9)
    ax.set_xlabel('Mean |SHAP value|', labelpad=5)
    ax.set_title(title, pad=6)
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    ax.text(-0.12, 1.08, panel_label, transform=ax.transAxes,
            fontsize=15, va='top', ha='right')


def double_ring_panel(fig, gs_ring, merged):
    ax = fig.add_subplot(gs_ring)

    # ---- Outer ring: individual features (COD pct) ----
    outer_df = merged[merged['cod_pct'] >= DONUT_THRESHOLD].sort_values(
        'cod_pct', ascending=False)
    minor_sum = merged[merged['cod_pct'] < DONUT_THRESHOLD]['cod_pct'].sum()

    outer_feats = list(outer_df['feature'])
    outer_sizes = list(outer_df['cod_pct'])
    if minor_sum > 0:
        outer_feats.append('_others_')
        outer_sizes.append(minor_sum)

    # Assign colors by group
    color_counters = {'A': 0, 'B': 0}
    outer_colors = []
    for f in outer_feats:
        if f == '_others_':
            outer_colors.append('#BBBBBB')
        else:
            g = feat_group(f)
            palette = _COLORS_A if g == 'A' else _COLORS_B
            outer_colors.append(palette[color_counters[g] % len(palette)])
            color_counters[g] += 1

    outer_labels = [LABEL_MAP.get(f, f) if f != '_others_' else 'Others'
                    for f in outer_feats]

    wedges_outer, _, autotexts_outer = ax.pie(
        outer_sizes,
        labels=None,
        autopct=lambda p: f'{p:.1f}%' if p >= 4.0 else '',
        wedgeprops=dict(width=0.38, edgecolor='white', linewidth=0.8),
        pctdistance=0.82,
        radius=1.0,
        startangle=90,
        colors=outer_colors,
        textprops={'fontsize': 6.5},
    )
    for at in autotexts_outer:
        at.set_color('#222222')

    # ---- Inner ring: group totals ----
    group_totals = {'A': 0.0, 'B': 0.0}
    for _, row in merged.iterrows():
        g = feat_group(row['feature'])
        group_totals[g] += row['cod_pct']

    inner_sizes  = [group_totals['A'], group_totals['B']]
    inner_colors = [_COLORS_A[1], _COLORS_B[2]]
    inner_labels = [GROUP_LABEL['A'], GROUP_LABEL['B']]

    wedges_inner, _ = ax.pie(
        inner_sizes,
        labels=None,
        wedgeprops=dict(width=0.30, edgecolor='white', linewidth=0.8),
        radius=0.58,
        startangle=90,
        colors=inner_colors,
    )

    # Annotate inner ring with group % labels
    for wedge, lbl, size in zip(wedges_inner, inner_labels, inner_sizes):
        ang   = (wedge.theta1 + wedge.theta2) / 2
        rad   = 0.42
        x     = rad * np.cos(np.deg2rad(ang))
        y_pos = rad * np.sin(np.deg2rad(ang))
        ax.text(x, y_pos, f'{lbl}\n{size:.1f}%',
                ha='center', va='center', fontsize=6,
                color='white', fontweight='bold',
                multialignment='center')

    # Legend below for outer ring
    ax.legend(wedges_outer, outer_labels,
              fontsize=6.5,
              loc='upper center',
              bbox_to_anchor=(0.5, -0.05),
              ncol=2, frameon=False,
              handlelength=1.0, handleheight=1.0,
              columnspacing=0.8)

    ax.set_aspect('equal')


for model in models:
    mk  = model_file[model]
    fig = plt.figure(figsize=(16, 5))
    gs  = gridspec.GridSpec(1, 4, width_ratios=[2.5, 1.3, 2.5, 1.3],
                            wspace=0.55, figure=fig)

    m_before = load_merged(mk, 'before')
    m_after  = load_merged(mk, 'after')

    bar_panel(fig, gs[0], m_before, 'Before', '(a)')
    double_ring_panel(fig, gs[1], m_before)
    bar_panel(fig, gs[2], m_after,  'After',  '(b)')
    double_ring_panel(fig, gs[3], m_after)

    fig.suptitle(f'{model} — SHAP Feature Importance', fontsize=13, y=1.02)
    plt.savefig(f"figs/3_{model}_shap_importance.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
