import arcade
import arcade.gl as gl

from sprites.tile_sprite import TileSprite
from sprites.entity_sprite import EntitySprite
from map_generation import TerrainGenerator
from constants import *

MAP_SIZE = [max(SCREEN_HEIGHT, SCREEN_WIDTH) // TILE_SIZE] * 2


def get_rect_from_pos(p1: list[int], p2: list[int], cam_p: list[int], mini=False):
    left = min(p1[0], p2[0]) + cam_p[0]
    right = max(p1[0], p2[0]) + cam_p[0]
    bottom = min(p1[1], p2[1]) + cam_p[1]
    top = max(p1[1], p2[1]) + cam_p[1]
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
        self.key_pressed = []

        self.camera = None
        self.camera_gui = None
        self.press_pos: list[int] | None = None
        self.current_pos: list[int] | None = None

        self.minimap_sprite_list = None
        self.minimap_texture = None
        self.minimap_sprite = None

    def setup(self):
        self.window.background_color = arcade.csscolor.GRAY
        self.window.default_camera.use()

        self.camera = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()

        generator = TerrainGenerator(MAP_SIZE, "plains")
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

        self.minimap_texture = arcade.Texture.create_empty("MiniMap", (256, 256))
        self.minimap_sprite = arcade.Sprite(
            self.minimap_texture,
            center_x=128,
            center_y=self.height - 128,
        )

        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

    def update_minimap(self):
        map_width = TileSprite.REAL_TILE_SIZE * MAP_SIZE[0]
        map_height = TileSprite.REAL_TILE_SIZE * MAP_SIZE[1]
        proj = (0, map_width, 0, map_height)
        atlas = self.minimap_sprite_list.atlas
        cam_bl = self.camera.bottom_left
        cam_tr = self.camera.top_right

        with atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear()
            self.land_tiles.draw()
            self.mountain_tiles.draw()
            self.sea_tiles.draw()
            rect = arcade.LRBT(cam_bl[0], cam_tr[0], cam_bl[1], cam_tr[1])
            arcade.draw_rect_outline(rect, (0, 255, 0), 10)

    def on_draw(self):
        """Draw this view"""
        self.clear()
        with self.camera.activate():
            self.land_tiles.draw(filter=gl.NEAREST)
            self.mountain_tiles.draw(filter=gl.NEAREST)
            self.sea_tiles.draw(filter=gl.NEAREST)
            self.entity_sprites.draw(filter=gl.NEAREST)

            for e in self.selected_sprites:
                e.draw_hit_box((0, 255, 0, 255))

            if self.press_pos:
                select_rect = get_rect_from_pos(
                    self.press_pos, self.current_pos, self.camera.bottom_left
                )
                arcade.draw_rect_outline(select_rect, (0, 255, 0, 255))

        with self.camera_gui.activate():
            self.update_minimap()
            self.minimap_sprite_list.draw()

    def on_update(self, delta_time):
        for key in self.key_pressed:
            if key in KEY_UP:
                self.camera.position = (
                    self.camera.position.x,
                    self.camera.position.y + TileSprite.REAL_TILE_SIZE,
                )
            elif key in KEY_DOWN:
                self.camera.position = (
                    self.camera.position.x,
                    self.camera.position.y - TileSprite.REAL_TILE_SIZE,
                )
            elif key in KEY_LEFT:
                self.camera.position = (
                    self.camera.position.x - TileSprite.REAL_TILE_SIZE,
                    self.camera.position.y,
                )
            elif key in KEY_RIGHT:
                self.camera.position = (
                    self.camera.position.x + TileSprite.REAL_TILE_SIZE,
                    self.camera.position.y,
                )
        return super().on_update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        if button in LEFT_CLICK and self.minimap_sprite.rect.point_in_rect((x, y)):
            px = (
                (x - self.minimap_sprite.rect[0])
                / 256
                * MAP_SIZE[0]
                * TileSprite.REAL_TILE_SIZE
            )
            py = (
                (y - self.minimap_sprite.rect[2])
                / 256
                * MAP_SIZE[1]
                * TileSprite.REAL_TILE_SIZE
            )
            self.camera.position = (px, py)
            return super().on_mouse_press(x, y, button, modifiers)
        if len(self.entity_sprites) == 0:
            self.entity_sprites.append(EntitySprite(192, 304))
            self.entity_sprites.append(EntitySprite(400, 320))
            self.entity_sprites.append(EntitySprite(352, 240))
            self.entity_sprites.append(EntitySprite(128, 80))
        else:
            self.press_pos = (x, y)
            self.current_pos = (x, y)
        return super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.current_pos = (x, y)
        return super().on_mouse_drag(x, y, dx, dy, _buttons, _modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        # Entity selection
        if self.press_pos:
            rect = get_rect_from_pos(
                (x, y), self.press_pos, self.camera.bottom_left, True
            )
            self.selected_sprites = arcade.get_sprites_in_rect(
                rect, self.entity_sprites
            )
            for e in self.selected_sprites:
                print(f"Entity avec {e.health} vie")
            self.press_pos = None
            self.current_pos = None

        return super().on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        self.key_pressed.append(symbol)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.key_pressed:
            self.key_pressed.remove(symbol)
        return super().on_key_release(symbol, modifiers)

    def on_resize(self, width: int, height: int):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        super().on_resize(width, height)
        self.camera.match_window(aspect=SCREEN_WIDTH / SCREEN_HEIGHT, projection=False)
        self.camera_gui.match_window(
            aspect=SCREEN_WIDTH / SCREEN_HEIGHT, projection=False
        )
