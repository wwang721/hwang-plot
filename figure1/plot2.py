import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()


alpha = 0.7
alpha2 = 0.7

colors = [
    '#E64B35',  # red
    '#8491B4',  # lavender
    '#DC0000',  # bright red
    '#F39B7F',  # salmon
    '#00B0F6',  # light blue (extended)
    '#00A087',  # teal
    '#91D1C2',  # mint
    '#3C5488',  # navy
    '#7E6148',  # brown
    '#4DBBD5',  # cyan
    '#B09C85',  # tan
    '#FF6700',  # orange (extended)
]
# increment = 7

value_names = [r'$\mathrm{Q_i}$', r'$\mathrm{Q_{MBR}}$', r'$\Delta\mathrm{P}$', 'DO', r'$\mathrm{pH_i}$', r'$\mathrm{COD_i}$',
               r'$\mathrm{NH_3}$-$\mathrm{N_i}$', r'$\mathrm{pH_o}$', r'$\mathrm{COD_o}$', r'$\mathrm{NH_3}$-$\mathrm{N_o}$',
               r'$\mathrm{Temp_o}$', r'$\mathrm{pH_{MBR}}$']

fig, ax= plt.subplots(figsize=(8.5, 4.2))

# Load CSV
df = pd.read_csv("./data/2025TRAINCOD.csv")

time = pd.to_datetime(df.iloc[:, 0])
for idx in range(12):
    value = df.iloc[:, idx + 1]
    value_name = df.columns[idx + 1]
    ax.plot(time, value, color=colors[idx], alpha=alpha, clip_on=False)


df = pd.read_csv("./data/2025TESTCOD.csv")
time = pd.to_datetime(df.iloc[:, 0])

for idx in range(12):
    value = df.iloc[:, idx + 1]
    ax.plot(time, value, color=colors[idx], alpha=alpha2, label=value_names[idx], clip_on=False)

ax.axvline(x=time[0], color='gray', linestyle='--', alpha=alpha)
ax.grid(True, alpha=0.2)
ax.set_xlabel(df.columns[0])

ax.legend(loc='upper right', fontsize=10, frameon=False) # bbox_to_anchor=(1.025, 1.58), labelspacing=0.15)

x_left, x_right = ax.get_xlim()
import matplotlib.dates as mdates
ax.axvspan(x_left, mdates.date2num(time[0]), color='C0', alpha=0.015, zorder=-1)
ax.axvspan(mdates.date2num(time[0]), x_right, color='C3', alpha=0.015, zorder=-1)
ax.set_xlim(x_left, x_right)

plt.savefig("test2.png", dpi=300, bbox_inches='tight')
