from typing import Any
import arcade

from constants import TILE_SIZE, TILE_SCALING


class TileSprite(arcade.Sprite):
    def __init__(self, type: str, pos: list[int], **kwargs: Any) -> None:
        x, y = (
            TILE_SIZE * (pos[0] + 1 / 2),
            TILE_SIZE * (pos[1] + 1 / 2),
        )
        super().__init__(
            f":tiles:{type}.png",
            scale=TILE_SCALING,
            center_x=int(x),
            center_y=int(y),
            **kwargs,
        )
