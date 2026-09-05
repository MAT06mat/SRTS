import arcade
from .game_view import GameView


class MenuView(arcade.View):
    def setup(self):
        self.window.background_color = arcade.csscolor.BURLYWOOD
        self.window.default_camera.use()

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Main menu",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to start",
            self.window.width / 2,
            self.window.height / 2 - 75,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """If the user presses the mouse button, start the game."""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
