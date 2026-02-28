"""Core fuel and cost calculations for the gas calculator app."""

from __future__ import annotations

from dataclasses import dataclass

GALLON_TO_LITER = 3.78541


@dataclass(frozen=True)
class FillEstimates:
    needed: float
    total_cost: float
    current_percent: float
    cost_to_quarter: float
    cost_to_half: float
    cost_to_full: float


def to_liters(gallons: float) -> float:
    return gallons * GALLON_TO_LITER


def to_gallons(liters: float) -> float:
    return liters / GALLON_TO_LITER


def validate_inputs(price_per_unit: float, capacity: float, current_level: float) -> None:
    if price_per_unit <= 0:
        raise ValueError("Price must be greater than 0.")
    if capacity <= 0:
        raise ValueError("Tank capacity must be greater than 0.")
    if current_level < 0:
        raise ValueError("Current fuel level cannot be negative.")
    if current_level > capacity:
        raise ValueError("Current fuel level cannot exceed tank capacity.")


def fuel_needed(capacity: float, current_level: float) -> float:
    return max(capacity - current_level, 0.0)


def cost_for_target_level(
    current_level: float,
    capacity: float,
    target_ratio: float,
    price_per_unit: float,
) -> float:
    target_level = capacity * target_ratio
    needed = max(target_level - current_level, 0.0)
    return needed * price_per_unit


def estimate_distance_to_empty(current_level: float, efficiency: float) -> float:
    if efficiency <= 0:
        raise ValueError("Efficiency must be greater than 0.")
    return current_level * efficiency


def build_estimates(price_per_unit: float, capacity: float, current_level: float) -> FillEstimates:
    validate_inputs(price_per_unit, capacity, current_level)
    needed = fuel_needed(capacity, current_level)

    return FillEstimates(
        needed=needed,
        total_cost=needed * price_per_unit,
        current_percent=(current_level / capacity) * 100.0,
        cost_to_quarter=cost_for_target_level(current_level, capacity, 0.25, price_per_unit),
        cost_to_half=cost_for_target_level(current_level, capacity, 0.50, price_per_unit),
        cost_to_full=cost_for_target_level(current_level, capacity, 1.00, price_per_unit),
    )
