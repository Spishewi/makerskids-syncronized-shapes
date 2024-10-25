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
        self.__width = width
        self.__height = height
        self.__color = color

        self.update_data()

    def __dict__(self) -> dict:
        return {
            '__x': self.__x,
            '__y': self.__y,
            '__width': self.__width,
            '__height': self.__height,
            '__color': self.__color
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
    def width(self):
        return self.__width
    
    @width.setter
    def width(self, v):
        self.__width = v
        self.update_data()
    
    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, v):
        self.__height = v
        self.update_data()

    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, v):
        self.__color = v
        self.update_data()