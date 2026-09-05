import arcade

from sprites.tile_sprite import TileSprite


class GameView(arcade.View):
    def __init__(self, window: arcade.Window | None = None) -> None:
        super().__init__(window)
        self.tiles = arcade.SpriteList()

    def setup(self):
        self.window.background_color = arcade.csscolor.GRAY
        self.window.default_camera.use()

        grid = [[0, 0, 1, 2, 3], [0, 4, 2, 1, 1], [0, 1, 2, 1, 3], [1, 1, 2, 3, 0]]

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                new_tile = TileSprite(grid[y][x], [x, y])
                self.tiles.append(new_tile)

    def on_draw(self):
        """Draw this view"""
        self.clear()
        self.tiles.draw()
        arcade.draw_text(
            "Coins game !",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass

    def on_update(self, delta_time):
        pass
