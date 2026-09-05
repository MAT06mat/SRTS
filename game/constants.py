"""
Constant values for the game
"""

import arcade
from enum import Enum

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Simple RTS"
TILE_SCALING = 2.0
TILE_SIZE = 16

# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]

CAMERA_WIDTH = 512
CAMERA_HEIGHT = 288


# Map tile ids
class Tile(Enum):
    WATER = 0
    GRASS = 1
    STONE = 2
    SAND = 3
    SNOW = 4
