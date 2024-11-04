#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape

class Line(SyncronizedShape):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, color: tuple[int, int, int]) -> None:
        """
        Initializes a line with the given position, dimensions, and color.

        :param x1: The x1-coordinate of the line
        :param y1: The y1-coordinate of the line
        :param x2: The x2-coordinate of the line
        :param y2: The y2-coordinate of the line
        :param color: The color of the line as an (R, G, B) tuple
        """
        # Set the x1-coordinate of the line
        self.__x1 = x1
        # Set the y1-coordinate of the line
        self.__y1 = y1
        # Set the x2-coordinate of the line
        self.__x2 = x2
        # Set the y2-coordinate of the line
        self.__y2 = y2
        # Set the color of the line
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
    def x1(self):
        return self.__x1

    @x1.setter
    def x1(self, v):
        self.__x1 = v
        self.update_data()

    @property
    def y1(self):
        return self.__y1

    @y1.setter
    def y1(self, v):
        self.__y1 = v
        self.update_data()

    @property
    def x2(self):
        return self.__x2

    @x2.setter
    def x2(self, v):
        self.__x2 = v
        self.update_data()

    @property
    def y2(self):
        return self.__y2

    @y2.setter
    def y2(self, v):
        self.__y2 = v
        self.update_data()

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, v):
        self.__color = v
        self.update_data()
