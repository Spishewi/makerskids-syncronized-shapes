from aiohttp import web
import socketio

import constants as c

# pylint: disable-next=unused-wildcard-import,wildcard-import
import variables as g

sio = socketio.AsyncServer(
    async_mode="aiohttp",
    cors_allowed_origins="*",
    debug=True
)
app = web.Application()
sio.attach(app)

class ClientNamespace(socketio.AsyncNamespace):
    """
    Namespace for the client.
    """

    # events
    async def on_connect(self, sid, environ): #pylint: disable=unused-argument
        """
        When a client connect, this function is called.
        For now, it just creates a new empty set of shapes.
        """
        print("connect client", sid)

        # create an empty set of shapes for the client
        # this will be used to store the shape UUIDs
        g.shapes_owner[sid] = set()

        # set the default client's username
        g.usernames[sid] = sid

        await RendererNamespace.emit_usernames_update(sid)


    async def on_disconnect(self, sid):
        """
        Handles the disconnection of a client. Removes all shapes associated 
        with the client and cleans up client data from the server.
        """
        print('disconnect client', sid)

        # Make disconnect idempotent: client can already be partially removed.
        if sid not in g.shapes_owner and sid not in g.usernames:
            return

        #list of shapes that has been deleted
        deleted_shapes = []

        # Remove all shapes associated with the client
        for shape_uuid in g.shapes_owner.get(sid, set()):
            deleted_shapes.append(shape_uuid)
            g.shapes_data.pop(shape_uuid, None)

        # Remove the client from the list of shape owners
        g.shapes_owner.pop(sid, None)
        g.usernames.pop(sid, None)

        # emit to the renderer the shapes that have been deleted
        await RendererNamespace.emit_shapes_update(sid, deleted_shapes=deleted_shapes)

        # emit to the renderer the updated list of usernames
        await RendererNamespace.emit_usernames_update(sid)


        print(f"all {sid} shapes have been deleted")


    async def on_set_username(self, sid, username):
        """
        Handles the setting of a username. Updates the server's data structures
        with the new username.

        :param sid: Session ID for the client
        :param username: String containing the username
        """

        # basics sanity checks

        # username must be a string
        if not isinstance(username, str):
            return 400, "USERNAME MUST BE A STRING"

        # client must exist
        if sid not in g.usernames or sid not in g.shapes_owner:
            return 400, "UNKNOWN CLIENT"

        username = username.strip()
        if len(username) == 0:
            return 400, "USERNAME MUST NOT BE EMPTY"
        if len(username) > c.MAX_USERNAME_LENGTH:
            return 400, f"USERNAME TOO LONG (MAX {c.MAX_USERNAME_LENGTH})"

        # Do nothing if the username is already set
        if g.usernames[sid] == username:
            return 200, "OK"

        # Username must be unique
        if username in g.usernames.values():
            return 400, "USERNAME ALREADY EXISTS"

        #set the username
        g.usernames[sid] = username

        # emit to the renderer the updated list of usernames
        await RendererNamespace.emit_usernames_update(sid)

        return 200, "OK"


    async def on_create_shape(self, sid, shape_uuid, shape_type, shape_data):
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
        if len(shape_uuid) == 0:
            return 400, "SHAPE_UUID MUST NOT BE EMPTY"
        if len(shape_uuid) > c.MAX_SHAPE_UUID_LENGTH:
            return 400, f"SHAPE_UUID TOO LONG (MAX {c.MAX_SHAPE_UUID_LENGTH})"

        #shape_type must be a string
        if not isinstance(shape_type, str):
            return 400, "SHAPE_TYPE MUST BE A STRING"

        # shape_type must be one of the supported shapes
        if shape_type not in g.SUPPORTED_SHAPES:
            return 400, "SHAPE_TYPE MUST BE A SUPPORTED SHAPE"

        # shape_data must be a dictionary
        if not isinstance(shape_data, dict):
            return 400, "SHAPE_DATA MUST BE A DICTIONARY"

        # shape musn't already exist
        if shape_uuid in g.shapes_data:
            return 400, "THIS SHAPE ALREADY EXISTS. YOU CAN'T CREATE A SHAPE THAT ALREADY EXISTS"

        # client must not exceed the configured number of shapes
        if sid not in g.shapes_owner:
            return 400, "UNKNOWN CLIENT"
        if len(g.shapes_owner[sid]) >= c.MAX_SHAPES_PER_CLIENT:
            return 400, f"MAX SHAPES PER CLIENT REACHED ({c.MAX_SHAPES_PER_CLIENT})"

        # Add the new shape to the server's data structures
        g.shapes_data[shape_uuid] = (shape_type, shape_data)
        g.shapes_owner[sid].add(shape_uuid)

        # emit to the renderer the new shape
        await RendererNamespace.emit_shapes_update(sid, new_shapes=[(shape_uuid, shape_type, shape_data)])

        return 200, "OK"


    async def on_update_shape(self, sid, shape_uuid, shape_type, shape_data):
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

        # client must exist
        if sid not in g.shapes_owner:
            return 400, "UNKNOWN CLIENT"

        #shape_type must be a string
        if not isinstance(shape_type, str):
            return 400, "SHAPE_TYPE MUST BE A STRING"

        # shape_data must be a dictionary
        if not isinstance(shape_data, dict):
            return 400, "SHAPE_DATA MUST BE A DICTIONARY"

        # shape musn't already exist
        if shape_uuid not in g.shapes_data:
            return 400, "THIS SHAPE DOESN'T EXIST"

        # shape must be of the same type
        if shape_type != g.shapes_data[shape_uuid][0]:
            return 400, "YOU CAN'T UPDATE A THIS SHAPE TO A DIFFERENT TYPE"

        # clients can only update their own shapes
        if shape_uuid not in g.shapes_owner[sid]:
            return 400, "YOU CAN'T UPDATE A SHAPE YOU DON'T OWN"

        # we add the shapes to ours data
        g.shapes_data[shape_uuid] = (shape_type, shape_data)
        #g.shapes_owner[sid].add(shape_uuid) # I think i don't need this

        # emit to the renderer the updated shape
        await RendererNamespace.emit_shapes_update(sid, updated_shapes=[(shape_uuid, shape_type, shape_data)])

        return 200, "OK"


    async def on_delete_shape(self, sid, shape_uuid):
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

        # client must exist
        if sid not in g.shapes_owner:
            return 400, "UNKNOWN CLIENT"

        # if it exists
        if shape_uuid not in g.shapes_data:
            return 400, "THIS SHAPE DOESN'T EXIST"

        # clients can only delete their own shapes
        if shape_uuid not in g.shapes_owner[sid]:
            return 400, "YOU CAN'T DELETE A SHAPE YOU DON'T OWN"

        # remove the shape from the server's data structures
        g.shapes_data.pop(shape_uuid, None)

        # remove the shape from the client's list of shapes
        g.shapes_owner[sid].discard(shape_uuid)
        
        # emit to the renderer the deleted shape
        await RendererNamespace.emit_shapes_update(sid, deleted_shapes=[shape_uuid])

        return 200, "OK"

    async def on_get_canvas_size(self, sid):
        """Return the renderer canvas size configured on the server."""
        # sid is kept for API symmetry with other events.
        return {
            "width": c.RENDERER_CANVAS_WIDTH,
            "height": c.RENDERER_CANVAS_HEIGHT,
        }

