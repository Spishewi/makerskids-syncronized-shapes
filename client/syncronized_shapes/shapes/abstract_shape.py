from abc import ABC, abstractmethod
import threading
import time
import uuid
import weakref
import socketio

# pylint: disable-next=relative-beyond-top-level
from ..constants import (
    CLIENT_NAMESPACE,
    DISCONNECTED_MESSAGE,
    EVENT_CREATE_SHAPE,
    EVENT_DELETE_SHAPE,
    EVENT_UPDATE_SHAPE,
    get_shape_update_interval_seconds,
)
# pylint: disable-next=relative-beyond-top-level
from ..network import sio, error_handler


def _is_client_namespace_connected() -> bool:
    """Return True only when the client namespace is connected.

    Socket.IO keeps a connection per namespace. The library only sends shape
    traffic on the `/client` namespace, so we must check that namespace rather
    than relying on the generic client connection state alone.
    """
    if not sio.connected:
        return False

    namespaces = getattr(sio, "namespaces", None)
    if isinstance(namespaces, dict):
        return CLIENT_NAMESPACE in namespaces

    # Defensive fallback for potential future API shape changes.
    try:
        return CLIENT_NAMESPACE in namespaces
    except TypeError:
        return False


def _safe_emit_client(event: str, data, callback=None) -> bool:
    """Emit on the client namespace without raising on transient disconnect races.

    Shape setters are used from beginner scripts, so the library should absorb
    transient namespace/network races internally and let the shape code decide
    when to surface a connection problem.
    """
    if not _is_client_namespace_connected():
        return False

    try:
        sio.emit(event, data, callback=callback, namespace=CLIENT_NAMESPACE)
        return True
    except (socketio.exceptions.BadNamespaceError, ConnectionError, RuntimeError, OSError):
        return False

