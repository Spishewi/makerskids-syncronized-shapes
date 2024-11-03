import time
import random
import math

#pylint: disable-next=unused-import
from syncronized_shapes import (
    connect_client,
    set_username,
    Rectangle)

connect_client('http://localhost:8080')

def get_random_color(): 
    return (
        random.randint(255//3, 255//3*2),
        random.randint(255//3, 255//3*2),
        random.randint(255//3, 255//3*2)
        )

rectangles = [Rectangle(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), get_random_color()) for i in range(100_000_000)]


while True:
    for r in rectangles:
        r.x = abs(150 + math.cos(time.time()) * 200)
        r.y = abs(150 + math.sin(time.time()) * 200)
    #print(r1.x, r1.y)
    time.sleep(.01)