class RendererNamespace(socketio.AsyncNamespace):
    """
    Namespace for the renderer.
    """

    # events
    def on_connect(self, sid, environ):
        """
        Triggered when the renderer connects to the server.
        Prints a message to the console.

        :param sid: Session ID for the client
        :param environ: Environment dictionary containing request parameters
        """
        print("connect renderer", sid)

    def on_disconnect(self, sid):
        """
        Triggered when the renderer disconnects.
        Prints a message to the console.

        :param sid: Session ID for the client
        """
        print("disconnect renderer", sid)

    async def on_get_shapes(self, sid):
        """
        Triggered when the renderer needs a full update of the shapes.
        Returns the current state of all shapes in the server's data structures.

        :param sid: Session ID for the client
        """
        return g.shapes_data
    
    async def on_get_usernames(self, sid):
        """
        Triggered when the renderer needs a full update of the usernames.
        Returns the current state of all usernames in the server's data structures.

        :param sid: Session ID for the client
        """
        return g.usernames

    async def on_get_canvas_size(self, sid):
        """Return the renderer canvas size configured on the server."""
        # sid is kept for API symmetry with other events.
        return {
            "width": c.RENDERER_CANVAS_WIDTH,
            "height": c.RENDERER_CANVAS_HEIGHT,
        }

    # emits
    @staticmethod
    async def emit_shapes_update(sid, deleted_shapes:list = None, updated_shapes:list = None, new_shapes:list = None):
        """
        Emits a "shapes_update" event to the renderer client with the given sid.
        The event contains the list of deleted, updated and new shapes.

        :param sid: Session ID for the client
        :param deleted_shapes: List of shape UUIDs that have been deleted
        :param updated_shapes: List of shape UUIDs and data that have been updated
        :param new_shapes: List of shape UUIDs and data that have been added
        """
        # set default values
        deleted_shapes = [] if deleted_shapes is None else deleted_shapes
        updated_shapes = [] if updated_shapes is None else updated_shapes
        new_shapes = [] if new_shapes is None else new_shapes

        # emit the event to the renderer
        await sio.emit("shapes_update", {
            "deleted": deleted_shapes,
            "updated": updated_shapes,
            "new": new_shapes
            },
            namespace="/renderer"
        )

    @staticmethod
    async def emit_usernames_update(sid):
        """
        Emits a "usernames_update" event to the renderer client with the given sid.
        The event contains the list of usernames.

        :param sid: Session ID for the client
        :param usernames: List of usernames
        """
        # emit the event to the renderer
        await sio.emit("usernames_update", g.usernames, namespace="/renderer")

# register the namespaces
sio.register_namespace(ClientNamespace("/client"))
sio.register_namespace(RendererNamespace("/renderer"))

# add the static files
app.router.add_static('/static', './web/static')

# add the web renderer
async def renderer_index(request): # pylint: disable=unused-argument
    """Serve the client-side application."""
    with open('./web/renderer/index.html', encoding='utf-8') as f:
        return web.Response(text=f.read(), content_type='text/html')

app.router.add_get('/renderer', renderer_index)
