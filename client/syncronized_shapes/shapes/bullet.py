#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape
# pylint: disable-next=relative-beyond-top-level
from ..network import get_canvas_size
# pylint: disable-next=relative-beyond-top-level
from ..validators import validate_coordinate
import math


SPEED = 10

class Bullet(SyncronizedShape):
    def __init__(self, x: float | int, y: float | int, angle:float | int, color: tuple[int, int, int] | list[int]) -> None:

        # Set the x-coordinate of the bullet
        self.__x = validate_coordinate("x", x)

        # Set the y-coordinate of the bullet
        self.__y = validate_coordinate("y", y)

        # Set the angle of the bullet
        if not (isinstance(angle, float) or isinstance(angle, int)):
            raise TypeError("Expected float or int, got " + type(angle).__name__)
        self.__angle = float(angle)

        # Set the color of the bullet
        if not (isinstance(color, tuple) or isinstance(color, list)) or len(color) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            raise TypeError("Expected tuple or list of length 3 containing ints between 0 and 255, got " + str(color))
        self.__color = tuple(color)

        # Initialize the parent SyncronizedShape class
        super().__init__()


    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the bullet.

        This is used to serialize the bullet's data when sending it to the server.

        :return: A dictionary containing the bullet's data
        """
        return {
            # The x-coordinate of the bullet
            '__x': self.__x,
            # The y-coordinate of the bullet
            '__y': self.__y,
            # The angle of the bullet (kept for future renderer usage)
            '__angle': self.__angle,
            # The color of the bullet as an (R, G, B) tuple
            '__color': self.__color
        }

    @property
    def x(self) -> float:
        """
        The x-coordinate of center of the bullet.
        """
        return self.__x

    @x.setter
    def x(self, v: float | int):
        self.__x = validate_coordinate("x", v)
        self.update_data()

    @property
    def y(self) -> float:
        """
        The y-coordinate of center of the bullet.
        """
        return self.__y

    @y.setter
    def y(self, v: float | int):
        self.__y = validate_coordinate("y", v)
        self.update_data()


    @property
    def angle(self) -> float:
        """
        The angle of the bullet.
        """
        return self.__angle

    @angle.setter
    def angle(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__angle = float(v)
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the bullet as an (R, G, B) tuple
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        if not (isinstance(v, tuple) or isinstance(v, list)) or len(v) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in v):
            raise TypeError("Expected tuple or list of length 3 containing ints between 0 and 255, got " + str(v))
        self.__color = tuple(v)
        self.update_data()

    def update(self):
        self.__x += math.sin(math.radians(self.__angle)) * SPEED
        self.__y += -math.cos(math.radians(self.__angle)) * SPEED
        self.update_data()

    def isOut(self):
        canvas_size = get_canvas_size()
        width = canvas_size["width"]
        height = canvas_size["height"]

        return self.__x < 0 or self.__y < 0 or self.__y > height or self.__x > width