class SynchronizedShape(ABC):
    """Base class that synchronizes shape state with the server.

    The public API stays intentionally simple: users mutate properties like
    `x`, `y`, `width`, `height`, `color`, etc. The library then packs those
    rapid property changes into a smaller number of Socket.IO messages.
    """

    # Shapes that have pending updates waiting to be flushed.
    # Weak references are used so the queue never keeps dead shapes alive.
    _dirty_shapes = weakref.WeakSet()
    # Protects access to the class-level dirty queue and flush thread setup.
    _dirty_lock = threading.Lock()
    # Single background flusher used by every synchronized shape instance.
    _flush_thread: threading.Thread | None = None

    @classmethod
    def _ensure_flush_thread_started(cls) -> None:
        """Start the background flusher once, lazily, on first shape creation."""
        with cls._dirty_lock:
            if cls._flush_thread is not None and cls._flush_thread.is_alive():
                return

            # One daemon thread is enough because it only needs to drain the
            # dirty queue at a steady cadence.
            cls._flush_thread = threading.Thread(target=cls._flush_loop, daemon=True)
            cls._flush_thread.start()

    @classmethod
    def _flush_loop(cls) -> None:
        """Periodically flush the latest pending payload for every dirty shape."""
        while True:
            # Flush more often than the requested shape interval so updates stay
            # responsive even when several property writes happen close together.
            interval = get_shape_update_interval_seconds()
            time.sleep(max(0.001, interval / 2.0))

            # Snapshot the dirty shapes under lock, then release the lock before
            # emitting network traffic. This keeps update_data() responsive.
            with cls._dirty_lock:
                shapes_to_flush = list(cls._dirty_shapes)
                cls._dirty_shapes.clear()

            # Each shape decides whether it has a pending payload to send.
            for shape in shapes_to_flush:
                shape._flush_pending_payload()

    def __init__(self) -> None:
        """
        Initializes a new synchronized shape. Ensures the client is connected 
        to the server before creating a shape UUID and emitting a create_shape event.
        """
        # The library fails fast if the client is not connected at creation time.
        if not sio.connected:
            raise ConnectionError(DISCONNECTED_MESSAGE)

        # Every shape gets a stable UUID so the server can update/delete it later.
        self.__uuid = str(uuid.uuid4())

        # Latest payload waiting to be sent. When a user changes x and then y,
        # this stores only the newest snapshot.
        self.__pending_update_payload = None

        # Last payload that was actually sent successfully.
        self.__last_sent_payload = None

        # If a flush fails because the connection dropped, we store the error so
        # the next user-visible property change can raise a clear message.
        self.__pending_update_error: Exception | None = None

        # Per-shape lock for payload/error state. The background flusher and the
        # main script thread can both touch this shape.
        self.__pending_lock = threading.Lock()

        # Creation is sent immediately so the server knows this shape exists.
        create_payload = (self.__uuid, self.__class__.__name__, self.to_dict())
        if not _safe_emit_client(EVENT_CREATE_SHAPE, create_payload):
            raise ConnectionError(DISCONNECTED_MESSAGE)

        # Treat the initial create payload as already synchronized state so
        # immediate no-op property writes do not generate redundant updates.
        self.__last_sent_payload = create_payload

        # Register the flush thread after the object is fully initialized.
        self.__class__._ensure_flush_thread_started()

    def _emit_update_payload(self, payload) -> None:
        """Emit the latest shape snapshot and remember it as the last sent state."""
        if not _safe_emit_client(EVENT_UPDATE_SHAPE, payload):
            raise ConnectionError(DISCONNECTED_MESSAGE)

        with self.__pending_lock:
            self.__last_sent_payload = payload

    def _flush_pending_payload(self) -> None:
        """Send one queued payload if there is one."""
        with self.__pending_lock:
            payload = self.__pending_update_payload
            self.__pending_update_payload = None

        # Nothing queued: the shape can be dropped from the dirty set.
        if payload is None:
            return

        try:
            self._emit_update_payload(payload)
        except ConnectionError as exc:
            # Keep the failure for the next property change so the user gets a
            # simple library-level error instead of a silent failure.
            with self.__pending_lock:
                self.__pending_update_error = exc

    def __del__(self) -> None:
        """
        Called when the shape is garbage collected. Emits a delete_shape event
        to the server to remove the shape from the server's data structures.
        """
        try:
            # Best-effort cleanup: if the connection is already gone, ignore it.
            _safe_emit_client(EVENT_DELETE_SHAPE, self.__uuid, callback=error_handler)
        except (ConnectionError, RuntimeError, OSError):
            # Avoid raising from __del__ during interpreter shutdown.
            pass

    def update_data(self):
        """
        Queue the latest shape state for background flushing.

        This is the key part of the educational API: the user just writes
        `shape.x = ...` or `shape.color = ...`. The library records the latest
        state and lets the flusher thread coalesce multiple quick changes into a
        single network update.
        """
        with self.__pending_lock:
            # If a previous flush failed, surface that error now.
            pending_error = self.__pending_update_error
            self.__pending_update_error = None

        if pending_error is not None:
            raise pending_error

        # If the namespace is already gone, fail fast with the shared message.
        if not _is_client_namespace_connected():
            raise ConnectionError(DISCONNECTED_MESSAGE)

        # Capture the current full shape state. This is the only payload we ever
        # need to send; if another property changes immediately after, the newer
        # call will overwrite this pending payload.
        payload = (self.__uuid, self.__class__.__name__, self.to_dict())
        with self.__pending_lock:
            if payload == self.__pending_update_payload:
                return

            # If nothing is currently queued, skip a redundant emit when the
            # shape already has the same last successfully sent snapshot.
            if self.__pending_update_payload is None and payload == self.__last_sent_payload:
                return

            self.__pending_update_payload = payload

        # Mark the shape dirty so the flusher thread will pick it up.
        with self.__class__._dirty_lock:
            self.__class__._dirty_shapes.add(self)

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Abstract method that should be overridden to return a dictionary representation
        of the shape's attributes. This dictionary is used for synchronization with the server.
        
        :return: A dictionary containing the shape's attributes.
        """

