import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()


train_color = 'C0' # 'C2'
test_color = 'C3' # 'C1'
alpha = 0.7
value_names = [r'$\mathrm{Q_i}$', r'$\mathrm{Q_{MBR}}$', r'$\Delta\mathrm{P}$', 'DO', r'$\mathrm{pH_i}$', r'$\mathrm{COD_i}$',
               r'$\mathrm{NH_3}$-$\mathrm{N_i}$', r'$\mathrm{pH_o}$', r'$\mathrm{COD_o}$', r'$\mathrm{NH_3}$-$\mathrm{N_o}$',
               r'$\mathrm{Temp_o}$', r'$\mathrm{pH_{MBR}}$']

fig, axes= plt.subplots(4, 3, figsize=(16, 8))

axes = axes.flatten()

# Load CSV
df = pd.read_csv("./data/2025TRAINCOD.csv")

time = pd.to_datetime(df.iloc[:, 0])
for idx, ax in enumerate(axes):
    value = df.iloc[:, idx + 1]
    if idx != 2:
        ax.plot(time, value, color=train_color, alpha=alpha, clip_on=False)
    else:
        ax.plot(time, value, color=train_color, label='Train', alpha=alpha, clip_on=False)


df = pd.read_csv("./data/2025TESTCOD.csv")
time = pd.to_datetime(df.iloc[:, 0])

for idx, ax in enumerate(axes):
    value = df.iloc[:, idx + 1]

    ax.axvline(x=time[0], color='gray', linestyle='--')
    if idx != 2:
        ax.plot(time, value, color=test_color, alpha=alpha, clip_on=False)
    else:
        ax.plot(time, value, color=test_color, label='Test', alpha=alpha, clip_on=False)

    ax.grid(True, alpha=0.2)

    value_name = df.columns[idx + 1]
    ax.set_title(value_names[idx], pad=6)

    if idx < 9:
        ax.set_xticklabels([])
    else:
        for i, label in enumerate(ax.get_xticklabels()):
            label.set_visible(i % 2 == 0)
        ax.set_xlabel(df.columns[0])

axes[0].set_ylim(bottom=0)
axes[1].set_ylim(bottom=0)
axes[3].set_ylim(bottom=0)
axes[5].set_ylim(bottom=0)
axes[6].set_ylim(bottom=0)
axes[8].set_ylim(bottom=0)
# axes[9].set_ylim(bottom=0)
axes[-1].set_ylim(bottom=5.8)

plt.subplots_adjust(
    wspace=0.12,   # width space between columns
    hspace=0.275   # height space between rows
)

axes[2].legend(loc='upper right', fontsize=14, bbox_to_anchor=(1.025, 1.58), labelspacing=0.14)
# fig.suptitle("Overall Title: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", y=0.96, fontsize=16)
plt.savefig("test.png", dpi=300, bbox_inches='tight')
