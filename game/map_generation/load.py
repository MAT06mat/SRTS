import json

from constants import Tile


def load_biome_config(name: str) -> dict:
    """Loads a biome configuration from its name.

    :param str name: The name of the biome.
    :return dict: The biome configuration.
    """
    with open("assets/configs/biomes.json", "r") as f:
        biomes = json.load(f)
    b = biomes.get(name)
    if b is None:
        raise ValueError(f"Biome '{name}' not found in biomes.json")
    return b
