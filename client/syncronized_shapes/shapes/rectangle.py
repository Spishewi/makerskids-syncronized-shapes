#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape

class Rectangle(SyncronizedShape):
    def __init__(self, x: float | int, y: float | int, width: float | int, height: float | int, color: tuple[int, int, int] | list[int]) -> None:
        """
        Initializes a rectangle with the given position, dimensions, and color.

        :param x: The x-coordinate of the rectangle
        :param y: The y-coordinate of the rectangle
        :param width: The width of the rectangle
        :param height: The height of the rectangle
        :param color: The color of the rectangle as an (R, G, B) tuple
        """
        # Set the x-coordinate of the rectangle
        if not (isinstance(x, float) or isinstance(x, int)):
            raise TypeError("Expected float or int, got " + type(x).__name__)
        self.__x = float(x)

        # Set the y-coordinate of the rectangle
        if not (isinstance(y, float) or isinstance(y, int)):
            raise TypeError("Expected float or int, got " + type(y).__name__)
        self.__y = float(y)

        # Set the width of the rectangle
        if not (isinstance(width, float) or isinstance(width, int)):
            raise TypeError("Expected float or int, got " + type(width).__name__)
        self.__width = float(width)

        # Set the height of the rectangle
        if not (isinstance(height, float) or isinstance(height, int)):
            raise TypeError("Expected float or int, got " + type(height).__name__)
        self.__height = float(height)

        # Set the color of the rectangle
        if not (isinstance(color, tuple) or isinstance(color, list)) or len(color) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            raise TypeError("Expected tuple or list of 3 integers between 0 and 255, got " + type(color).__name__)
        self.__color = tuple(color)

        # Initialize the parent SyncronizedShape class
        super().__init__()


    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the rectangle.

        This is used to serialize the rectangle's data when sending it to the server.

        :return: A dictionary containing the rectangle's data
        """
        return {
            # The x-coordinate of the rectangle
            '__x': self.__x,
            # The y-coordinate of the rectangle
            '__y': self.__y,
            # The width of the rectangle
            '__width': self.__width,
            # The height of the rectangle
            '__height': self.__height,
            # The color of the rectangle as an (R, G, B) tuple
            '__color': self.__color
        }

    @property
    def x(self) -> float:
        """
        The x-coordinate of the rectangle.
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
        The y-coordinate of the rectangle.
        """
        return self.__y

    @y.setter
    def y(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__y = float(v)
        self.update_data()

    @property
    def width(self) -> float:
        """
        The width of the rectangle.
        """
        return self.__width

    @width.setter
    def width(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__width = float(v)
        self.update_data()

    @property
    def height(self) -> float:
        """
        The height of the rectangle.
        """
        return self.__height

    @height.setter
    def height(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__height = float(v)
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the rectangle as an (R, G, B) tuple.
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        if not (isinstance(v, tuple) or isinstance(v, list)) or len(v) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in v):
            raise TypeError("Expected tuple or list of 3 integers between 0 and 255, got " + type(v).__name__)
        self.__color = tuple(v)
        self.update_data()
