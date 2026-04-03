import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()
Path("figs").mkdir(exist_ok=True)

# Curated palette — perceptually distinct, not garish
PALETTE = [
    '#2196F3',  # blue
    '#FF7043',  # deep orange
    '#43A047',  # green
    '#AB47BC',  # purple
    '#00ACC1',  # cyan
    '#F9A825',  # amber
]


def ball_plot(ax, x, y, color, label=None, s=38):
    """Scatter with a layered 'ball' highlight effect."""
    # shadow layer
    ax.scatter(x, y, s=s * 1.6, color=color, edgecolors='none', alpha=0.18, zorder=2)
    # main ball
    ax.scatter(x, y, s=s, color=color, edgecolors='white', linewidth=0.2,
               alpha=0.82, zorder=3, label=label)
    # tiny white specular highlight — offset slightly up-right
    highlight_x = np.asarray(x) + (np.nanmax(x) - np.nanmin(x)) * 0.003
    ax.scatter(highlight_x, np.asarray(y) * 1.0, s=s * 0.08,
               color='white', edgecolors='none', alpha=0.7, zorder=4)


# ── Figure 1: COD2 (CODo, CODMBR) ──
cod1 = pd.read_csv("./data/2/COD1.csv")
cod2 = pd.read_csv("./data/2/COD2.csv")

x1 = np.arange(1, len(cod1) + 1)
x2 = np.arange(1, len(cod2) + 1)

fig, ax = plt.subplots(figsize=(9, 4))
ball_plot(ax, x2, cod2['CODo'],   PALETTE[1], label=r'$\mathrm{COD_o}$')
ball_plot(ax, x2, cod2['CODMBR'], PALETTE[2], label=r'$\mathrm{COD_{MBR}}$')
ax.set_ylabel('COD (mg/L)', labelpad=5)
ax.set_xlabel('Time (d)', labelpad=5)
ax.legend(frameon=False)
ax.set_xlim(0, len(cod2) + 1)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("figs/2_COD.png", dpi=300, bbox_inches='tight')
plt.close(fig)
print("Saved figs/2_COD.png")


