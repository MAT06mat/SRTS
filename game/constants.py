"""
Constant values for the game
"""

import arcade
from enum import Enum

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Simple RTS"
TILE_SCALING = 2.0
TILE_RESOLUTION = 16
MINIMAP_WIDTH = 256

# Calculated constants
TILE_SIZE = TILE_RESOLUTION * TILE_SCALING
SCREEN_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
MAP_GRID = [max(SCREEN_HEIGHT, SCREEN_WIDTH) // TILE_RESOLUTION] * 2
MAP_SIZE = [MAP_GRID[0] * TILE_SIZE, MAP_GRID[1] * TILE_SIZE]
MINIMAP_ZOOM = MAP_SIZE[0] / MINIMAP_WIDTH

# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]
RIGHT_CLICK = [arcade.MOUSE_BUTTON_RIGHT]
LEFT_CLICK = [arcade.MOUSE_BUTTON_LEFT]
MOUSE_CLICK = [arcade.MOUSE_BUTTON_MIDDLE]


# Map tile ids
class Tile(Enum):
    WATER = 0
    GRASS = 1
    STONE = 2
    SAND = 3
    SNOW = 4
