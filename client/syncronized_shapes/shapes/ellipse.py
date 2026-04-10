#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SynchronizedShape
# pylint: disable-next=relative-beyond-top-level
from ..validators import validate_color, validate_coordinate, validate_positive_dimension

class Ellipse(SynchronizedShape):
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
        self.__x = validate_coordinate("x", x)

        # Set the y-coordinate of the ellipse
        self.__y = validate_coordinate("y", y)

        # Set the x-radius of the ellipse
        self.__x_radius = validate_positive_dimension("x_radius", x_radius)

        # Set the y-radius of the ellipse
        self.__y_radius = validate_positive_dimension("y_radius", y_radius)

        # Set the color of the ellipse
        self.__color = validate_color("color", color)

        # Initialize the parent SynchronizedShape class
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
        self.__x = validate_coordinate("x", v)
        self.update_data()

    @property
    def y(self) -> float:
        """
        The y-coordinate of center of the ellipse.
        """
        return self.__y

    @y.setter
    def y(self, v: float | int):
        self.__y = validate_coordinate("y", v)
        self.update_data()

    @property
    def x_radius(self) -> float:
        """
        The x-radius of the ellipse.
        """
        return self.__x_radius

    @x_radius.setter
    def x_radius(self, v: float | int):
        self.__x_radius = validate_positive_dimension("x_radius", v)
        self.update_data()

    @property
    def y_radius(self) -> float:
        """
        The y-radius of the ellipse.
        """
        return self.__y_radius

    @y_radius.setter
    def y_radius(self, v: float | int):
        self.__y_radius = validate_positive_dimension("y_radius", v)
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the ellipse as an (R, G, B) tuple
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        self.__color = validate_color("color", v)
        self.update_data()
