from abc import ABC, abstractmethod
from threading import Lock, Timer
import time
import uuid

# pylint: disable-next=relative-beyond-top-level
from ..constants import get_shape_update_interval_seconds
# pylint: disable-next=relative-beyond-top-level
from ..network import sio, error_handler

class SyncronizedShape(ABC):
    """Base class that synchronizes shape state with the server.

    Network lifecycle:
    1. On construction, emits one `create_shape` event.
    2. On property changes, `update_data` emits throttled `update_shape` events.
    3. On destruction, emits one `delete_shape` event.

    Update optimization:
    - Throttling: at most N updates/second (configured in constants).
    - Coalescing: if multiple changes happen quickly, only the latest state is sent.
    """

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

        # Synchronization internals for throttled/coalesced updates.
        self.__update_lock = Lock()
        self.__last_sent_payload: dict | None = None
        self.__pending_payload: dict | None = None
        self.__last_sent_at = 0.0
        self.__flush_timer: Timer | None = None

        # Emit a create_shape event with the shape's UUID, class name, and data
        created_payload = self.to_dict()
        sio.emit("create_shape", (self.__uuid, self.__class__.__name__, created_payload), callback=error_handler, namespace="/client")
        self.__last_sent_payload = created_payload
        self.__last_sent_at = time.monotonic()

    def __flush_pending_update(self):
        """Send the latest pending state after the throttle delay.

        This runs in a timer thread. It intentionally sends only one payload:
        the most recent pending state.
        """
        payload_to_send = None

        with self.__update_lock:
            self.__flush_timer = None

            # Nothing to send.
            if self.__pending_payload is None:
                return
            # Pending state became identical to last sent state.
            if self.__pending_payload == self.__last_sent_payload:
                self.__pending_payload = None
                return

            payload_to_send = self.__pending_payload
            self.__pending_payload = None
            self.__last_sent_payload = payload_to_send
            self.__last_sent_at = time.monotonic()

        sio.emit("update_shape", (self.__uuid, self.__class__.__name__, payload_to_send), callback=error_handler, namespace="/client")

    def __del__(self) -> None:
        """
        Called when the shape is garbage collected. Emits a delete_shape event
        to the server to remove the shape from the server's data structures.
        """
        try:
            with self.__update_lock:
                # Prevent a delayed update from being sent after delete.
                if self.__flush_timer is not None:
                    self.__flush_timer.cancel()
                    self.__flush_timer = None
                self.__pending_payload = None

            # Emit a delete_shape event with the shape's UUID
            if sio.connected:
                sio.emit("delete_shape", self.__uuid, callback=error_handler, namespace="/client")
        except Exception:
            # Avoid raising from __del__ during interpreter shutdown.
            pass

    def update_data(self):
        """
        Queue or send an `update_shape` event with the latest shape data.

        Behavior:
        - If enough time passed since last send, emit immediately.
        - Otherwise, store as pending and schedule one timer flush.
        - If data did not change, do nothing.
        """
        payload = self.to_dict()
        payload_to_send = None

        with self.__update_lock:
            # Skip no-op updates.
            if payload == self.__last_sent_payload and self.__pending_payload is None:
                return

            now = time.monotonic()
            elapsed = now - self.__last_sent_at
            update_interval = get_shape_update_interval_seconds()

            # Fast path: send now if throttle interval has elapsed.
            if elapsed >= update_interval and self.__flush_timer is None:
                self.__last_sent_payload = payload
                self.__last_sent_at = now
                payload_to_send = payload
            else:
                # Coalesce rapid changes into one pending state.
                self.__pending_payload = payload
                if self.__flush_timer is None:
                    delay = max(0.0, update_interval - elapsed)
                    self.__flush_timer = Timer(delay, self.__flush_pending_update)
                    self.__flush_timer.daemon = True
                    self.__flush_timer.start()

        if payload_to_send is not None:
            sio.emit("update_shape", (self.__uuid, self.__class__.__name__, payload_to_send), callback=error_handler, namespace="/client")

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Abstract method that should be overridden to return a dictionary representation
        of the shape's attributes. This dictionary is used for synchronization with the server.
        
        :return: A dictionary containing the shape's attributes.
        """

