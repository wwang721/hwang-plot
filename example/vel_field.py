# To generate a velocity field as shown in paper: https://doi.org/10.1038/s42005-021-00530-6

import numpy as np
from scipy.interpolate import RBFInterpolator
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init, parula_map


plt_init()
plt.rc('axes', labelsize=10)

np.random.seed(42)                     # for reproducibility

L = 100.0                              # size of the box
pts = np.random.rand(1000, 2) * L      # generate 2d points in a box

v0 = 15.0                              # characteristic velocity
vel = np.random.randn(1000, 2) * v0    # generate random velocities for each point

x, y = pts[:, 0], pts[:, 1]
vx, vy = vel[:, 0], vel[:, 1]

# Grid limits (choose to cover your particles)
xmin, xmax = 0, L    # x.min(), x.max()
ymin, ymax = 0, L    # y.min(), y.max()

# Resolution of the grid
nx, ny = 100, 100

X, Y = np.meshgrid(
    np.linspace(xmin, xmax, nx),
    np.linspace(ymin, ymax, ny)
)

# Radial Basis Function interpolation
rbf_ux = RBFInterpolator(pts, vx, kernel='thin_plate_spline')
rbf_uy = RBFInterpolator(pts, vy, kernel='thin_plate_spline')

ux = rbf_ux(np.column_stack((X.ravel(), Y.ravel()))).reshape(X.shape)
uy = rbf_uy(np.column_stack((X.ravel(), Y.ravel()))).reshape(X.shape)

# Compute magnitude of velocity
mag = np.sqrt(ux**2 + uy**2)


fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
background = ax.pcolormesh(X, Y, mag, shading='auto', cmap=parula_map, vmin=0, vmax=30)  # or other colormap like 'viridis'

#========================== Colorbar ==========================
cbar = plt.colorbar(background, ax=ax, location='top', fraction=0.035, aspect=12, pad=0.015)
# fraction: fraction of original size
# aspect: length of the horizontal colorbar (fixed thickness)
# pad: distance between colorbar and main plot

# Add label to colorbar
cbar.ax.text(1.12, 0.3, r'$V\,(\mathrm{\mu m\cdot\mathrm{h}^{-1}})$', fontsize=8, transform=cbar.ax.transAxes)

cbar.outline.set_linewidth(0)
cbar.ax.tick_params(axis='both', which='major', direction='in', labelsize=8, pad=0)
cbar.ax.tick_params(axis='both', which='major', width=0.3, length=0)

cbar.set_ticks([0, 15, 30])

# Modify size of ticks
ticks = cbar.ax.xaxis.get_major_ticks()    # tick1line → tick on the left/bottom; tick2line → tick on the right/top
ticks[1].tick2line.set_markersize(1)       # only one tick in the middle

# Move colorbar position
pos = cbar.ax.get_position()
dx = 0.06
cbar.ax.set_position([pos.x0 - dx, pos.y0, pos.width, pos.height])
#==============================================================

# ax.streamplot(X, Y, ux, uy, color='k', linewidth=0.8, density=2.5)
# ax.quiver(x, y, vx, vy, color='k', scale=50)
ax.quiver(X, Y, ux, uy, color='k', scale=3000)

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")

ax.set_ylabel('Velocity field', labelpad=2)

# Remove ticks and spines
ax.tick_params(axis='both', length=0, labelbottom=False, labelleft=False)
ax.set_frame_on(False)

plt.savefig('vel_field.png', bbox_inches='tight', dpi=300)
