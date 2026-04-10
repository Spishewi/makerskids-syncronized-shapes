#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SynchronizedShape
from .bullet import Bullet
# pylint: disable-next=relative-beyond-top-level
from ..validators import validate_color, validate_coordinate
import math


HEIGHT = 40
MAX_BULLETS = 5
class SpaceShip(SynchronizedShape):




    def __init__(self, x: float | int, y: float | int, rotation: float | int, color: tuple[int, int, int] | list[int]) -> None:
        self.__bullets = []
        """
        Initializes a spaceship with the given position, dimensions, and color.

        :param x: The x-coordinate of the spaceship
        :param y: The y-coordinate of the spaceship
        :param color: The color of the spaceship as an (R, G, B) tuple
        """
        # Set the x-coordinate of the spaceship
        self.__x = validate_coordinate("x", x)

        # Set the y-coordinate of the spaceship
        self.__y = validate_coordinate("y", y)

        # Set the rotation of the spaceship
        if not (isinstance(rotation, float) or isinstance(rotation, int)):
            raise TypeError("Expected float or int, got " + type(rotation).__name__)
        self.__rotation = float(rotation)
       

        self.__color = validate_color("color", color)

        # Initialize the parent SynchronizedShape class
        super().__init__()


    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the spaceship.

        This is used to serialize the spaceship data when sending it to the server.

        :return: A dictionary containing the spaceship data
        """
        return {
            # The x-coordinate of the spaceship
            '__x': self.__x,
            # The y-coordinate of the spaceship
            '__y': self.__y,
            # The rotation of the ship
            '__rotation': self.__rotation,
            # The color of the spaceship as an (R, G, B) tuple
            '__color': self.__color
        }

    @property
    def x(self) -> float:
        """
        The x-coordinate of the spaceship.
        """
        return self.__x

    @x.setter
    def x(self, v: float | int):
        self.__x = validate_coordinate("x", v)
        self.update_data()

    @property
    def y(self) -> float:
        """
        The y-coordinate of the spaceship.
        """
        return self.__y

    @y.setter
    def y(self, v: float | int):
        self.__y = validate_coordinate("y", v)
        self.update_data()

    @property
    def rotation(self) -> float:
        """
        The rotation of the spaceship.
        """
        return self.__rotation

    @rotation.setter
    def rotation(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__rotation = float(v)
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the spaceship as an (R, G, B) tuple.
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        self.__color = validate_color("color", v)
        self.update_data()

    def shoot(self):
        # Keep at most MAX_BULLETS active bullets.
        if len(self.__bullets) < MAX_BULLETS:
            dx = math.sin(math.radians(self.__rotation)) * HEIGHT
            dy = -math.cos(math.radians(self.__rotation)) * HEIGHT
            b = Bullet(self.__x+dx, self.__y+dy, self.__rotation, self.color)
            self.__bullets.append(b)
    
    def update(self):
        # Build a new list to avoid removing from the list while iterating.
        active_bullets = []
        for b in self.__bullets:
            b.update()
            if not b.isOut():
                active_bullets.append(b)
        self.__bullets = active_bullets

        
        
