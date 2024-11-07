from dataclasses import dataclass

# pylint: disable=no-member
import pyray as pr

# pylint: disable-next=unused-wildcard-import,wildcard-import
import variables as g
from server import kick_user

# create a dataclass for a point and a rectangle
# with integer values because pyray uses floats but doesn't support them...
@dataclass()
class IntPoint():
    """
    A dataclass for a point with integer values.
    """
    x: int
    y: int


@dataclass
class IntRectangle():
    """
    A dataclass for a rectangle with integer values.
    """
    x: int
    y: int
    width: int
    height: int


class Renderer():
    """
    This class is responsible for rendering the shapes on the window.
    """

    WINDOW_SIZE = IntPoint(800, 500)
    RENDER_AREA = IntRectangle(20, 20, 460, 460)

    def __init__(self):
        """
        Initializes a new Renderer object.

        :param shapes_data: A dictionary mapping shape UUIDs to dictionaries containing
            shape data.
        :param shapes_owner: A dictionary mapping client session IDs to sets of shape UUIDs.
        """

        self.__is_running = False
        self.__should_close = False

    def __draw(self):

        # I need to copy the data here because the dictionary can be modified during the loop because of concurrency
        # A shallow copy is sufficient because the data itself is never modified, only replaced with new data
        # Drawing shapes on the window can be long, so I don't want to lock for too long
        # TODO: see if just locking is faster or slower.

        with g.shapes_data_lock, g.usernames_lock:
            safe_shape_data = g.shapes_data.copy()
            safe_usernames = g.usernames.copy()

        pr.begin_drawing()
        pr.clear_background(
            # the need to add 2**32 is because pr.gui_get_style returns a uint32 and it isn't correctly cast to an int
            pr.get_color(2**32 + pr.gui_get_style(pr.GuiControl.DEFAULT, pr.GuiDefaultProperty.BACKGROUND_COLOR))
        )

        pr.draw_fps(20, 1)

        pr.begin_scissor_mode(self.RENDER_AREA.x, self.RENDER_AREA.y, self.RENDER_AREA.width, self.RENDER_AREA.height)

        pr.clear_background(pr.WHITE)

        # Draw the shapes
        for shape in safe_shape_data.values():
            shape_type, shape_data = shape
            if shape_type not in g.SUPPORTED_SHAPES:
                print(f"Invalid shape type: {shape_type}")
                # Do nothing for invalid shapes

            elif shape_type == "Rectangle":
                self.__draw_rectangle(shape_data, offset_x=self.RENDER_AREA.x, offset_y=self.RENDER_AREA.y)

            elif shape_type == "Ellipse":
                self.__draw_ellipse(shape_data, offset_x=self.RENDER_AREA.x, offset_y=self.RENDER_AREA.y)

            elif shape_type == "Line":
                self.__draw_line(shape_data, offset_x=self.RENDER_AREA.x, offset_y=self.RENDER_AREA.y)

        pr.end_scissor_mode()

        pr.draw_rectangle_lines(self.RENDER_AREA.x, self.RENDER_AREA.y, self.RENDER_AREA.width, self.RENDER_AREA.height, pr.BLACK)

        # Draw the usernames, sorted alphabetically
        pr.draw_text("Connected users :", 520, 20, 20, pr.BLACK)
        for i, sid_username_pair in enumerate(sorted(list(safe_usernames.items()), key=lambda x: x[1])):
            sid, username = sid_username_pair
            if pr.gui_button(pr.Rectangle(520, (i+2) * 25, 20, 20), f"#{pr.GuiIconName.ICON_EXIT}#"):
                kick_user(sid)

            pr.gui_label(pr.Rectangle(520+30, (i+2) * 25, 200, 20), username)

        pr.end_drawing()

    def __draw_rectangle(self, shape_data: dict, offset_x: int = 0, offset_y: int = 0):
        """
        Draws a rectangle on the window based on the given shape data.

        :param shape_data: A dictionary containing the shape data for the rectangle.
        """
        try:
            # Extract the data from the shape data dictionary
            x = int(shape_data["__x"]) + offset_x
            y = int(shape_data["__y"]) + offset_y
            width = int(shape_data["__width"])
            height = int(shape_data["__height"])
            color = pr.Color(*[int(i) for i in shape_data["__color"]], 255) # cast all values to int

            # Draw the rectangle
            pr.draw_rectangle(x, y, width, height, color)

        # pylint: disable=broad-except
        except Exception as e:
            # Print a message if the data is invalid
            print("Invalid shape data:", e)
            raise e

    def __draw_ellipse(self, shape_data: dict, offset_x: int = 0, offset_y: int = 0):
        """
        Draws an ellipse on the window based on the given shape data.

        :param shape_data: A dictionary containing the shape data for the ellipse.
        """
        try:
            # Extract the data from the shape data dictionary
            x = int(shape_data["__x"]) + offset_x
            y = int(shape_data["__y"]) + offset_y
            x_radius = float(shape_data["__x_radius"])
            y_radius = float(shape_data["__y_radius"])
            color = pr.Color(*[int(i) for i in shape_data["__color"]], 255) # cast all values to int

            # Draw the ellipse
            pr.draw_ellipse(x, y, x_radius, y_radius, color)

        # pylint: disable=broad-except
        except Exception as e:
            # Print a message if the data is invalid
            print("Invalid shape data:", e)
            raise e

    def __draw_line(self, shape_data: dict, offset_x: int = 0, offset_y: int = 0):
        """
        Draws an line on the window based on the given shape data.

        :param shape_data: A dictionary containing the shape data for the line.
        """
        try:
            # Extract the data from the shape data dictionary
            x1 = int(shape_data["__x1"]) + offset_x
            y1 = int(shape_data["__y1"]) + offset_y
            x2 = int(shape_data["__x2"]) + offset_x
            y2 = int(shape_data["__y2"]) + offset_y
            color = pr.Color(*[int(i) for i in shape_data["__color"]], 255) # cast all values to int

            # Draw the line
            pr.draw_line(x1, y1, x2, y2, color)

        # pylint: disable=broad-except
        except Exception as e:
            # Print a message if the data is invalid
            print("Invalid shape data:", e)
            raise e

    def run(self):
        """
        Main loop that continuously draws shapes until the window should close.
        """
        self.__is_running = True

        pr.init_window(self.WINDOW_SIZE.x, self.WINDOW_SIZE.y, "Makers Kids Connect")
        pr.set_target_fps(30)

        while not pr.window_should_close() and not self.__should_close:
            # Draw the shapes on the window
            self.__draw()

        pr.close_window()

    def stop(self):
        """
        Sets the flag to indicate that the rendering loop should stop
        and the Raylib window should be closed.
        """
        # Set the internal flag to signal the window to close
        self.__should_close = True

    def __del__(self):
        """
        Destructor for the Renderer class. Closes the Raylib window when the
        object is garbage collected.
        """
        if self.__is_running:
            pr.close_window()
