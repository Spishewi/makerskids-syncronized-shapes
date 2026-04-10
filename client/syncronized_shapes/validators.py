"""Validation helpers for synchronized shapes payload values."""

from .network import get_server_constants


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_color(name: str, value: tuple[int, int, int] | list[int]) -> tuple[int, int, int]:
    """Validate an RGB color tuple/list and return a normalized tuple."""
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"Expected tuple or list for {name}, got {type(value).__name__}")
    if len(value) != 3:
        raise ValueError(f"Expected 3 values for {name}, got {len(value)}")
    if not all(isinstance(channel, int) and 0 <= channel <= 255 for channel in value):
        raise TypeError(f"Expected 3 integers between 0 and 255 for {name}")
    return tuple(value)


def _get_limits() -> tuple[float, float]:
    """Return (max_coordinate, max_dimension) from synced server constants."""
    constants = get_server_constants()

    max_coordinate = constants.get("max_shape_coordinate")
    max_dimension = constants.get("max_shape_dimension")

    if not isinstance(max_coordinate, (int, float)) or not isinstance(max_dimension, (int, float)):
        raise RuntimeError("Server constants cache is missing numeric shape limits")

    return float(max_coordinate), float(max_dimension)


def validate_coordinate(name: str, value: float | int) -> float:
    """Validate a shape coordinate and return it as float."""
    if not _is_number(value):
        raise TypeError(f"Expected float or int for {name}, got {type(value).__name__}")

    max_coordinate, _ = _get_limits()
    parsed = float(value)
    if abs(parsed) > max_coordinate:
        raise ValueError(f"{name} is out of bounds (max abs: {max_coordinate})")
    return parsed


def validate_positive_dimension(name: str, value: float | int) -> float:
    """Validate a shape size/radius and return it as float."""
    if not _is_number(value):
        raise TypeError(f"Expected float or int for {name}, got {type(value).__name__}")

    _, max_dimension = _get_limits()
    parsed = float(value)
    if parsed <= 0:
        raise ValueError(f"{name} must be > 0")
    if parsed > max_dimension:
        raise ValueError(f"{name} is too large (max: {max_dimension})")
    return parsed
