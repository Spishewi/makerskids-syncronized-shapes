import time
import random
import math

from syncronized_shapes import (
    connect_client,
    set_username,
    Rectangle,
    Ellipse,
    Line
)

connect_client('http://localhost:8080')
#set_username("Bob")

randomColor = (random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2))

r1 = Line(0, 0, 50, 75, randomColor)

offsetx = random.randint(0, 100)
offsety = random.randint(0, 100)

while True:
    r1.x = 150 + math.cos(time.time()) * 200 + offsetx
    r1.y = 150 + math.sin(time.time()) * 200 + offsety
    #print(r1.x, r1.y)
    time.sleep(.03)
