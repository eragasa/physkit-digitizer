# tests/physkit_digitizer/curve/test__PixelCurve.py
import numpy as np
import pytest

from physkit_digitizer.calibration import AxisAlignedLinearCalibration
from physkit_digitizer.curve import DigitizedCurve, PixelCurve


@pytest.fixture
def calibration() -> AxisAlignedLinearCalibration:
    return AxisAlignedLinearCalibration(
        u1=64.0,
        x1=0.0,
        u2=350.0,
        x2=100.0,
        v1=229.0,
        y1=0.0,
        v2=24.0,
        y2=100.0,
    )


def test__PixelCurve__stores_pixel_coordinates() -> None:
    curve = PixelCurve(
        name="test_curve",
        u=np.array([64.0, 350.0]),
        v=np.array([229.0, 24.0]),
    )

    assert curve.name == "test_curve"
    assert np.allclose(curve.u, np.array([64.0, 350.0]))
    assert np.allclose(curve.v, np.array([229.0, 24.0]))


def test__PixelCurve__raises_error_for_mismatched_shapes() -> None:
    with pytest.raises(ValueError):
        PixelCurve(
            name="bad_curve",
            u=np.array([64.0, 350.0]),
            v=np.array([229.0]),
        )


def test__to_data_curve__returns_DigitizedCurve(
    calibration: AxisAlignedLinearCalibration,
) -> None:
    pixel_curve = PixelCurve(
        name="test_curve",
        u=np.array([64.0, 350.0]),
        v=np.array([229.0, 24.0]),
    )

    curve = pixel_curve.to_data_curve(
        calibration,
        x_label="composition_wt_percent",
        y_label="temperature_C",
    )

    assert isinstance(curve, DigitizedCurve)
    assert curve.name == "test_curve"
    assert curve.x_label == "composition_wt_percent"
    assert curve.y_label == "temperature_C"
    assert np.allclose(curve.x, np.array([0.0, 100.0]))
    assert np.allclose(curve.y, np.array([0.0, 100.0]))