import time
import random
import math

from syncronized_shapes import (
    connect_client,
    Rectangle)

connect_client("http://localhost:8080")

def get_random_color() -> tuple[int, int, int]:
    """
    Returns a random color as a tuple of 3 integers between 85 and 170.
    """
    return (
        random.randint(85, 200),
        random.randint(85, 200),
        random.randint(85, 200)
    )


rectangles = [
    Rectangle(
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        get_random_color()
    ) for _ in range(100)]


while True:
    t = time.time()
    x = abs(150 + math.cos(t) * 200)
    y = abs(150 + math.sin(t) * 200)

    for r in rectangles:
        r.x = x
        r.y = y

    # Keep stress high, but avoid unbounded producer saturation.
    time.sleep(0.01)