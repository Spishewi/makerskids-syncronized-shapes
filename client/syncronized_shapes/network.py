import sys
import socketio

sio = socketio.Client()
_canvas_size_cache: dict[str, int] | None = None

@sio.event
def connect():
    """
    Handles the connection event emitted by the server after a
    successful connection.

    Prints a message to the console to indicate that the connection
    has been established.
    """
    print('connection established')

@sio.event
def disconnect():
    """
    Handles the disconnection event emitted by the server after a
    successful disconnection.

    Prints a message to the console to indicate that the disconnection
    has been sucessful and exits the program.
    """
    print('disconnected from server')
    sys.exit() # completely exit the program

def connect_client(url: str) -> None:
    """
    Connects the client to the server at the given URL.

    :param url: URL of the server
    """
    # Connect to the server
    sio.connect(url, namespaces=["/client"])

def get_canvas_size(force_refresh: bool = False) -> dict[str, int]:
    """Return the renderer canvas size defined by the server.

    :param force_refresh: If True, always request fresh data from server.
    :return: Dictionary with "width" and "height" integer keys.
    """
    global _canvas_size_cache

    if not sio.connected:
        raise ConnectionError("Please be connected to the server !")

    if _canvas_size_cache is not None and not force_refresh:
        return _canvas_size_cache

    data = sio.call("get_canvas_size", namespace="/client", timeout=2)
    if not isinstance(data, dict):
        raise RuntimeError("Invalid canvas size payload from server")

    width = data.get("width")
    height = data.get("height")
    if not isinstance(width, int) or not isinstance(height, int):
        raise RuntimeError("Canvas size payload must contain integer width and height")

    _canvas_size_cache = {"width": width, "height": height}
    return _canvas_size_cache

def set_username(username: str):
    """
    Emits an event to set the username on the server.

    :param username: The username to be set for the client
    """
    if not sio.connected:
        raise ConnectionError("Please be connected to the server !")

    # Emit the set_username event with the provided username
    sio.emit("set_username", username, callback=error_handler, namespace="/client")

def error_handler(status_code, message):
    """
    Handles errors by printing an error message to stderr if the status code is not 200.

    :param status_code: The status code returned by a request
    :param message: The error message to be displayed
    """
    # Check if the status code indicates an error
    if status_code != 200:
        # Print the error message to stderr
        print(f"ERROR: {message}", file=sys.stderr)

#unused ?
def wait():
    try:
        while sio.connected:
            pass
    except KeyboardInterrupt:
        pass
