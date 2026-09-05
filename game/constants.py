"""
Constant values for the game
"""

import arcade
from enum import Enum

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Simple RTS"
TILE_SCALING = 1.0
SPRITE_SIZE = 16

# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]

# Map tile ids
class Tile(Enum):
    WATER = 0
    GRASS = 1
    STONE = 2
    SAND = 3
    SNOW = 4
    