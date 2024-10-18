import asyncio
import socketio

sio = socketio.AsyncClient()

data = []

@sio.event
async def connect():
    print('connection established')

@sio.event
async def update(data):
    print('update : ', data)
    

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:8080')
    while sio.connected:
        await asyncio.sleep(2.0)
        data.append("a")
        await sio.emit("update", data)
    #await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())