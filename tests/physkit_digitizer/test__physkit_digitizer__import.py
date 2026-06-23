#! ./tests/physkit_digitizer/test__physkit_digitizer__import.py
import pytest

def test__package__imports() -> None:
    import physkit_digitizer

    assert physkit_digitizer is not None

