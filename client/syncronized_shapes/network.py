import sys
import socketio

from .constants import (
    CLIENT_NAMESPACE,
    DISCONNECTED_MESSAGE,
    EVENT_GET_SERVER_CONSTANTS,
    EVENT_SERVER_CONSTANTS,
    EVENT_SET_USERNAME,
    SERVER_CONSTANTS_FETCH_TIMEOUT_SECONDS,
    SERVER_CONSTANTS_REQUIRED_KEYS,
)

# Use a simple connection lifecycle like before the recent refactors:
# no forced WebSocket transport and no automatic reconnect state juggling.
sio = socketio.Client(reconnection=False, request_timeout=30)
_canvas_size_cache: dict[str, int] | None = None
_server_constants_cache: dict[str, int | float] | None = None


def _validate_server_constants_payload(data: dict) -> dict[str, int | float]:
    if not isinstance(data, dict):
        raise RuntimeError("Invalid server constants payload")

    missing_keys = [key for key in SERVER_CONSTANTS_REQUIRED_KEYS if key not in data]
    if missing_keys:
        raise RuntimeError(f"Missing server constants keys: {', '.join(missing_keys)}")

    return data


def _merge_server_constants(data: dict) -> None:
    global _server_constants_cache, _canvas_size_cache
    _server_constants_cache = _validate_server_constants_payload(data)

    # Keep canvas cache consistent with server constants.
    _canvas_size_cache = {
        "width": int(_server_constants_cache["renderer_canvas_width"]),
        "height": int(_server_constants_cache["renderer_canvas_height"]),
    }


def _fetch_and_cache_server_constants() -> None:
    """Fetch constants once from server and store them in local cache."""
    payload = sio.call(
        EVENT_GET_SERVER_CONSTANTS,
        namespace=CLIENT_NAMESPACE,
        timeout=SERVER_CONSTANTS_FETCH_TIMEOUT_SECONDS,
    )
    _merge_server_constants(payload)

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
    Handles the disconnection event emitted by the server.

    Prints an error message to stderr. The caller can decide whether
    to stop the program or keep running.
    """
    print('ERROR: disconnected from server', file=sys.stderr)


@sio.on('connect', namespace=CLIENT_NAMESPACE)
def on_client_namespace_connect():
    """Handle successful connection of the /client namespace."""
    print('connection established on /client namespace')


@sio.on('disconnect', namespace=CLIENT_NAMESPACE)
def on_client_namespace_disconnect():
    """Handle disconnection of the /client namespace."""
    print('ERROR: disconnected from /client namespace', file=sys.stderr)


@sio.on('connect_error', namespace=CLIENT_NAMESPACE)
def on_client_namespace_connect_error(data):
    """Handle connection error for the /client namespace."""
    print(f'ERROR: /client namespace connection failed: {data}', file=sys.stderr)


@sio.on(EVENT_SERVER_CONSTANTS, namespace=CLIENT_NAMESPACE)
def on_server_constants(data):
    """Receive pushed constants from server and refresh local runtime cache."""
    try:
        _merge_server_constants(data)
    except RuntimeError:
        # Keep existing cache if server temporarily emits an invalid payload.
        pass

def connect_client(url: str) -> None:
    """
    Connects the client to the server at the given URL.

    :param url: URL of the server
    """
    global _server_constants_cache, _canvas_size_cache

    # Reset runtime cache before a new connection attempt.
    _server_constants_cache = None
    _canvas_size_cache = None

    # Prefer WebSocket to avoid polling request timeout churn under heavy update traffic.
    try:
        sio.connect(url, namespaces=[CLIENT_NAMESPACE], transports=["websocket"], wait_timeout=20)
    except socketio.exceptions.ConnectionError:
        # Fallback keeps compatibility when WebSocket upgrade is temporarily unavailable.
        sio.connect(url, namespaces=[CLIENT_NAMESPACE], wait_timeout=20)

    try:
        # Fetch constants once at startup and use cache afterwards.
        _fetch_and_cache_server_constants()
    except Exception as exc:
        sio.disconnect()
        raise ConnectionError("Could not fetch server constants at startup.") from exc

def get_canvas_size() -> dict[str, int]:
    """Return the renderer canvas size defined by the server.

    :return: Dictionary with "width" and "height" integer keys.
    """
    global _canvas_size_cache

    if _canvas_size_cache is not None:
        return _canvas_size_cache

    if not sio.connected:
        raise ConnectionError(DISCONNECTED_MESSAGE)

    if _canvas_size_cache is None:
        raise RuntimeError("Canvas size is not synchronized yet. Wait for server constants.")

    return _canvas_size_cache


def get_server_constants() -> dict[str, int | float]:
    """Return runtime constants synchronized from the server.

    :return: Dictionary containing server-side runtime constants.
    """
    if _server_constants_cache is not None:
        return _server_constants_cache.copy()

    if not sio.connected:
        raise ConnectionError(DISCONNECTED_MESSAGE)

    if _server_constants_cache is None:
        raise RuntimeError("Server constants are not synchronized yet. Wait for server_constants event.")

    return _server_constants_cache.copy()

def set_username(username: str):
    """
    Emits an event to set the username on the server.

    :param username: The username to be set for the client
    """
    if not sio.connected:
        raise ConnectionError(DISCONNECTED_MESSAGE)

    # Emit the set_username event with the provided username
    sio.emit(EVENT_SET_USERNAME, username, callback=error_handler, namespace=CLIENT_NAMESPACE)

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
