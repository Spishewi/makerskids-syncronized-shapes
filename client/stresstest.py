import time
import random
import math

#pylint: disable-next=unused-import
from syncronized_shapes import (
    connect_client,
    Rectangle)

connect_client('http://localhost:8080')

def get_random_color() -> tuple[int, int, int]:
    """
    Returns a random color as a tuple of 3 integers between 85 and 170.
    """
    return (
        random.randint(85, 170),
        random.randint(85, 170),
        random.randint(85, 170)
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
    try:
        for r in rectangles:
            r.x = abs(150 + math.cos(time.time_ns() / 100000000) * 200)
            r.y = abs(150 + math.sin(time.time_ns() / 100000000) * 200)
    except ConnectionError:
        print("ERROR: connection lost, stopping stress test")
        break
    #print(r1.x, r1.y)
    #time.sleep(.01)