from aiohttp import web
import socketio

import pyray as pr
import threading

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

#async def index(request):
#    """Serve the client-side application."""
#    with open('index.html') as f:
#        return web.Response(text=f.read(), content_type='text/html')

server_data = {}

@sio.event
def connect(sid, environ):
    print("connect ", sid)
    server_data[sid] = []

@sio.event
async def update(sid, data):
    server_data[sid] = data
    #print(data)
    
    to_send_back = server_data.copy()
    del to_send_back[sid]
    await sio.emit("update", to_send_back, skip_sid=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    del server_data[sid]

#app.router.add_static('/static', 'static')
#app.router.add_get('/', index)
def run_raylib():
    pr.init_window(1920, 1080, "Makers Kids Connect")
    #pr.toggle_fullscreen()

    pr.set_target_fps(30)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)

        for shapes in server_data.values():
            for shape in shapes.values():
                if shape[0] == "Rectangle":
                    try:
                        pr.draw_rectangle(
                            int(shape[1]['__x']), 
                            int(shape[1]['__y']), 
                            int(shape[1]['__w']), 
                            int(shape[1]['__h']), 
                            pr.Color(
                                int(shape[1]['__c'][0]),
                                int(shape[1]['__c'][1]),
                                int(shape[1]['__c'][2]),
                                255 # alpha tkt
                                )
                            )
                    except Exception as e:
                        print(e)

        pr.end_drawing()
    pr.close_window()

if __name__ == '__main__':
    rl_thread = threading.Thread(target=run_raylib)
    rl_thread.start()
    web.run_app(app)