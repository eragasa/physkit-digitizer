# tests/physkit_digitizer/calibration/test__AxisAlignedLinearCalibration.py

import numpy as np

from physkit_digitizer.calibration import AxisAlignedLinearCalibration


def test__pixel_to_x__maps_left_axis_point() -> None:
    cal = AxisAlignedLinearCalibration(
        u1=64.0,
        x1=0.0,
        u2=350.0,
        x2=100.0,
        v1=229.0,
        y1=0.0,
        v2=24.0,
        y2=100.0,
    )

    assert cal.pixel_to_x(64.0) == 0.0


def test__pixel_to_x__maps_right_axis_point() -> None:
    cal = AxisAlignedLinearCalibration(
        u1=64.0,
        x1=0.0,
        u2=350.0,
        x2=100.0,
        v1=229.0,
        y1=0.0,
        v2=24.0,
        y2=100.0,
    )

    assert cal.pixel_to_x(350.0) == 100.0


def test__pixel_to_y__maps_bottom_axis_point() -> None:
    cal = AxisAlignedLinearCalibration(
        u1=64.0,
        x1=0.0,
        u2=350.0,
        x2=100.0,
        v1=229.0,
        y1=0.0,
        v2=24.0,
        y2=100.0,
    )

    assert cal.pixel_to_y(229.0) == 0.0


def test__pixel_to_y__maps_top_axis_point() -> None:
    cal = AxisAlignedLinearCalibration(
        u1=64.0,
        x1=0.0,
        u2=350.0,
        x2=100.0,
        v1=229.0,
        y1=0.0,
        v2=24.0,
        y2=100.0,
    )

    assert cal.pixel_to_y(24.0) == 100.0


def test__pixel_to_data__maps_pixel_pair_to_data_pair() -> None:
    cal = AxisAlignedLinearCalibration(
        u1=64.0,
        x1=0.0,
        u2=350.0,
        x2=100.0,
        v1=229.0,
        y1=0.0,
        v2=24.0,
        y2=100.0,
    )

    x, y = cal.pixel_to_data(64.0, 229.0)

    assert x == 0.0
    assert y == 0.0


def test__pixel_to_data__accepts_numpy_arrays() -> None:
    cal = AxisAlignedLinearCalibration(
        u1=64.0,
        x1=0.0,
        u2=350.0,
        x2=100.0,
        v1=229.0,
        y1=0.0,
        v2=24.0,
        y2=100.0,
    )

    u = np.array([64.0, 350.0])
    v = np.array([229.0, 24.0])

    x, y = cal.pixel_to_data(u, v)

    assert np.allclose(x, np.array([0.0, 100.0]))
    assert np.allclose(y, np.array([0.0, 100.0]))