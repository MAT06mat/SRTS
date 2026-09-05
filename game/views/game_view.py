import arcade

from sprites.tile_sprite import TileSprite
from map_generation import TerrainGenerator
from constants import *


class GameView(arcade.View):
    def __init__(self, window: arcade.Window | None = None) -> None:
        super().__init__(window)
        self.land_tiles = arcade.SpriteList()
        self.mountain_tiles = arcade.SpriteList()
        self.sea_tiles = arcade.SpriteList()

        self.entity_sprites = arcade.SpriteList()

    def setup(self):
        self.window.background_color = arcade.csscolor.GRAY
        self.window.default_camera.use()

        print("Start generation")
        generator = TerrainGenerator(
            (SCREEN_HEIGHT // TILE_SIZE, SCREEN_WIDTH // TILE_SIZE), "plains"
        )
        grid = generator.generate()
        biome = generator.biome
        layers = biome["layers"]

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                type = Tile(grid[y, x]).name.lower()
                new_tile = TileSprite(type, [x, y])
                if type in layers["land"]:
                    self.land_tiles.append(new_tile)
                elif type in layers["mountain"]:
                    self.mountain_tiles.append(new_tile)
                elif type in layers["sea"]:
                    self.sea_tiles.append(new_tile)
                else:
                    raise Exception(
                        f"Tile {type} is not in the layers of the {biome["name"]}"
                    )
        print("End generation")

    def on_draw(self):
        """Draw this view"""
        self.clear()
        self.land_tiles.draw()
        self.mountain_tiles.draw()
        self.sea_tiles.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        pass

    def on_update(self, delta_time):
        pass
