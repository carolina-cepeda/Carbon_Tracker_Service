import pytest

from app.domain.value_objects.distance import Distance
from app.domain.value_objects.weight import Weight


def test_distance_accepts_positive_value():
    assert Distance(42.5).value == 42.5


def test_distance_rejects_zero():
    with pytest.raises(ValueError):
        Distance(0)


def test_distance_rejects_negative():
    with pytest.raises(ValueError):
        Distance(-1)


def test_distance_rejects_excessive():
    with pytest.raises(ValueError):
        Distance(100_001)


def test_weight_accepts_zero():
    assert Weight(0).value == 0


def test_weight_rejects_negative():
    with pytest.raises(ValueError):
        Weight(-0.5)


def test_weight_rejects_excessive():
    with pytest.raises(ValueError):
        Weight(100.5)