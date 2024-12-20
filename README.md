# Makers Kids Synchronized Shapes
 https://2e21-176-175-194-121.ngrok-free.app 
## Overview

Makers Kids Synchronized Shapes is a real-time collaborative drawing application that allows multiple users to create and manipulate shapes on a shared canvas. The project utilizes WebSockets and Python to enable seamless communication between clients and the server.

The goal of this application is to help learn python syntax using visually appealing shapes on screen, and extend to more complex multiplayer behavior.

## Features

*   Real-time shape creation and manipulation
*   Multi-user collaboration
*   Support for various shape types (currently rectangles, ellipses and lines)
*   Automatic synchronization of shape data between clients and server

## Requirements

*   Python 3.10+
*   `python-socketio` library (client and server)
*   `aiohttp` library (server)
*   `raylib` library (server, for rendering)

## client
### setup
1.  Go to `client/` folder
2.  Install required libraries by running `pip install -r client-requirements.txt`
3.  For utilization exemples, see `client/exemple.py`

### Usage

1.  Connect to a server using `connect_client(url)`
2.  Create a new shape by instantiating a `Rectangle` object (or another supported shape)
3.  Manipulate shape attributes (e.g., position, size, color) using the provided setter methods
4.  The shape will be automatically synchronized with the server and other connected clients

## server
### setup
1.  Go to `server/` folder
2.  Install required libraries by running `pip install -r server-requirements.txt`
3.  Start the server by running `python ./main.py`


## API Documentation

see in-code documentation

## Contributing

Contributions are welcome! Please submit pull requests with clear descriptions of changes and additions.