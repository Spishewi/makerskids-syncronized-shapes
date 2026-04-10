"""Runtime configuration for synchronized shapes network behavior."""

# Socket.IO namespaces.
CLIENT_NAMESPACE = "/client"
RENDERER_NAMESPACE = "/renderer"

# Client event names.
EVENT_SERVER_CONSTANTS = "server_constants"
EVENT_GET_SERVER_CONSTANTS = "get_server_constants"
EVENT_SET_USERNAME = "set_username"
EVENT_CREATE_SHAPE = "create_shape"
EVENT_UPDATE_SHAPE = "update_shape"
EVENT_DELETE_SHAPE = "delete_shape"

# Shared connection error message used by network and shape layers.
DISCONNECTED_MESSAGE = "Please be connected to the server !"

# Required keys for server runtime constants payload.
SERVER_CONSTANTS_REQUIRED_KEYS = (
    "max_shapes_per_client",
    "max_username_length",
    "max_shape_uuid_length",
    "max_shape_dimension",
    "max_shape_coordinate",
    "renderer_canvas_width",
    "renderer_canvas_height",
)

# Timeout used when fetching runtime constants once at startup.
SERVER_CONSTANTS_FETCH_TIMEOUT_SECONDS = 5

# Maximum number of update messages sent per shape per second.
# This is a client-side throttle, not a guaranteed delivery rate.
# Default is tuned for smooth animations.
SHAPE_UPDATES_PER_SECOND = 60


def set_shape_updates_per_second(value: int) -> None:
    """Set the per-shape update rate limit (messages per second).

    Higher values improve animation smoothness but increase network traffic.
    Lower values reduce traffic but can make movement appear less fluid.
    """
    global SHAPE_UPDATES_PER_SECOND

    if not isinstance(value, int):
        raise TypeError(f"Expected int, got {type(value).__name__}")
    if value < 1:
        raise ValueError("SHAPE_UPDATES_PER_SECOND must be >= 1")

    SHAPE_UPDATES_PER_SECOND = value


def get_shape_update_interval_seconds() -> float:
    """Return minimum delay between two updates for one shape."""
    return 1.0 / SHAPE_UPDATES_PER_SECOND
