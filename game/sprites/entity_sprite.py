from typing import Any

import arcade


class EntitySprite(arcade.Sprite):
    def __init__(
        self, center_x: int = 0, center_y: int = 0, health: int = 100, **kwargs: Any
    ) -> None:
        super().__init__(center_x=center_x, center_y=center_y, **kwargs)
        self.health = health
