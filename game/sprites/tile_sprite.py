from typing import Any
import arcade

from constants import TILE_SIZE, TILE_SCALING


class TileSprite(arcade.Sprite):
    REAL_TILE_SIZE = TILE_SIZE * TILE_SCALING

    def __init__(self, type: str, pos: list[int], **kwargs: Any) -> None:
        x, y = (
            TileSprite.REAL_TILE_SIZE * (pos[0] + 1 / 2),
            TileSprite.REAL_TILE_SIZE * (pos[1] + 1 / 2),
        )
        super().__init__(
            f"assets/tiles/{type}.png",
            scale=TILE_SCALING,
            center_x=int(x),
            center_y=int(y),
            **kwargs,
        )
