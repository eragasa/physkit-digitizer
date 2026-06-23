# tests/physkit_digitizer/curve/test__DigitizedCurve.py

from pathlib import Path

import numpy as np
import pytest

from physkit_digitizer.curve import DigitizedCurve


def test__DigitizedCurve__stores_data_coordinates() -> None:
    """DigitizedCurve should store calibrated curve coordinates and labels."""

    # These are already calibrated plot coordinates, not pixel coordinates.
    curve = DigitizedCurve(
        name="test_curve",
        x=np.array([0.0, 100.0]),
        y=np.array([0.0, 100.0]),
        x_label="composition_wt_percent",
        y_label="temperature_C",
    )

    assert curve.name == "test_curve"
    assert np.allclose(curve.x, np.array([0.0, 100.0]))
    assert np.allclose(curve.y, np.array([0.0, 100.0]))
    assert curve.x_label == "composition_wt_percent"
    assert curve.y_label == "temperature_C"


def test__DigitizedCurve__raises_error_for_mismatched_shapes() -> None:
    """DigitizedCurve should reject curves where x and y have different lengths."""

    # A curve is a paired sequence of points, so every x must have a y.
    with pytest.raises(ValueError):
        DigitizedCurve(
            name="bad_curve",
            x=np.array([0.0, 100.0]),
            y=np.array([0.0]),
        )


def test__to_dict__returns_serializable_dictionary() -> None:
    """to_dict should convert NumPy arrays into JSON-serializable lists."""

    curve = DigitizedCurve(
        name="test_curve",
        x=np.array([0.0, 100.0]),
        y=np.array([10.0, 20.0]),
        x_label="composition_wt_percent",
        y_label="temperature_C",
    )

    # JSON cannot directly serialize NumPy arrays, so x and y must become lists.
    data = curve.to_dict()

    assert data == {
        "name": "test_curve",
        "x_label": "composition_wt_percent",
        "y_label": "temperature_C",
        "x": [0.0, 100.0],
        "y": [10.0, 20.0],
    }


def test__from_dict__constructs_digitized_curve() -> None:
    """from_dict should reconstruct a DigitizedCurve from serialized data."""

    data = {
        "name": "test_curve",
        "x_label": "composition_wt_percent",
        "y_label": "temperature_C",
        "x": [0.0, 100.0],
        "y": [10.0, 20.0],
    }

    # The serialized lists should be converted back into NumPy arrays.
    curve = DigitizedCurve.from_dict(data)

    assert curve.name == "test_curve"
    assert curve.x_label == "composition_wt_percent"
    assert curve.y_label == "temperature_C"
    assert np.allclose(curve.x, np.array([0.0, 100.0]))
    assert np.allclose(curve.y, np.array([10.0, 20.0]))


def test__save_json__writes_json_file(tmp_path: Path) -> None:
    """save_json should write a DigitizedCurve to a JSON file."""

    path = tmp_path / "curve.json"

    curve = DigitizedCurve(
        name="test_curve",
        x=np.array([0.0, 100.0]),
        y=np.array([10.0, 20.0]),
    )

    # The output path is inside pytest's temporary directory.
    curve.save_json(path)

    assert path.exists()


def test__from_json__loads_digitized_curve(tmp_path: Path) -> None:
    """from_json should load a saved DigitizedCurve without changing its data."""

    path = tmp_path / "curve.json"

    curve = DigitizedCurve(
        name="test_curve",
        x=np.array([0.0, 100.0]),
        y=np.array([10.0, 20.0]),
        x_label="composition_wt_percent",
        y_label="temperature_C",
    )

    # Save and reload to test the full JSON round trip.
    curve.save_json(path)
    loaded = DigitizedCurve.from_json(path)

    assert loaded.name == curve.name
    assert loaded.x_label == curve.x_label
    assert loaded.y_label == curve.y_label
    assert np.allclose(loaded.x, curve.x)
    assert np.allclose(loaded.y, curve.y)