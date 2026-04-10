import time
import random
import math

from syncronized_shapes import (
    connect_client,
    set_username,
    Rectangle,
)

connect_client("http://127.0.0.1:8080")# 'https://6fd3-2a01-e0a-1081-aaf0-5d6f-8b-75d7-7b4b.ngrok-free.app/')#172.16.17.220 https://d73d-176-175-194-121.ngrok-free.app
set_username("Bob")

randomColor = (random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2),
               random.randint(255//3, 255//3*2))

r1 = Rectangle(0, 0, 50, 75, randomColor)

offsetx = random.randint(0, 100)
offsety = random.randint(0, 100)

while True:
    try:
        r1.x = 150 + math.cos(time.time()) * 200 + offsetx
        r1.y = 150 + math.sin(time.time()) * 200 + offsety
    except ConnectionError:
        print("ERROR: connection lost, stopping client loop")
        break

    #print(r1.x, r1.y)
    time.sleep(0.03)
