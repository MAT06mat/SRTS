import noise
import numpy as np
import random

from constants import Tile
from .load import load_biome_config
from .perlin_noise import generate_fractal_noise_2d


class TerrainGenerator:
    def __init__(self, shape: tuple[int, int], biome_name: str) -> None:
        self.shape = shape
        self.biome = load_biome_config(biome_name)

    def _get_tile_from_height(self, height: float) -> int:
        '''Returns the tile type based on the height value and the biome's tile thresholds.
        
        :param float height: The height value.
        :return int: The tile type (Tile enum value).
        '''
        n = len(self.biome["tiles"]) # The number of tile types in the biome
        for i, (tile, threshold) in enumerate(sorted(
            list(self.biome["tiles"].items()), key=lambda item: item[1]
        )):
            # If the height is less than the threshold or if it's the last tile type, return the tile type
            if height < threshold or i == n - 1:
                return Tile[tile.upper()].value

    def generate(self) -> np.ndarray:
        res: tuple[int, int] = tuple(self.biome["res"])
        octaves: int = self.biome["octaves"]
        persistence: float = self.biome["persistence"]
        lacunarity: int = self.biome["lacunarity"]
        k = lacunarity ** (octaves - 1)

        w = self.shape[0] if self.shape[0] % (k * res[0]) == 0 else self.shape[0] + (k * res[0] - self.shape[0] % (k * res[0]))
        h = self.shape[1] if self.shape[1] % (k * res[1]) == 0 else self.shape[1] + (k * res[1] - self.shape[1] % (k * res[1]))
        pnoise = generate_fractal_noise_2d(
            shape=(w, h),
            res=res,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
        )
        return np.vectorize(self._get_tile_from_height)(pnoise)[:self.shape[0], :self.shape[1]]
