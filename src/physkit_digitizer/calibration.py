from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class AxisAlignedLinearCalibration:
    """
    Linear calibration for an axis-aligned 2D plot.

    This object maps image pixel coordinates to plot coordinates.

    Pixel coordinates:
        u = horizontal pixel coordinate, increasing to the right
        v = vertical pixel coordinate, increasing downward

    Data coordinates:
        x = horizontal plot coordinate
        y = vertical plot coordinate

    The calibration assumes that the plot axes are linear and not skewed.
    """

    # First horizontal calibration point:
    # pixel coordinate u1 corresponds to data coordinate x1.
    u1: float
    x1: float

    # Second horizontal calibration point:
    # pixel coordinate u2 corresponds to data coordinate x2.
    u2: float
    x2: float

    # First vertical calibration point:
    # pixel coordinate v1 corresponds to data coordinate y1.
    v1: float
    y1: float

    # Second vertical calibration point:
    # pixel coordinate v2 corresponds to data coordinate y2.
    v2: float
    y2: float

    def pixel_to_x(self, u: float | NDArray[np.float64]) -> float | NDArray[np.float64]:
        """
        Convert horizontal pixel coordinate u to data coordinate x.
        """

        return self.x1 + (u - self.u1) * (self.x2 - self.x1) / (self.u2 - self.u1)

    def pixel_to_y(self, v: float | NDArray[np.float64]) -> float | NDArray[np.float64]:
        """
        Convert vertical pixel coordinate v to data coordinate y.

        Image coordinates usually increase downward, so y2 may be larger
        even when v2 is smaller.
        """

        return self.y1 + (v - self.v1) * (self.y2 - self.y1) / (self.v2 - self.v1)

    def pixel_to_data(
        self,
        u: float | NDArray[np.float64],
        v: float | NDArray[np.float64],
    ) -> tuple[float | NDArray[np.float64], float | NDArray[np.float64]]:
        """
        Convert pixel coordinates (u, v) to plot coordinates (x, y).
        """

        x = self.pixel_to_x(u)
        y = self.pixel_to_y(v)

        return x, y