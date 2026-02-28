import pytest

from calculator import (
    GALLON_TO_LITER,
    build_estimates,
    estimate_distance_to_empty,
    to_gallons,
    to_liters,
    validate_inputs,
)


def test_unit_conversions_round_trip():
    gallons = 12.0
    liters = to_liters(gallons)
    assert liters == pytest.approx(gallons * GALLON_TO_LITER)
    assert to_gallons(liters) == pytest.approx(gallons)


def test_validate_inputs_rejects_invalid_values():
    with pytest.raises(ValueError):
        validate_inputs(0, 10, 5)
    with pytest.raises(ValueError):
        validate_inputs(3, 0, 0)
    with pytest.raises(ValueError):
        validate_inputs(3, 10, -1)
    with pytest.raises(ValueError):
        validate_inputs(3, 10, 11)


def test_build_estimates_costs_and_percentages():
    estimates = build_estimates(price_per_unit=4.0, capacity=20.0, current_level=5.0)
    assert estimates.needed == pytest.approx(15.0)
    assert estimates.total_cost == pytest.approx(60.0)
    assert estimates.current_percent == pytest.approx(25.0)
    assert estimates.cost_to_quarter == pytest.approx(0.0)
    assert estimates.cost_to_half == pytest.approx(20.0)
    assert estimates.cost_to_full == pytest.approx(60.0)


def test_estimate_distance_to_empty():
    assert estimate_distance_to_empty(current_level=8, efficiency=30) == pytest.approx(240)

    with pytest.raises(ValueError):
        estimate_distance_to_empty(current_level=8, efficiency=0)
