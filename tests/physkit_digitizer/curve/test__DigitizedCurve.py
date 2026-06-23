# tests/physkit_digitizer/curve/test__DigitizedCurve.py
import numpy as np
import pytest

from physkit_digitizer.curve import DigitizedCurve


def test__DigitizedCurve__stores_data_coordinates() -> None:
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
    with pytest.raises(ValueError):
        DigitizedCurve(
            name="bad_curve",
            x=np.array([0.0, 100.0]),
            y=np.array([0.0]),
        )