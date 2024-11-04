# pylint: disable=no-member
import pyray as pr

from globals import SUPPORTED_SHAPES

class Renderer():
    def __init__(self, shapes_data: dict[str, dict], shapes_owner: dict[str, set[str]], usernames: dict[str, str]):
        """
        Initializes a new Renderer object.

        :param shapes_data: A dictionary mapping shape UUIDs to dictionaries containing
            shape data.
        :param shapes_owner: A dictionary mapping client session IDs to sets of shape UUIDs.
        """

        self.__shapes_data = shapes_data
        self.__shapes_owner = shapes_owner
        self.__usernames = usernames

        self.__is_running = False
        self.__should_close = False

    def __draw(self):
        #TODO: because of concurrency problems, i'll have to make a lock system on theses variables
        safe_shape_data = self.__shapes_data
        safe_usernames = self.__usernames

        pr.begin_drawing()
        pr.clear_background(pr.GRAY)

        pr.begin_scissor_mode(0, 0, 500, 500)

        pr.clear_background(pr.WHITE)

        for shape in safe_shape_data.values():
            shape_type, shape_data = shape
            if shape_type not in SUPPORTED_SHAPES:
                print(f"Invalid shape type: {shape_type}")
                continue

            if shape_type == "Rectangle":
                self.__draw_rectangle(shape_data)

        pr.end_scissor_mode()

        pr.draw_text("Connected users :", 520, 20, 20, pr.BLACK)
        for i, username in enumerate(sorted(list(safe_usernames.values()))):
            pr.draw_text(username, 520, (i+2) * 20, 20, pr.BLUE)

        pr.end_drawing()

    def __draw_rectangle(self, shape_data: dict):
        try:
            x = int(shape_data["__x"])
            y = int(shape_data["__y"])
            width = int(shape_data["__width"])
            height = int(shape_data["__height"])
            color = pr.Color(*[int(i) for i in shape_data["__color"]], 255) # cast all values to int

            pr.draw_rectangle(x, y, width, height, color)

        # pylint: disable=broad-except
        except Exception as e:
            print("Invalid shape data:", e)
            raise e

    def run(self):
        """
        Main loop that continuously draws shapes until the window should close.
        """
        self.__is_running = True

        pr.init_window(800, 500, "Makers Kids Connect")
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
