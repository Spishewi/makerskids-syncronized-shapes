import time
import random
import math

from GeometryClient import *

connect_client('http://localhost:8080')

randomColor = (random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2))

r1 = Rectangle(0, 0, 50, 50, randomColor)

offsetx = random.randint(0, 500)
offsety = random.randint(0, 500)

print(data)

while True:
    r1.x = 150 + math.cos(time.time()) * 200 + offsetx
    r1.y = 150 + math.sin(time.time()) * 200 + offsety
    #print(r1.x, r1.y)
    time.sleep(.01)