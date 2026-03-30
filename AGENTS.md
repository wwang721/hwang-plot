# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

Supplementary plotting code and data for Hai Wang's master thesis. Python scripts generate scientific figures from CSV data; PNG outputs are committed automatically by GitHub Actions bot — **never commit locally generated PNGs**.

## Running Scripts

Install dependencies:
```bash
pip install -r requirements.txt
```

Run a specific figure script (from its directory):
```bash
cd figure1 && python plot.py
cd figure2 && python plot1.py
```

The CI workflow uses `uv` and sets `MPLBACKEND=Agg` for headless rendering. When running locally, set this if no display is available:
```bash
MPLBACKEND=Agg python plot.py
```

## Architecture

### Shared Configuration (`plt_settings.py`)

All plotting scripts import from the root-level `plt_settings.py` via a path manipulation pattern:
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from plt_settings import plt_init
```

`plt_init()` configures matplotlib globally: Times New Roman + Noto Sans CJK JP fonts, STIX mathtext (no LaTeX), consistent tick styles, and defines the Parula colormap.

### Figure Organization

Each figure lives in its own `figureN/` directory with:
- `plot.py` / `plot1.py` etc. — plotting scripts
- `data/` — CSV input files (time-series environmental monitoring data, primarily COD and NH3N)
- Generated PNGs saved locally within the directory or `figs/` subdirectory

### CI/CD Workflow

The `auto-plot.yml` workflow:
- Only runs when pushed by `wwang721` to `main`
- Skips on changes to `.md`, `.png`, `.jpg`, `.csv` files
- Installs Microsoft core fonts + Noto CJK (cached between runs)
- Runs scripts sequentially per figure directory
- Commits all `*.png` files with message `:bento: Generate figures [bot]`

To add a new figure to the pipeline, add its run commands to the workflow's "Run python scripts" step.

## Adding a New Figure

1. Create `figureN/` directory with a `data/` subfolder
2. Add CSV data and a `readme.md` describing requirements
3. Write `plot.py` using the shared `plt_settings` import pattern
4. Add `cd figureN && uv run plotX.py && cd ..` to `.github/workflows/auto-plot.yml`
