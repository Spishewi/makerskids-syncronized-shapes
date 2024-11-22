#from threading import Thread

from aiohttp import web

#from renderer import Renderer

from server import app

#renderer = Renderer()

#renderer_thread = Thread(target=renderer.run)
#renderer_thread.start()

web.run_app(app)

#if renderer_thread.is_alive():
#    renderer.stop()
