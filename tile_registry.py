import os
import csv
import pygame

TILE_SIZE = 64
TILE_FOLDER = os.path.join("assets", "tiles")

def load_tile_registry():
    tile_registry = {}
    with open(os.path.join(TILE_FOLDER, "tiles.csv")) as f:
        reader = csv.DictReader(f)
        for row in reader:
            tile_type = row["type"]
            image_path = os.path.join(TILE_FOLDER, row["filename"])
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            tile_registry[tile_type] = {
                "image": image,
                "type": tile_type
            }
    return tile_registry
