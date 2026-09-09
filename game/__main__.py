import arcade, arcade.resources as res
from pathlib import Path

from constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from views.menu_view import MenuView


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.views = {}

        res.add_resource_handle("entities", Path("assets/entities").resolve())
        res.add_resource_handle("tiles", Path("assets/tiles").resolve())


def main():
    """Main method"""
    window = MyWindow()
    window.center_window()
    start_view = MenuView(window)
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
