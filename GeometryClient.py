import socketio

import uuid

sio = socketio.Client()

data = {}
server_data = {}

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def update(data):
    global server_data
    server_data = data

def connect_client(url: str):
    sio.connect(url)

def wait():
    try:
        while sio.connected:
            pass
    except KeyboardInterrupt:
        pass


class SyncronizedShape():
    def __init__(self) -> None:
        global data

        if not sio.connected:
            raise ConnectionError("Please be connected to the server !")

        self._uuid = str(uuid.uuid4())

    def __del__(self) -> None:
        global data
        del data[self._uuid]

    def update_data(self):
        data[self._uuid] = (self.__class__.__name__, self.__dict__())
        sio.emit("update", data)

class Rectangle(SyncronizedShape):
    def __init__(self, x: float, y: float, width: float, height: float, color: tuple[int, int, int]) -> None:
        super().__init__()
        self.__x = x
        self.__y = y
        self.__w = width
        self.__h = height
        self.__c = color

        self.update_data()

    def __dict__(self) -> dict:
        return {
            '__x': self.__x,
            '__y': self.__y,
            '__w': self.__w,
            '__h': self.__h,
            '__c': self.__c
        }
    
    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, v):
        self.__x = v
        self.update_data()
    
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, v):
        self.__y = v
        self.update_data()

    @property
    def w(self):
        return self.__w
    
    @w.setter
    def w(self, v):
        self.__w = v
        self.update_data()
    
    @property
    def h(self):
        return self.__h
    
    @h.setter
    def h(self, v):
        self.__h = v
        self.update_data()

    @property
    def color(self):
        return self.__c
    
    @color.setter
    def color(self, v):
        self.__c = v
        self.update_data()