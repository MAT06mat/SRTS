import noise
import numpy as np

from constants import Tile
from .load import load_biome_config


class TerrainGenerator:
    def __init__(self, shape: tuple[int, int], biome_name: str) -> None:
        self.shape = shape
        self.biome = load_biome_config(biome_name)

    def generate(self) -> np.ndarray:
        scale: float = self.biome["scale"]
        octaves: int = self.biome["octaves"]
        persistence: float = self.biome["persistence"]
        lacunarity: float = self.biome["lacunarity"]
        tiles: dict[str, float] = self.biome["tiles"]

        terrain = np.zeros(self.shape, dtype=np.int8)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                x, y = i / scale, j / scale
                noise_value = noise.pnoise2(
                    x,
                    y,
                    octaves,
                    persistence,
                    lacunarity,
                    repeatx=self.shape[0],
                    repeaty=self.shape[1],
                    base=0,
                )
                for tile, threshold in sorted(
                    list(tiles.items()), key=lambda item: item[1]
                ):
                    if noise_value < threshold:
                        terrain[i][j] = Tile[tile.upper()].value
                        break

        return terrain
