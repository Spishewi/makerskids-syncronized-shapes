# Maximum number of shapes a single client can own at the same time.
MAX_SHAPES_PER_CLIENT = 100

# Socket.IO namespaces.
CLIENT_NAMESPACE = "/client"
RENDERER_NAMESPACE = "/renderer"

# Event names.
EVENT_SERVER_CONSTANTS = "server_constants"
EVENT_SHAPES_UPDATE = "shapes_update"
EVENT_USERNAMES_UPDATE = "usernames_update"

# Renderer canvas size used by both the web renderer and client logic.
RENDERER_CANVAS_WIDTH = 2000
RENDERER_CANVAS_HEIGHT = 1000

# Server-side shape bounds.
MAX_SHAPE_DIMENSION = 2000.0
MAX_SHAPE_COORDINATE = 10000.0

# Basic payload limits to protect server memory and avoid abusive inputs.
MAX_USERNAME_LENGTH = 32
MAX_SHAPE_UUID_LENGTH = 128
