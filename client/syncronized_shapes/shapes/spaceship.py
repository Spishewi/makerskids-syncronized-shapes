#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape
from .bullet import Bullet
import math


HEIGHT = 40
MAX_BULLETS = 5
class SpaceShip(SyncronizedShape):




    def __init__(self, x: float | int, y: float | int, rotation: float | int, color: tuple[int, int, int] | list[int]) -> None:
        self.__bullets = []
        """
        Initializes a spaceshit with the given position, dimensions, and color.

        :param x: The x-coordinate of the spaceshit
        :param y: The y-coordinate of the spaceshit
        :param color: The color of the spaceshit as an (R, G, B) tuple
        """
        # Set the x-coordinate of the spaceshit
        if not (isinstance(x, float) or isinstance(x, int)):
            raise TypeError("Expected float or int, got " + type(x).__name__)
        self.__x = float(x)

        # Set the y-coordinate of the spaceshit
        if not (isinstance(y, float) or isinstance(y, int)):
            raise TypeError("Expected float or int, got " + type(y).__name__)
        self.__y = float(y)

        # Set the y-coordinate of the spaceshit
        if not (isinstance(rotation, float) or isinstance(rotation, int)):
            raise TypeError("Expected float or int, got " + type(rotation).__name__)
        self.__rotation = float(rotation)
       

        # Set the color of the spaceshit
        if not (isinstance(color, tuple) or isinstance(color, list)) or len(color) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            raise TypeError("Expected tuple or list of 3 integers between 0 and 255, got " + type(color).__name__)
        self.__color = tuple(color)

        # Initialize the parent SyncronizedShape class
        super().__init__()


    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the spaceshit.

        This is used to serialize the spaceshit's data when sending it to the server.

        :return: A dictionary containing the spaceshit's data
        """
        return {
            # The x-coordinate of the spaceshit
            '__x': self.__x,
            # The y-coordinate of the spaceshit
            '__y': self.__y,
            # The rotation of the ship
            '__rotation': self.__rotation,
            # The color of the spaceshit as an (R, G, B) tuple
            '__color': self.__color
        }

    @property
    def x(self) -> float:
        """
        The x-coordinate of the spaceshit.
        """
        return self.__x

    @x.setter
    def x(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__x = float(v)
        self.update_data()

    @property
    def y(self) -> float:
        """
        The y-coordinate of the spaceshit.
        """
        return self.__y

    @y.setter
    def y(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__y = float(v)
        self.update_data()

    @property
    def rotation(self) -> float:
        """
        The y-coordinate of the spaceshit.
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
        The color of the spaceshit as an (R, G, B) tuple.
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        if not (isinstance(v, tuple) or isinstance(v, list)) or len(v) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in v):
            raise TypeError("Expected tuple or list of 3 integers between 0 and 255, got " + type(v).__name__)
        self.__color = tuple(v)
        self.update_data()

    def shoot(self):
        if len(self.__bullets)<=MAX_BULLETS:
            dx = math.sin(math.radians(self.__rotation)) * HEIGHT
            dy = -math.cos(math.radians(self.__rotation)) * HEIGHT
            b = Bullet(self.__x+dx, self.__y+dy, self.__rotation, self.color)
            self.__bullets.append(b)
    
    def update(self):
        for b in self.__bullets:
            b.update()
            if(b.isOut()):
                self.__bullets.remove(b)

        
        
