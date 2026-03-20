import sys
import socketio

sio = socketio.Client()
_canvas_size_cache: dict[str, int] | None = None
_server_constants_cache: dict[str, int | float] | None = None
_is_runtime_synced = False


def _validate_server_constants_payload(data: dict) -> dict[str, int | float]:
    required_keys = [
        "max_shapes_per_client",
        "max_username_length",
        "max_shape_uuid_length",
        "max_shape_dimension",
        "max_shape_coordinate",
        "renderer_canvas_width",
        "renderer_canvas_height",
    ]

    if not isinstance(data, dict):
        raise RuntimeError("Invalid server constants payload")

    missing_keys = [key for key in required_keys if key not in data]
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


def _sync_runtime_state() -> None:
    global _is_runtime_synced

    if not sio.connected:
        raise ConnectionError("Please be connected to the server !")

    constants_payload = sio.call("get_server_constants", namespace="/client", timeout=2)
    _merge_server_constants(constants_payload)

    _is_runtime_synced = True

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


@sio.on("server_constants", namespace="/client")
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
    try:
        # Connect to the server.
        sio.connect(url, namespaces=["/client"])

        # Block until runtime constants and canvas size are synchronized.
        _sync_runtime_state()
    except Exception:
        # Avoid leaving a half-initialized connected socket on sync failure.
        if sio.connected:
            sio.disconnect()
        raise

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

    # Refresh from constants to keep one authoritative source.
    _sync_runtime_state()

    if _canvas_size_cache is None:
        raise RuntimeError("Canvas size is not synchronized yet. Call connect_client first.")

    return _canvas_size_cache


def get_server_constants(force_refresh: bool = False) -> dict[str, int | float]:
    """Return runtime constants synchronized from the server.

    :param force_refresh: If True, always request fresh data from server.
    :return: Dictionary containing server-side runtime constants.
    """
    if not sio.connected:
        raise ConnectionError("Please be connected to the server !")

    if force_refresh:
        _sync_runtime_state()

    if not _is_runtime_synced or _server_constants_cache is None:
        raise RuntimeError("Runtime state is not synchronized yet. Call connect_client first.")

    return _server_constants_cache.copy()

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
