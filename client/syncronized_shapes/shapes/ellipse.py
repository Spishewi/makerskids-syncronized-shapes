#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape

class Ellipse(SyncronizedShape):
    def __init__(self, x: float | int, y: float | int, x_radius: float | int, y_radius: float | int, color: tuple[int, int, int] | list[int]) -> None:
        """
        Initializes a ellipse with the given position, radius, and color.

        :param x: The x-coordinate of the ellipse
        :param y: The y-coordinate of the ellipse
        :param x_radius: The x-radius of the ellipse
        :param y_radius: The y-radius of the ellipse
        :param color: The color of the ellipse as an (R, G, B) tuple
        """
        # Set the x-coordinate of the ellipse
        if not (isinstance(x, float) or isinstance(x, int)):
            raise TypeError("Expected float or int, got " + type(x).__name__)
        self.__x = float(x)

        # Set the y-coordinate of the ellipse
        if not (isinstance(y, float) or isinstance(y, int)):
            raise TypeError("Expected float or int, got " + type(y).__name__)
        self.__y = float(y)

        # Set the x-radius of the ellipse
        if not (isinstance(x_radius, float) or isinstance(x_radius, int)):
            raise TypeError("Expected float or int, got " + type(x_radius).__name__)
        self.__x_radius = float(x_radius)

        # Set the y-radius of the ellipse
        if not (isinstance(y_radius, float) or isinstance(y_radius, int)):
            raise TypeError("Expected float or int, got " + type(y_radius).__name__)
        self.__y_radius = float(y_radius)

        # Set the color of the ellipse
        if not (isinstance(color, tuple) or isinstance(color, list)) or len(color) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            raise TypeError("Expected tuple or list of length 3 containing ints between 0 and 255, got " + str(color))
        self.__color = tuple(color)

        # Initialize the parent SyncronizedShape class
        super().__init__()


    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the ellipse.

        This is used to serialize the ellipse's data when sending it to the server.

        :return: A dictionary containing the ellipse's data
        """
        return {
            # The x-coordinate of the ellipse
            '__x': self.__x,
            # The y-coordinate of the ellipse
            '__y': self.__y,
            # The x-radius of the ellipse
            '__x_radius': self.__x_radius,
            # The y-radius of the ellipse
            '__y_radius': self.__y_radius,
            # The color of the ellipse as an (R, G, B) tuple
            '__color': self.__color
        }

    @property
    def x(self) -> float:
        """
        The x-coordinate of center of the ellipse.
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
        The y-coordinate of center of the ellipse.
        """
        return self.__y

    @y.setter
    def y(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__y = float(v)
        self.update_data()

    @property
    def x_radius(self) -> float:
        """
        The x-radius of the ellipse.
        """
        return self.__x_radius

    @x_radius.setter
    def x_radius(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__x_radius = float(v)
        self.update_data()

    @property
    def y_radius(self) -> float:
        """
        The y-radius of the ellipse.
        """
        return self.__y_radius

    @y_radius.setter
    def y_radius(self, v: float | int):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise TypeError("Expected float or int, got " + type(v).__name__)
        self.__y_radius = float(v)
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the ellipse as an (R, G, B) tuple
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        if not (isinstance(v, tuple) or isinstance(v, list)) or len(v) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in v):
            raise TypeError("Expected tuple or list of length 3 containing ints between 0 and 255, got " + str(v))
        self.__color = tuple(v)
        self.update_data()