# ── Other CSVs: one figure each ──
others = [
    ('NH3N.csv',   ['NH3-NO', 'NH3NMBR'],
     [r'$\mathrm{NH_3}$-$\mathrm{N_o}$', r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$'],
     r'$\mathrm{NH_3}$-N (mg/L)', '2_NH3N'),
    ('Q.csv',      ['Q2i', 'Q2mbr'],
     [r'$Q_i$', r'$Q_\mathrm{MBR}$'],
     r'Flow rate (m$^3$/d)', '2_Q'),
    ('温度.csv',   ['TempO'],
     ['Temperature'],
     'Temperature (°C)', '2_Temp'),
    ('pH.csv',     ['pH2i', 'pHO', 'pHMBR'],
     [r'$\mathrm{pH_i}$', r'$\mathrm{pH_o}$', r'$\mathrm{pH_{MBR}}$'],
     'pH', '2_pH'),
]

for filename, cols, labels, ylabel, outname in others:
    df = pd.read_csv(f"./data/2/{filename}", index_col=0)
    x = np.arange(1, len(df) + 1)

    fig, ax = plt.subplots(figsize=(9, 4))
    for col, lbl, c in zip(cols, labels, PALETTE):
        if col in df.columns:
            ball_plot(ax, x, df[col], c, label=lbl)
    ax.set_ylabel(ylabel, labelpad=5)
    ax.set_xlabel('Time (d)', labelpad=5)
    if outname != '2_Temp':
        ax.legend(frameon=False)
    ax.set_xlim(0, len(df) + 1)

    plt.tight_layout()
    plt.savefig(f"figs/{outname}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved figs/{outname}.png")

# ── P figure ──
do_p = pd.read_csv("./data/2/DO和P.csv", index_col=0)
x = np.arange(1, len(do_p) + 1)
fig, ax = plt.subplots(figsize=(9, 4))
ball_plot(ax, x, do_p['P'], PALETTE[0], label=r'$\Delta P$ (Pa)')
ax.set_ylabel(r'$\Delta P$ (Pa)', labelpad=5)
ax.set_xlabel('Time (d)', labelpad=5)
ax.legend(frameon=False)
ax.set_xlim(0, len(do_p) + 1)
plt.tight_layout()
plt.savefig("figs/2_P.png", dpi=300, bbox_inches='tight')
plt.close(fig)
print("Saved figs/2_P.png")

# ── DO figure ──
fig, ax = plt.subplots(figsize=(9, 4))
ball_plot(ax, x, do_p['DO'], PALETTE[1], label='DO (mg/L)')
ax.set_ylabel('DO (mg/L)', labelpad=5)
ax.set_xlabel('Time (d)', labelpad=5)
ax.legend(frameon=False)
ax.set_xlim(0, len(do_p) + 1)
plt.tight_layout()
plt.savefig("figs/2_DO.png", dpi=300, bbox_inches='tight')
plt.close(fig)
print("Saved figs/2_DO.png")

# ── NH3-Ni separate figure ──
nh3n = pd.read_csv("./data/2/NH3N.csv", index_col=0)
x = np.arange(1, len(nh3n) + 1)
fig, ax = plt.subplots(figsize=(9, 4))
ball_plot(ax, x, nh3n['NH3-N2i'], PALETTE[0], label=r'$\mathrm{NH_3}$-$\mathrm{N_i}$')
ax.set_ylabel(r'$\mathrm{NH_3}$-N (mg/L)', labelpad=5)
ax.set_xlabel('Time (d)', labelpad=5)
ax.legend(frameon=False)
ax.set_xlim(0, len(nh3n) + 1)
plt.tight_layout()
plt.savefig("figs/2_NH3Ni.png", dpi=300, bbox_inches='tight')
plt.close(fig)
print("Saved figs/2_NH3Ni.png")

# ── Combined COD: all three series in one panel ──
fig, ax = plt.subplots(figsize=(9, 4))
ball_plot(ax, x1, cod1['COD2i'],   PALETTE[0], label=r'$\mathrm{COD_i}$')
ball_plot(ax, x2, cod2['CODo'],    PALETTE[1], label=r'$\mathrm{COD_o}$')
ball_plot(ax, x2, cod2['CODMBR'],  PALETTE[2], label=r'$\mathrm{COD_{MBR}}$')
ax.set_ylabel('COD (mg/L)', labelpad=5)
ax.set_xlabel('Time (d)', labelpad=5)
ax.legend(frameon=False)
ax.set_xlim(0, max(len(cod1), len(cod2)) + 1)
ax.set_ylim(bottom=0)
plt.tight_layout()
plt.savefig("figs/2_COD_combined.png", dpi=300, bbox_inches='tight')
plt.close(fig)
print("Saved figs/2_COD_combined.png")

# ── Combined NH3N: all three series in one panel ──
fig, ax = plt.subplots(figsize=(9, 4))
ball_plot(ax, x, nh3n['NH3-N2i'], PALETTE[0], label=r'$\mathrm{NH_3}$-$\mathrm{N_i}$')
ball_plot(ax, x, nh3n['NH3-NO'],  PALETTE[1], label=r'$\mathrm{NH_3}$-$\mathrm{N_o}$')
ball_plot(ax, x, nh3n['NH3NMBR'], PALETTE[2], label=r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$')
ax.set_ylabel(r'$\mathrm{NH_3}$-N (mg/L)', labelpad=5)
ax.set_xlabel('Time (d)', labelpad=5)
ax.legend(frameon=False)
ax.set_xlim(0, len(nh3n) + 1)
plt.tight_layout()
plt.savefig("figs/2_NH3N_combined.png", dpi=300, bbox_inches='tight')
plt.close(fig)
print("Saved figs/2_NH3N_combined.png")
