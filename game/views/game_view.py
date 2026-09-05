import arcade


class GameView(arcade.View):
    def __init__(
        self,
        window: arcade.Window | None = None,
        background_color: (
            tuple[int, int, int] | tuple[int, int, int, int] | None
        ) = None,
    ) -> None:
        super().__init__(window, background_color)
        self.coins = 10

    def setup(self):
        self.window.background_color = arcade.csscolor.GRAY
        self.window.default_camera.use()

    def on_draw(self):
        """Draw this view"""
        self.clear()
        arcade.draw_text(
            "Coins game !",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Your coins: {self.coins}",
            self.window.width / 2,
            self.window.height / 2 - 75,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )
        if self.coins <= 0:
            arcade.draw_text(
                "You lost the game",
                self.window.width / 2,
                self.window.height / 2 - 125,
                arcade.color.WHITE,
                font_size=20,
                anchor_x="center",
            )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.coins -= 1

    def on_update(self, delta_time):
        if self.coins <= 0:
            print("THE END")
