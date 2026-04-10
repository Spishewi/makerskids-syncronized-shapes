#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SynchronizedShape
# pylint: disable-next=relative-beyond-top-level
from ..validators import validate_color, validate_coordinate

class Line(SynchronizedShape):
    def __init__(self, x1: float | int, y1: float | int, x2: float | int, y2: float | int, color: tuple[int, int, int] | list[int]) -> None:
        """
        Initializes a line with the given position, dimensions, and color.

        :param x1: The x1-coordinate of the line
        :param y1: The y1-coordinate of the line
        :param x2: The x2-coordinate of the line
        :param y2: The y2-coordinate of the line
        :param color: The color of the line as an (R, G, B) tuple
        """
        # Set the x1-coordinate of the line
        self.__x1 = validate_coordinate("x1", x1)

        # Set the y1-coordinate of the line
        self.__y1 = validate_coordinate("y1", y1)

        # Set the x2-coordinate of the line
        self.__x2 = validate_coordinate("x2", x2)

        # Set the y2-coordinate of the line
        self.__y2 = validate_coordinate("y2", y2)

        self.__color = validate_color("color", color)

        # Initialize the parent SynchronizedShape class
        super().__init__()


    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the line.

        This is used to serialize the line's data when sending it to the server.

        :return: A dictionary containing the line's data
        """
        return {
            # The x1-coordinate of the line
            '__x1': self.__x1,
            # The y1-coordinate of the line
            '__y1': self.__y1,
            # The x2-coordinate of the line
            '__x2': self.__x2,
            # The y2-coordinate of the line
            '__y2': self.__y2,
            # The color of the line as an (R, G, B) tuple
            '__color': self.__color
        }

    @property
    def x1(self) -> float:
        """
        The x-coordinate of the first point of the line
        """
        return self.__x1

    @x1.setter
    def x1(self, v: float | int):
        self.__x1 = validate_coordinate("x1", v)
        self.update_data()

    @property
    def y1(self) -> float:
        """
        The y-coordinate of the first point of the line
        """
        return self.__y1

    @y1.setter
    def y1(self, v: float | int):
        self.__y1 = validate_coordinate("y1", v)
        self.update_data()

    @property
    def x2(self) -> float:
        """
        The x-coordinate of the second point of the line
        """
        return self.__x2

    @x2.setter
    def x2(self, v: float | int):
        self.__x2 = validate_coordinate("x2", v)
        self.update_data()

    @property
    def y2(self) -> float:
        """
        The y-coordinate of the second point of the line
        """
        return self.__y2

    @y2.setter
    def y2(self, v: float | int):
        self.__y2 = validate_coordinate("y2", v)
        self.update_data()

    @property
    def color(self) -> tuple[int, int, int]:
        """
        The color of the line as an (R, G, B) tuple
        """
        return self.__color

    @color.setter
    def color(self, v: tuple[int, int, int] | list[int]):
        self.__color = validate_color("color", v)
        self.update_data()
