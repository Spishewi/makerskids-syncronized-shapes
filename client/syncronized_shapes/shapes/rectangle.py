#pylint: disable-next=relative-beyond-top-level
from .abstract_shape import SyncronizedShape

class Rectangle(SyncronizedShape):
    def __init__(self, x: float, y: float, width: float, height: float, color: tuple[int, int, int]) -> None:
        """
        Initializes a rectangle with the given position, dimensions, and color.

        :param x: The x-coordinate of the rectangle
        :param y: The y-coordinate of the rectangle
        :param width: The width of the rectangle
        :param height: The height of the rectangle
        :param color: The color of the rectangle as an (R, G, B) tuple
        """
        # Set the x-coordinate of the rectangle
        self.__x = x
        # Set the y-coordinate of the rectangle
        self.__y = y
        # Set the width of the rectangle
        self.__width = width
        # Set the height of the rectangle
        self.__height = height
        # Set the color of the rectangle
        self.__color = color

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
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, v):
        self.__x = v
        self.update_data()
    
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, v):
        self.__y = v
        self.update_data()

    @property
    def width(self):
        return self.__width
    
    @width.setter
    def width(self, v):
        self.__width = v
        self.update_data()
    
    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, v):
        self.__height = v
        self.update_data()

    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, v):
        self.__color = v
        self.update_data()