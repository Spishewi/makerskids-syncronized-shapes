from threading import Thread

from aiohttp import web

from renderer import Renderer
from server import app, shapes_data, shapes_owner


renderer = Renderer(shapes_data=shapes_data, shapes_owner=shapes_owner)

renderer_thread = Thread(target=renderer.run)
renderer_thread.start()

web.run_app(app)

if renderer_thread.is_alive():
    renderer.stop()
