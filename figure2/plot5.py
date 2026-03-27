import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()

method_colors = ['C3', 'C4', 'C1', 'C2']

alpha = 0.8
lw = 1.1

fig, ax = plt.subplots(1, 1, figsize=(12, 4))

df = pd.read_csv(f"./data/COD.csv")

time = pd.to_datetime(df.iloc[:, 0])

ax.plot(time, df.iloc[:, 1], clip_on=False, color='C0', label=r'Raw $\mathrm{COD_{MBR}}$', alpha=alpha, lw=lw)

for idx in range(4):
    value = df.iloc[:, idx + 2]
    value_name = df.columns[idx + 2]

    mask = value == 1
    ax.plot(time[mask], df.loc[mask, df.columns[1]], 'o', markersize=3, color=method_colors[idx], clip_on=False, label=f'{value_name} trend aware')

ticks = ax.get_xticks()
ax.set_xlim(left=time.min()-pd.Timedelta(days=31), right=time.max()+pd.Timedelta(days=31))
ax.set_ylim(bottom=0)

ax.legend(frameon=False)
ax.set_xlabel(df.columns[0], labelpad=5)
ax.set_ylabel(r'$\mathrm{COD_{MBR}}$', labelpad=5)
plt.savefig('./figs/5_COD.png', dpi=300, bbox_inches='tight')


#=====================================================================================


fig, ax = plt.subplots(1, 1, figsize=(12, 4))

df = pd.read_csv(f"./data/NH3N.csv")

time = pd.to_datetime(df.iloc[:, 0])

ax.plot(time, df.iloc[:, 1], clip_on=False, color='C0', label=r'Raw $\mathrm{NH_3}$-$\mathrm{N_{MBR}}$', alpha=alpha, lw=lw)

for idx in range(4):
    value = df.iloc[:, idx + 2]
    value_name = df.columns[idx + 2]

    mask = value == 1
    ax.plot(time[mask], df.loc[mask, df.columns[1]], 'o', markersize=3, color=method_colors[idx], clip_on=False, label=f'{value_name} trend aware')

ticks = ax.get_xticks()
ax.set_xlim(left=time.min()-pd.Timedelta(days=31), right=time.max()+pd.Timedelta(days=31))
ax.set_ylim(bottom=0, top=15)

ax.legend(frameon=False)
ax.set_xlabel(df.columns[0], labelpad=5)
ax.set_ylabel(r'$\mathrm{NH_3}$-$\mathrm{N_{MBR}}$', labelpad=5)
plt.savefig('./figs/5_NH3N.png', dpi=300, bbox_inches='tight')
