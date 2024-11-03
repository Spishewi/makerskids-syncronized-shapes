import sys
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')
    exit() # completely exit the program

def connect_client(url: str) -> None:
    """
    Connects the client to the server at the given URL.

    :param url: URL of the server
    """
    # Connect to the server
    sio.connect(url)

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