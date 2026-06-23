# examples/manual_trace.py
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from physkit_digitizer import AxisAlignedLinearCalibration, PixelCurve, RasterImage

def find_project_root(start: Path) -> Path:
    """Find the project root by walking upward until pyproject.toml is found."""

    current = start.resolve()

    if current.is_file():
        current = current.parent

    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("Could not find project root containing pyproject.toml.")

# ---------------------------------------------------------------------------
# Edit these values for the image you are tracing.
# ---------------------------------------------------------------------------
PROJECT_ROOT = find_project_root(Path(__file__))
IMAGE_PATH = PROJECT_ROOT / "data" / "private" / "img_Callister9Ed_fig.09.01.png"
OUTPUT_PATH = PROJECT_ROOT / "data" / "digitized" / "img_Callister9Ed_fig.09.01.json"
# Axis calibration:
# u = horizontal pixel coordinate
# v = vertical pixel coordinate
#
# For the sugar-water example:
# u=64  -> x=0
# u=350 -> x=100
# v=229 -> y=0
# v=24  -> y=100
CALIBRATION = AxisAlignedLinearCalibration(
    u1=64.0,
    x1=0.0,
    u2=350.0,
    x2=100.0,
    v1=229.0,
    y1=0.0,
    v2=24.0,
    y2=100.0,
)

CURVE_NAME = "manual_trace"
X_LABEL = "composition_wt_percent"
Y_LABEL = "temperature_C"


def main() -> None:
    """Manually trace a curve by clicking points on a plot image."""

    image = RasterImage.from_file(IMAGE_PATH)

    fig, ax = plt.subplots()

    # Show the raster image in pixel coordinates.
    # Matplotlib uses x for horizontal pixels and y for vertical pixels here.
    ax.imshow(image.array)

    ax.set_title(
        "Click curve points. Press Enter when done.",
    )
    ax.set_xlabel("u pixel coordinate")
    ax.set_ylabel("v pixel coordinate")

    # Collect clicked pixel coordinates.
    # Each point returned by ginput is a tuple (u, v).
    clicked_points = plt.ginput(n=-1, timeout=0)

    plt.close(fig)

    if len(clicked_points) == 0:
        raise RuntimeError("No points were clicked.")

    # Convert clicked tuples into separate u and v arrays.
    u = np.array([point[0] for point in clicked_points], dtype=np.float64)
    v = np.array([point[1] for point in clicked_points], dtype=np.float64)

    pixel_curve = PixelCurve(
        name=CURVE_NAME,
        u=u,
        v=v,
    )

    # Convert from pixel coordinates (u, v) to plot coordinates (x, y).
    digitized_curve = pixel_curve.to_data_curve(
        CALIBRATION,
        x_label=X_LABEL,
        y_label=Y_LABEL,
    )

    digitized_curve.save_json(OUTPUT_PATH)

    print(f"Saved digitized curve to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
