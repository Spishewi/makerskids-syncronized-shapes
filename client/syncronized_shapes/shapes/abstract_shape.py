from abc import ABC, abstractmethod
import uuid
import socketio

# pylint: disable-next=relative-beyond-top-level
from ..constants import (
    CLIENT_NAMESPACE,
    DISCONNECTED_MESSAGE,
    EVENT_CREATE_SHAPE,
    EVENT_DELETE_SHAPE,
    EVENT_UPDATE_SHAPE,
)
# pylint: disable-next=relative-beyond-top-level
from ..network import sio, error_handler


def _is_client_namespace_connected() -> bool:
    """Return True only when the client namespace is connected."""
    if not sio.connected:
        return False

    namespaces = getattr(sio, "namespaces", {})
    if isinstance(namespaces, dict):
        return CLIENT_NAMESPACE in namespaces

    # Defensive fallback for potential future API shape changes.
    return CLIENT_NAMESPACE in namespaces


def _safe_emit_client(event: str, data, callback=None) -> bool:
    """Emit on client namespace without raising on transient disconnect races."""
    if not _is_client_namespace_connected():
        return False

    try:
        sio.emit(event, data, callback=callback, namespace=CLIENT_NAMESPACE)
        return True
    except (socketio.exceptions.BadNamespaceError, ConnectionError, RuntimeError, OSError):
        return False

class SynchronizedShape(ABC):
    """Base class that synchronizes shape state with the server."""

    def __init__(self) -> None:
        """
        Initializes a new synchronized shape. Ensures the client is connected 
        to the server before creating a shape UUID and emitting a create_shape event.
        """
        # Check if the client is connected to the server
        if not sio.connected:
            raise ConnectionError(DISCONNECTED_MESSAGE)

        # Generate a unique UUID for the shape
        self.__uuid = str(uuid.uuid4())

        # Emit a create_shape event with the shape's UUID, class name, and data
        if not _safe_emit_client(EVENT_CREATE_SHAPE, (self.__uuid, self.__class__.__name__, self.to_dict())):
            raise ConnectionError(DISCONNECTED_MESSAGE)

    def _emit_update_payload(self, payload) -> None:
        """Emit one shape snapshot update to the server."""

        if not _safe_emit_client(EVENT_UPDATE_SHAPE, payload):
            raise ConnectionError(DISCONNECTED_MESSAGE)

    def __del__(self) -> None:
        """
        Called when the shape is garbage collected. Emits a delete_shape event
        to the server to remove the shape from the server's data structures.
        """
        try:
            # Emit a delete_shape event with the shape's UUID
            _safe_emit_client(EVENT_DELETE_SHAPE, self.__uuid, callback=error_handler)
        except (ConnectionError, RuntimeError, OSError):
            # Avoid raising from __del__ during interpreter shutdown.
            pass

    def update_data(self):
        """
        Updates the shape's data on the server.
        """
        payload = (self.__uuid, self.__class__.__name__, self.to_dict())
        self._emit_update_payload(payload)

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Abstract method that should be overridden to return a dictionary representation
        of the shape's attributes. This dictionary is used for synchronization with the server.
        
        :return: A dictionary containing the shape's attributes.
        """

