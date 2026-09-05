from typing import Any
import arcade

from constants import Tile, TILE_SIZE


class TileSprite(arcade.Sprite):
    def __init__(self, id: int, pos: list[int], **kwargs: Any) -> None:
        x, y = TILE_SIZE * (pos[0] + 1 / 2), TILE_SIZE * (pos[1] + 1 / 2)
        super().__init__(
            f"assets/tiles/{Tile(id).name.lower()}.png",
            center_x=int(x),
            center_y=int(y),
            **kwargs,
        )
