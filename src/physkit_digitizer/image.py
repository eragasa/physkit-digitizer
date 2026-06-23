# ./src/physkit_digitizer/image.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from PIL import Image


@dataclass(frozen=True)
class RasterImage:
    """
    Raster image stored as an RGB array.

    Pixel coordinate convention:
        u = horizontal pixel coordinate, increasing to the right
        v = vertical pixel coordinate, increasing downward

    Array convention:
        array[v, u, channel]
    """

    path: Path
    array: NDArray[np.uint8]

    @classmethod
    def from_file(cls, path: str | Path) -> RasterImage:
        image_path = Path(path)

        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        image = Image.open(image_path).convert("RGB")
        array = np.asarray(image, dtype=np.uint8)

        return cls(
            path=image_path,
            array=array,
        )

    @property
    def height(self) -> int:
        return int(self.array.shape[0])

    @property
    def width(self) -> int:
        return int(self.array.shape[1])

    @property
    def shape(self) -> tuple[int, int, int]:
        return self.array.shape

    def pixel(self, u: int, v: int) -> NDArray[np.uint8]:
        if not 0 <= u < self.width:
            raise IndexError(f"u={u} outside image width {self.width}")

        if not 0 <= v < self.height:
            raise IndexError(f"v={v} outside image height {self.height}")

        return self.array[v, u, :]
