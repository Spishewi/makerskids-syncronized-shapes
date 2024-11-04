from threading import Lock

SUPPORTED_SHAPES = [
    "Rectangle",
    "Ellipse",
    "Line"
    ]

# WARNING: ALLWAYS LOCK IN THIS ORDER
# shapes_data_lock -> shapes_owner_lock -> usernames_lock

# list of all the shapes with their data (dict[shape_uuid, dict])
shapes_data: dict[str, dict] = {}
shapes_data_lock = Lock()

# dictonary of all the clients and their shapes (dict[sid, set[shape_uuid]])
shapes_owner: dict[str, set[str]] = {}
shapes_owner_lock = Lock()

# clients usernames (dict[sid, username])
usernames: dict[str, str] = {}
usernames_lock = Lock()
