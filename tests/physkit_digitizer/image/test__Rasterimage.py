# ./tests/physkit_digitizer/image/test__RasterImage.py

from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from physkit_digitizer.image import RasterImage


@pytest.fixture
def rgb_image_path(tmp_path: Path) -> Path:
    path = tmp_path / "test.png"

    array = np.zeros((10, 20, 3), dtype=np.uint8)
    array[3, 4, :] = [255, 128, 64]

    Image.fromarray(array).save(path)

    return path


def test__from_file__loads_rgb_image(rgb_image_path: Path) -> None:
    image = RasterImage.from_file(rgb_image_path)

    assert image.width == 20
    assert image.height == 10
    assert image.array.shape == (10, 20, 3)


def test__pixel__returns_rgb_values(rgb_image_path: Path) -> None:
    image = RasterImage.from_file(rgb_image_path)

    assert np.array_equal(
        image.pixel(u=4, v=3),
        np.array([255, 128, 64], dtype=np.uint8),
    )