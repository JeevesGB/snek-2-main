import pygame
import os
import json

# Sprite paths (64x64 PNGs)
SPRITE_PATHS = {
    "wall": "assets/tiles/wall.png",
    "floor": "assets/tiles/floor.png",
    "food": "assets/tiles/food.png",
    "powerup": "assets/tiles/powerup.png",
    "enemy": "assets/tiles/enemy.png",
    "snake_start": "assets/tiles/snake_start.png"
}

_sprite_cache = {}

def load_sprite(name):
    """Load and cache a sprite image."""
    if name in _sprite_cache:
        return _sprite_cache[name]
    path = SPRITE_PATHS.get(name)
    if not path or not os.path.exists(path):
        print(f"Warning: Missing sprite file for '{name}' at {path}")
        return None
    image = pygame.image.load(path).convert_alpha()
    _sprite_cache[name] = image
    return image

def load_level_snkmap(json_path):
    """
    Load level from a .snkmap JSON file and return a 2D tile grid + snake start position.
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    grid_data = data["tiles"]
    snake_start = tuple(data["snake_start"]) if data.get("snake_start") else None

    sprites = {key: load_sprite(key) for key in SPRITE_PATHS}

    tiles = []
    for y, row in enumerate(grid_data):
        row_tiles = []
        for x, tile_type in enumerate(row):
            if tile_type in sprites:
                img = sprites[tile_type]
                if tile_type == "snake_start":
                    tile_type = "floor"  # Replace snake_start with floor
                row_tiles.append({"type": tile_type, "image": img})
            else:
                row_tiles.append(None)
        tiles.append(row_tiles)

    if snake_start is None:
        raise ValueError(f"Error: Snake start not defined in {json_path}")

    # Convert from tile coordinates to pixels
    return tiles, (snake_start[0] * 64, snake_start[1] * 64)
