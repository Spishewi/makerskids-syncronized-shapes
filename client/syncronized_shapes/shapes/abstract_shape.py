from abc import ABC, abstractmethod
import uuid

# pylint: disable-next=relative-beyond-top-level
from ..network import sio, error_handler

class SyncronizedShape(ABC):
    def __init__(self) -> None:
        """
        Initializes a new synchronized shape. Ensures the client is connected 
        to the server before creating a shape UUID and emitting a create_shape event.
        """
        # Check if the client is connected to the server
        if not sio.connected:
            raise ConnectionError("Please be connected to the server !")

        # Generate a unique UUID for the shape
        self.__uuid = str(uuid.uuid4())

        # Emit a create_shape event with the shape's UUID, class name, and data
        sio.emit("create_shape", (self.__uuid, self.__class__.__name__, self.to_dict()), callback=error_handler, namespace="/client")

    def __del__(self) -> None:
        """
        Called when the shape is garbage collected. Emits a delete_shape event
        to the server to remove the shape from the server's data structures.
        """
        # Emit a delete_shape event with the shape's UUID
        sio.emit("delete_shape", self.__uuid, callback=error_handler, namespace="/client")

    def update_data(self):
        """
        Updates the shape's data on the server. Emits an update_shape event
        with the shape's UUID, class name, and data.
        """
        # Emit an update_shape event with the shape's UUID, class name, and data
        sio.emit("update_shape", (self.__uuid, self.__class__.__name__, self.to_dict()), callback=error_handler, namespace="/client")

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Abstract method that should be overridden to return a dictionary representation
        of the shape's attributes. This dictionary is used for synchronization with the server.
        
        :return: A dictionary containing the shape's attributes.
        """

