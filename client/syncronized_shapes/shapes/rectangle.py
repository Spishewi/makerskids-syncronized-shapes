#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SynchronizedShape
# pylint: disable-next=relative-beyond-top-level
from ..validators import validate_color, validate_coordinate, validate_positive_dimension

class Rectangle(SynchronizedShape):
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
        self.__x = validate_coordinate("x", x)

        # Set the y-coordinate of the rectangle
        self.__y = validate_coordinate("y", y)

        # Set the width of the rectangle
        self.__width = validate_positive_dimension("width", width)

        # Set the height of the rectangle
        self.__height = validate_positive_dimension("height", height)

        self.__color = validate_color("color", color)

        # Initialize the parent SynchronizedShape class
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
        self.__x = validate_coordinate("x", v)
        self.update_data()

    @property
    def y(self) -> float:
        """
        The y-coordinate of the rectangle.
        """
        return self.__y

    @y.setter
    def y(self, v: float | int):
        self.__y = validate_coordinate("y", v)
        self.update_data()

    @property
    def width(self) -> float:
        """
        The width of the rectangle.
        """
        return self.__width

    @width.setter
    def width(self, v: float | int):
        self.__width = validate_positive_dimension("width", v)
        self.update_data()

    @property
    def height(self) -> float:
        """
        The height of the rectangle.
        """
        return self.__height

    @height.setter
    def height(self, v: float | int):
        self.__height = validate_positive_dimension("height", v)
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the rectangle as an (R, G, B) tuple.
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        self.__color = validate_color("color", v)
        self.update_data()
