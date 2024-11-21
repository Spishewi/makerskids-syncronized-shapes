SUPPORTED_SHAPES = [
    "Rectangle",
    "Ellipse",
    "Line",
    "SpaceShip"
    ]

# list of all the shapes with their data (dict[shape_uuid, dict])
shapes_data: dict[str, dict] = {}

# dictonary of all the clients and their shapes (dict[sid, set[shape_uuid]])
shapes_owner: dict[str, set[str]] = {}

# clients usernames (dict[sid, username])
usernames: dict[str, str] = {}
