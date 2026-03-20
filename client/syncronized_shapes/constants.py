"""Runtime configuration for synchronized shapes network behavior."""

# Maximum number of update messages sent per shape per second.
# This is a client-side throttle, not a guaranteed delivery rate.
# Default is tuned for smooth animations.
SHAPE_UPDATES_PER_SECOND = 60


def set_shape_updates_per_second(value: int) -> None:
    """Set the per-shape update rate limit (messages per second).

    Higher values improve animation smoothness but increase network traffic.
    Lower values reduce traffic but can make movement appear less fluid.
    """
    global SHAPE_UPDATES_PER_SECOND

    if not isinstance(value, int):
        raise TypeError(f"Expected int, got {type(value).__name__}")
    if value < 1:
        raise ValueError("SHAPE_UPDATES_PER_SECOND must be >= 1")

    SHAPE_UPDATES_PER_SECOND = value


def get_shape_update_interval_seconds() -> float:
    """Return minimum delay between two updates for one shape."""
    return 1.0 / SHAPE_UPDATES_PER_SECOND
