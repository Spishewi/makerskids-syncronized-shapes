"""
This module contains utility functions for the `syncronized_shapes` package.
"""

def map_value(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """
    Maps a value from one range to another range.

    This function maps a value from the range [in_min, in_max] to the range [out_min, out_max].

    :param value: The value to map
    :param in_min: The minimum value of the input range
    :param in_max: The maximum value of the input range
    :param out_min: The minimum value of the output range
    :param out_max: The maximum value of the output range
    :return: The mapped value
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min