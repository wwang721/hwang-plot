import numpy as np
import matplotlib.pyplot as plt

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init

plt_init()

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(4, 3))
ax.plot(x, y, label='$\sin(x)$', color='C0')
ax.plot(x, np.cos(x), label='$\cos(x)$', color='C3')
ax.set_xlabel('$x$ (rad)')
ax.set_ylabel('$y$')
ax.set_title('Times New Roman 字体示例')
ax.legend()
plt.savefig('font_test_TNR_Chinese.png', dpi=300, bbox_inches='tight')
