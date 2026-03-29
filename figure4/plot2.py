import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from scipy.stats import gaussian_kde
from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

models   = ['RF', 'LightGBM', 'SVM', 'XGBoost']
versions = [
    ('before', 'Before-{model}_{target}_pred_vs_actual.csv'),
    ('after',  '{model}_{target}_after_pred_vs_actual.csv'),
]

train_color = 'C0'
test_color  = 'C3'
alpha = 0.6


def r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def scatter_panel(ax, df, ylabel, panel_label):
    train = df[df['set'] == 'train']
    test  = df[df['set'] == 'test']

    ax.scatter(train['predicted'], train['actual'],
               s=12, color=train_color, alpha=alpha, label='Train data', zorder=3)
    ax.scatter(test['predicted'],  test['actual'],
               s=12, color=test_color,  alpha=alpha, label='Test data',  zorder=3)

    # Regression fit lines
    for subset, color, label in [(train, train_color, 'Train fit'),
                                  (test,  test_color,  'Test fit')]:
        p = np.polyfit(subset['predicted'], subset['actual'], 1)
        x_line = np.linspace(subset['predicted'].min(), subset['predicted'].max(), 100)
        ax.plot(x_line, np.polyval(p, x_line), color=color, lw=1.4,
                linestyle='--', label=label, zorder=4)

    # 45° reference
    all_vals = np.concatenate([df['actual'].values, df['predicted'].values])
    vmin, vmax = all_vals.min(), all_vals.max()
    margin = (vmax - vmin) * 0.05
    lim = (vmin - margin, vmax + margin)
    ax.plot(lim, lim, 'k:', lw=0.8, alpha=0.5, zorder=2)
    ax.set_xlim(lim)
    ax.set_ylim(lim)

    # Metrics annotation
    tr_r2, tr_rmse = r2(train['actual'], train['predicted']), rmse(train['actual'], train['predicted'])
    te_r2, te_rmse = r2(test['actual'],  test['predicted']),  rmse(test['actual'],  test['predicted'])
    ax.text(0.04, 0.98,
            f'Train R²: {tr_r2:.2f}   Train RMSE: {tr_rmse:.3f}\n'
            f'Test  R²: {te_r2:.2f}   Test  RMSE: {te_rmse:.3f}',
            transform=ax.transAxes, fontsize=8, va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.75, lw=0))

    ax.set_xlabel('Predicted values', labelpad=5)
    ax.set_ylabel(f'Actual {ylabel}', labelpad=8)
    ax.legend(ncol=2, frameon=False, fontsize=8)
    ax.text(-0.1, 1.22, panel_label, transform=ax.transAxes,
            fontsize=15, va='top', ha='right')

    # ---- Marginal KDE distributions ----
    divider = make_axes_locatable(ax)
    ax_top   = divider.append_axes("top",   size="18%", pad=0.05, sharex=ax)
    ax_right = divider.append_axes("right", size="18%", pad=0.05, sharey=ax)

    x_range = np.linspace(lim[0], lim[1], 300)

    for subset, color in [(train, train_color), (test, test_color)]:
        # Top marginal: distribution of predicted values
        kde_x = gaussian_kde(subset['predicted'], bw_method=0.3)
        dens_x = kde_x(x_range)
        ax_top.fill_between(x_range, dens_x, alpha=0.45, color=color)
        ax_top.plot(x_range, dens_x, color=color, lw=0.8)

        # Right marginal: distribution of actual values
        kde_y = gaussian_kde(subset['actual'], bw_method=0.3)
        dens_y = kde_y(x_range)
        ax_right.fill_betweenx(x_range, dens_y, alpha=0.45, color=color)
        ax_right.plot(dens_y, x_range, color=color, lw=0.8)

    # Clean up marginal axes
    ax_top.set_yticks([])
    ax_top.set_xticks([])
    ax_right.set_xticks([])
    ax_right.set_yticks([])
    for spine in ['top', 'right', 'left']:
        ax_top.spines[spine].set_visible(False)
    ax_top.spines['bottom'].set_visible(False)
    for spine in ['top', 'right', 'bottom']:
        ax_right.spines[spine].set_visible(False)
    ax_right.spines['left'].set_visible(False)


for model in models:
    for version, fname_tpl in versions:
        fname_cod  = fname_tpl.format(model=model, target='CODMBR')
        fname_nh3n = fname_tpl.format(model=model, target='NH3NMBR')

        df_cod  = pd.read_csv(f"./data/2/{fname_cod}")
        df_nh3n = pd.read_csv(f"./data/2/{fname_nh3n}")

        fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
        scatter_panel(axes[0], df_cod,
                      r'$\mathrm{COD_{MBR}}$ (mg/L)', '(a)')
        scatter_panel(axes[1], df_nh3n,
                      r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$ (mg/L)', '(b)')

        fig.suptitle(f'{model} — {version.capitalize()}', fontsize=13, y=1.0)
        plt.subplots_adjust(wspace=0.45)
        plt.savefig(f"figs/2_{model}_{version}.png", dpi=300, bbox_inches='tight')
        plt.close(fig)
