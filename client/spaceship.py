import time
import random
import math

from syncronized_shapes import (
    connect_client,
    set_username,
    Rectangle,
    SpaceShip,
    Ellipse,
    Line
)

connect_client('http://127.0.0.1:8080')#172.16.17.220
set_username("Mat")

randomColor = (random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2))

r1 = SpaceShip(100, 100, -90, (255,0,0))
r2 = SpaceShip(200, 200, -90, (255,250,0))

offsetx = random.randint(0, 100)
offsety = random.randint(0, 100)

while True:
    r1.x = 200 + math.cos(time.time()) * 200 + offsetx
    r1.y = 200 + math.sin(time.time()) * 200 + offsety
    r1.rotation = math.sin(time.time())*200; 
    if random.randint(0, 100) > 95:
        r2.shoot()
    if random.randint(0, 100) > 95:
        r1.shoot()


    #r2.x = 200 + math.cos(time.time()) * 200 
    #r2.y = 200 + math.sin(time.time()) * 200 
    #r2.rotation = 200 + math.cos(time.time()) * 360 

    #print(r1.x, r1.y)
    r1.update()
    r2.update()
    time.sleep(.03)
