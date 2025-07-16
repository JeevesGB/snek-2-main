import pygame
import json
import os
import time
import tkinter as tk
from tkinter import simpledialog, messagebox

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
GRID_WIDTH, GRID_HEIGHT = 16, 12
TILE_SIZE = 64
SIDEBAR_WIDTH = 256

TILE_TYPES = {
    "wall": "assets/tiles/wall.png",
    "floor": "assets/tiles/floor.png",
    "food": "assets/tiles/food.png",
    "powerup": "assets/tiles/powerup.png",
    "enemy": "assets/tiles/enemy.png",
    "snake_start": "assets/tiles/snake_start.png",
    "empty": None
}

def load_sprite(path):
    if path and os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    return None

def prompt_filename():
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Save Level", "Enter filename (without extension):")
    root.destroy()
    return name

def confirm_quit():
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno("Exit to Menu", "Return to main menu?")
    root.destroy()
    return result

def run_level_editor():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Level Editor")

    SPRITES = {key: load_sprite(path) for key, path in TILE_TYPES.items()}
    font = pygame.font.SysFont(None, 24)

    grid = [["floor" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    snake_start_pos = None
    selected_tile = "wall"
    tile_keys = list(TILE_TYPES.keys())

    clock = pygame.time.Clock()
    running = True

    save_message = ""
    save_message_time = 0

    def draw_grid():
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile_type = grid[y][x]
                sprite = SPRITES.get(tile_type)
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if sprite:
                    screen.blit(sprite, pos)
                else:
                    pygame.draw.rect(screen, (30, 30, 30), (*pos, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, (50, 50, 50), (*pos, TILE_SIZE, TILE_SIZE), 1)

    def draw_sidebar():
        pygame.draw.rect(screen, (40, 40, 40), (SCREEN_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        y_offset = 20
        for tile_type in tile_keys:
            x = SCREEN_WIDTH - SIDEBAR_WIDTH + 20
            sprite = SPRITES.get(tile_type)
            tile_rect = pygame.Rect(x, y_offset, TILE_SIZE, TILE_SIZE)

            if sprite:
                screen.blit(sprite, (x, y_offset))
            else:
                pygame.draw.rect(screen, (100, 100, 100), tile_rect)

            text_surf = font.render(tile_type.capitalize(), True, (255, 255, 255))
            screen.blit(text_surf, (x + TILE_SIZE + 10, y_offset + TILE_SIZE // 4))

            if tile_type == selected_tile:
                pygame.draw.rect(screen, (255, 255, 0), tile_rect.inflate(4, 4), 3)

            y_offset += TILE_SIZE + 20

        help_texts = [
            "S = Save",
            "ESC = Quit",
            "Q / E = Cycle Tile",
            "Click = Place Tile"
        ]
        for i, text in enumerate(help_texts):
            hint = font.render(text, True, (180, 180, 180))
            screen.blit(hint, (SCREEN_WIDTH - SIDEBAR_WIDTH + 10, SCREEN_HEIGHT - 100 + i * 20))

        if save_message and time.time() - save_message_time < 2:
            msg_surf = font.render(save_message, True, (0, 255, 0))
            screen.blit(msg_surf, (SCREEN_WIDTH // 2 - msg_surf.get_width() // 2, SCREEN_HEIGHT - 30))

    def save_level():
        nonlocal save_message, save_message_time
        filename = prompt_filename()
        if not filename:
            return
        full_path = os.path.join("saved_levels", f"{filename}.snkmap")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        tile_data = {
            "tiles": grid,
            "snake_start": list(snake_start_pos) if snake_start_pos else None
        }

        with open(full_path, "w") as f:
            json.dump(tile_data, f, indent=2)

        save_message = f"Saved as {filename}.snkmap"
        save_message_time = time.time()
        print(f"Level saved to {full_path}")

    while running:
        screen.fill((20, 20, 20))
        draw_grid()
        draw_sidebar()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if mx < GRID_WIDTH * TILE_SIZE and my < GRID_HEIGHT * TILE_SIZE:
                    grid_x = mx // TILE_SIZE
                    grid_y = my // TILE_SIZE

                    if selected_tile == "snake_start":
                        if snake_start_pos:
                            old_x, old_y = snake_start_pos
                            if grid[old_y][old_x] == "snake_start":
                                grid[old_y][old_x] = "floor"
                        snake_start_pos = (grid_x, grid_y)

                    grid[grid_y][grid_x] = selected_tile

                elif mx > SCREEN_WIDTH - SIDEBAR_WIDTH:
                    y_offset = 20
                    for tile_type in tile_keys:
                        x = SCREEN_WIDTH - SIDEBAR_WIDTH + 20
                        tile_rect = pygame.Rect(x, y_offset, TILE_SIZE, TILE_SIZE)
                        if tile_rect.collidepoint(mx, my):
                            selected_tile = tile_type
                            break
                        y_offset += TILE_SIZE + 20

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_level()
                elif event.key == pygame.K_q:
                    idx = tile_keys.index(selected_tile)
                    selected_tile = tile_keys[(idx - 1) % len(tile_keys)]
                elif event.key == pygame.K_e:
                    idx = tile_keys.index(selected_tile)
                    selected_tile = tile_keys[(idx + 1) % len(tile_keys)]
                elif event.key == pygame.K_ESCAPE:
                    if confirm_quit():
                        return

        pygame.display.flip()
        clock.tick(60)

    return

# Run the editor
if __name__ == "__main__":
    run_level_editor()
