# src/physkit_digitizer/curve.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from physkit_digitizer.calibration import AxisAlignedLinearCalibration


@dataclass(frozen=True)
class DigitizedCurve:
    """
    Curve represented in calibrated plot coordinates.

    For a phase diagram, the coordinates are usually

        x = composition
        y = temperature

    This object is the output of the digitization process.
    """

    name: str
    x: NDArray[np.float64]
    y: NDArray[np.float64]
    x_label: str = "x"
    y_label: str = "y"

    def __post_init__(self) -> None:
        if self.x.shape != self.y.shape:
            raise ValueError(
                f"x and y must have the same shape. "
                f"Got x.shape={self.x.shape}, y.shape={self.y.shape}."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "x_label": self.x_label,
            "y_label": self.y_label,
            "x": self.x.tolist(),
            "y": self.y.tolist(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DigitizedCurve:
        return cls(
            name=str(data["name"]),
            x=np.asarray(data["x"], dtype=np.float64),
            y=np.asarray(data["y"], dtype=np.float64),
            x_label=str(data.get("x_label", "x")),
            y_label=str(data.get("y_label", "y")),
        )

    def save_json(self, path: str | Path) -> None:
        json_path = Path(path)
        json_path.parent.mkdir(parents=True, exist_ok=True)

        with json_path.open("w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=2)

    @classmethod
    def from_json(cls, path: str | Path) -> DigitizedCurve:
        json_path = Path(path)

        with json_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return cls.from_dict(data)
    

@dataclass(frozen=True)
class PixelCurve:
    """
    Curve represented in image pixel coordinates.

    Pixel convention:
        u = horizontal pixel coordinate, increasing to the right
        v = vertical pixel coordinate, increasing downward

    This object is the output of tracing or image extraction.
    """

    name: str
    u: NDArray[np.float64]
    v: NDArray[np.float64]

    def __post_init__(self) -> None:
        if self.u.shape != self.v.shape:
            raise ValueError(
                f"u and v must have the same shape. "
                f"Got u.shape={self.u.shape}, v.shape={self.v.shape}."
            )

    def to_data_curve(
        self,
        calibration: AxisAlignedLinearCalibration,
        *,
        x_label: str = "x",
        y_label: str = "y",
    ) -> DigitizedCurve:
        """
        Convert this pixel-space curve into a calibrated data-space curve.
        """

        x, y = calibration.pixel_to_data(self.u, self.v)

        return DigitizedCurve(
            name=self.name,
            x=np.asarray(x, dtype=np.float64),
            y=np.asarray(y, dtype=np.float64),
            x_label=x_label,
            y_label=y_label,
        )