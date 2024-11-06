#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape

class Ellipse(SyncronizedShape):
    def __init__(self, x: float, y: float, x_radius: float, y_radius: float, color: tuple[int, int, int]) -> None:
        """
        Initializes a ellipse with the given position, radius, and color.

        :param x: The x-coordinate of the ellipse
        :param y: The y-coordinate of the ellipse
        :param x_radius: The x-radius of the ellipse
        :param y_radius: The y-radius of the ellipse
        :param color: The color of the ellipse as an (R, G, B) tuple
        """
        # Set the x-coordinate of the ellipse
        self.__x = x
        # Set the y-coordinate of the ellipse
        self.__y = y
        # Set the x-radius of the ellipse
        self.__x_radius = x_radius
        # Set the y-radius of the ellipse
        self.__y_radius = y_radius
        # Set the color of the ellipse
        self.__color = color

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
    def x(self, v: float):
        self.__x = v
        self.update_data()

    @property
    def y(self) -> float:
        """
        The y-coordinate of center of the ellipse.
        """
        return self.__y

    @y.setter
    def y(self, v: float):
        self.__y = v
        self.update_data()

    @property
    def x_radius(self) -> float:
        """
        The x-radius of the ellipse.
        """
        return self.__x_radius

    @x_radius.setter
    def x_radius(self, v: float):
        self.__x_radius = v
        self.update_data()

    @property
    def y_radius(self) -> float:
        """
        The y-radius of the ellipse.
        """
        return self.__y_radius

    @y_radius.setter
    def y_radius(self, v: float):
        self.__y_radius = v
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the ellipse as an (R, G, B) tuple
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int]):
        self.__color = v
        self.update_data()
