#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape
# pylint: disable-next=relative-beyond-top-level
from ..validators import validate_coordinate

class Line(SyncronizedShape):
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

        # Set the color of the line
        if not (isinstance(color, tuple) or isinstance(color, list)) or len(color) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            raise TypeError("Expected tuple or list of length 3 containing ints between 0 and 255, got " + str(color))
        self.__color = color

        # Initialize the parent SyncronizedShape class
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
        if not (isinstance(v, tuple) or isinstance(v, list)) or len(v) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in v):
            raise TypeError("Expected tuple or list of length 3 containing ints between 0 and 255, got " + str(v))
        self.__color = tuple(v)
        self.update_data()
