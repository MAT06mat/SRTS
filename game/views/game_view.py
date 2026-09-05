import arcade
import arcade.gl as gl

from sprites.tile_sprite import TileSprite
from sprites.entity_sprite import EntitySprite
from map_generation import TerrainGenerator
from constants import *


def get_rect_from_pos(p1: list[int], p2: list[int], mini=False):
    left = min(p1[0], p2[0])
    right = max(p1[0], p2[0])
    bottom = min(p1[1], p2[1])
    top = max(p1[1], p2[1])
    if mini:
        if left == right:
            right += 1
        if bottom == top:
            top += 1
    return arcade.LRBT(left, right, bottom, top)


class GameView(arcade.View):
    def __init__(self, window: arcade.Window | None = None) -> None:
        super().__init__(window)
        self.land_tiles = arcade.SpriteList(use_spatial_hash=True)
        self.mountain_tiles = arcade.SpriteList(use_spatial_hash=True)
        self.sea_tiles = arcade.SpriteList(use_spatial_hash=True)

        self.entity_sprites = arcade.SpriteList()
        self.selected_sprites: list[EntitySprite] = []

        self.camera = None
        self.press_pos: list[int] = None
        self.current_pos: list[int] = None

    def setup(self):
        self.window.background_color = arcade.csscolor.GRAY
        self.window.default_camera.use()

        self.camera = arcade.Camera2D()

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
                        f"Tile {type} is not in the layers of the {biome['name']}"
                    )
        print("End generation")

    def on_draw(self):
        """Draw this view"""
        self.clear()
        self.camera.use()
        self.land_tiles.draw(filter=gl.NEAREST)
        self.mountain_tiles.draw(filter=gl.NEAREST)
        self.sea_tiles.draw(filter=gl.NEAREST)
        self.entity_sprites.draw(filter=gl.NEAREST)

        for e in self.selected_sprites:
            e.draw_hit_box((0, 255, 0, 255))

        if self.press_pos:
            select_rect = get_rect_from_pos(self.press_pos, self.current_pos)
            arcade.draw_rect_outline(select_rect, (0, 255, 0, 255))

    def on_mouse_press(self, x, y, button, modifiers):
        if len(self.entity_sprites) == 0:
            print("Create one !")
            self.entity_sprites.append(EntitySprite(200, 300))
            self.entity_sprites.append(EntitySprite(400, 320))
            self.entity_sprites.append(EntitySprite(350, 240))
            self.entity_sprites.append(EntitySprite(120, 80))
        else:
            self.press_pos = (x, y)
            self.current_pos = (x, y)
        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.current_pos = (x, y)
        return super().on_mouse_drag(x, y, dx, dy, _buttons, _modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.press_pos:
            rect = get_rect_from_pos((x, y), self.press_pos, True)
            self.selected_sprites = arcade.get_sprites_in_rect(
                rect, self.entity_sprites
            )
            for e in self.selected_sprites:
                print(f"Entity avec {e.health} vie")
            self.press_pos = None
            self.current_pos = None

        return super().on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol in KEY_UP:
            self.camera.position = (self.camera.position.x, self.camera.position.y + 20)
        elif symbol in KEY_DOWN:
            self.camera.position = (self.camera.position.x, self.camera.position.y - 20)
        elif symbol in KEY_LEFT:
            self.camera.position = (self.camera.position.x - 20, self.camera.position.y)
        elif symbol in KEY_RIGHT:
            self.camera.position = (self.camera.position.x + 20, self.camera.position.y)
        return super().on_key_press(symbol, modifiers)
