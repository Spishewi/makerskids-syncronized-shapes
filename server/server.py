from aiohttp import web
import socketio

from globals import SUPPORTED_SHAPES

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

# list of all the shapes with their data
shapes_data: dict[str, dict] = {}

# dictonary of all the clients and their shapes
shapes_owner: dict[str, set[str]] = {}

@sio.event
def connect(sid, environ): #pylint: disable=unused-argument
    """
    When a client connect, this function is called.
    For now, it just creates a new empty set of shapes.
    """
    print("connect ", sid)
    # add the client to the list of connected clients
    shapes_owner[sid] = set()

@sio.event
def disconnect(sid):
    """
    Handles the disconnection of a client. Removes all shapes associated 
    with the client and cleans up client data from the server.
    """
    print('disconnect ', sid)

    # Remove all shapes associated with the client
    for shape_uuid in shapes_owner[sid]:
        del shapes_data[shape_uuid]

    # Remove the client from the list of shape owners
    del shapes_owner[sid]

    print(f"all {sid} shapes have been deleted")

@sio.event
async def create_shape(sid, shape_uuid, shape_type, shape_data):
    """
    Handles the creation of a new shape. Validates the input data,
    checks for existing shapes, and updates the server's data structures.

    :param sid: Session ID for the client
    :param shape_uuid: String containing shape UUID
    :param shape_type: String containing shape type
    :param shape_data: Dictionary containing shape data

    :return: a tuple of (status, message)
    """
    # basics sanity checks

    # shape_uuid must be a string
    if not isinstance(shape_uuid, str):
        return 400, "SHAPE_UUID MUST BE A STRING"

    #shape_type must be a string
    if not isinstance(shape_type, str):
        return 400, "SHAPE_TYPE MUST BE A STRING"

    # shape_type must be one of the supported shapes
    if shape_type not in SUPPORTED_SHAPES:
        return 400, "SHAPE_TYPE MUST BE A SUPPORTED SHAPE"

    # shape_data must be a dictionary
    if not isinstance(shape_data, dict):
        return 400, "SHAPE_DATA MUST BE A DICTIONARY"

    # shape musn't already exist
    if shape_uuid in shapes_data:
        return 400, "THIS SHAPE ALREADY EXISTS. YOU CAN'T CREATE A SHAPE THAT ALREADY EXISTS"

    # Add the new shape to the server's data structures
    shapes_data[shape_uuid] = (shape_type, shape_data)
    shapes_owner[sid].add(shape_uuid)

    # Return success status and message
    return 200, "OK"

@sio.event
async def update_shape(sid, shape_uuid, shape_type, shape_data):
    """
    Handles the update of a shape. Validates the input data,
    checks if the shape already exists, and updates the server's data structures.

    :param sid: Session ID for the client
    :param shape_uuid: String containing shape UUID
    :param shape_type: String containing shape type
    :param shape_data: Dictionary containing shape data

    :return: a tuple of (status, message)
    """
    # basics sanity checks

    # shape_uuid must be a string
    if not isinstance(shape_uuid, str):
        return 400, "SHAPE_UUID MUST BE A STRING"

    #shape_type must be a string
    if not isinstance(shape_type, str):
        return 400, "SHAPE_TYPE MUST BE A STRING"

    # shape_data must be a dictionary
    if not isinstance(shape_data, dict):
        return 400, "SHAPE_DATA MUST BE A DICTIONARY"

    # shape musn't already exist
    if shape_uuid not in shapes_data:
        return 400, "THIS SHAPE DOESN'T EXIST"

    # shape must be of the same type
    if shape_type != shapes_data[shape_uuid][0]:
        return 400, "YOU CAN'T UPDATE A THIS SHAPE TO A DIFFERENT TYPE"

    # we add the shapes to ours data
    shapes_data[shape_uuid] = (shape_type, shape_data)
    shapes_owner[sid].add(shape_uuid)

    return 200, "OK"

@sio.event
async def delete_shape(sid, shape_uuid):
    """
    Handles the deletion of a shape.
    Validates the input data, and updates the server's data structures.

    :param sid: Session ID for the client
    :param shape_uuid: String containing shape UUID
    :return: a tuple of (status, message)
    """
    # basics sanity checks
    if not isinstance(shape_uuid, str):
        return 400, "DATA IS NOT A STRING"

    # if it exists
    if shape_uuid not in shapes_data:
        return 400, "THIS SHAPE DOESN'T EXIST"

    # remove the shape from the server's data structures
    del shapes_data[shape_uuid]

    # remove the shape from the client's list of shapes
    shapes_owner[sid].discard(shape_uuid)

    return 200, "OK"

