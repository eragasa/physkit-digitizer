# physkit-digitizer

`physkit-digitizer` is a small scientific plot digitization package.

Its purpose is to convert raster plot images into calibrated numerical curves.

The core workflow is

$$
I(u,v)
\rightarrow
(u_i,v_i)
\rightarrow
(x_i,y_i)
\rightarrow
\mathcal{C}.
$$

where

- $I(u,v)$ is the image,
- $(u,v)$ are pixel coordinates,
- $(x,y)$ are calibrated plot coordinates,
- $\mathcal{C}$ is a digitized curve.

## Scope

This package provides:

- image loading,
- axis calibration,
- pixel-to-data coordinate transforms,
- manual curve tracing,
- color-based curve extraction,
- curve cleaning,
- CSV export.

It does not implement thermodynamic phase-diagram analysis directly. Phase-diagram interpretation belongs in `physkit`.

## Installation

```bash
python3 -m venv --prompt physkit-digitizer .venv
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## License
Apache=2.0


