import pygame
import random
import json
from level_manager import load_level_snkmap
from save_system import save_game, load_game

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
TILE_SIZE = 64

def start_game(level_path="saved_levels/level1.snkmap", load_saved=False):
    pygame.init()
    level_data, snake_start = load_level_snkmap(level_path)
    level_width = len(level_data[0]) * TILE_SIZE
    level_height = len(level_data) * TILE_SIZE
    screen = pygame.display.set_mode((level_width, level_height))
    clock = pygame.time.Clock()

    if load_saved:
        saved = load_game()
        if not saved:
            print("No save file found. Starting new game.")
            return start_game(level_path)

        level_path = saved["level"]
        snake = [pygame.Rect(x, y, 64, 64) for x, y in saved["snake"]]
        direction = tuple(saved["direction"])
        food_positions = [tuple(pos) for pos in saved["food"]]
        score = saved["score"]
    else:
        snake = [pygame.Rect(snake_start[0], snake_start[1], 64, 64)]
        direction = (64, 0)
        score = 0
        food_positions = []

        for y, row in enumerate(level_data):
            for x, tile in enumerate(row):
                if tile and tile["type"] == "food":
                    food_positions.append((x * 64, y * 64))

    level_data, _ = load_level_snkmap(level_path)
    paused = False
    running = True

    def respawn_food():
        while True:
            fx = random.randint(0, len(level_data[0]) - 1)
            fy = random.randint(0, len(level_data) - 1)
            tile = level_data[fy][fx]
            pos = (fx * 64, fy * 64)
            if tile and tile["type"] == "floor" and pos not in food_positions and pos not in [seg.topleft for seg in snake]:
                food_positions.append(pos)
                break

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction[1] == 0:
                    direction = (0, -64)
                elif event.key == pygame.K_DOWN and direction[1] == 0:
                    direction = (0, 64)
                elif event.key == pygame.K_LEFT and direction[0] == 0:
                    direction = (-64, 0)
                elif event.key == pygame.K_RIGHT and direction[0] == 0:
                    direction = (64, 0)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_s:  # Save state
                    save_game({
                        "level": level_path,
                        "snake": [list(seg.topleft) for seg in snake],
                        "direction": list(direction),
                        "score": score,
                        "food": [list(f) for f in food_positions]
                    })
                    print("Game saved.")

        if not paused and pygame.time.get_ticks() % 100 < 16:
            head = snake[0].copy()
            head.move_ip(direction)

            x_idx, y_idx = head.left // 64, head.top // 64
            if (x_idx < 0 or x_idx >= len(level_data[0]) or
                y_idx < 0 or y_idx >= len(level_data) or
                (level_data[y_idx][x_idx] and level_data[y_idx][x_idx]["type"] == "wall")):
                print("Hit wall")
                running = False

            if head.collidelist(snake) != -1:
                print("Hit self")
                running = False

            if head.topleft in food_positions:
                food_positions.remove(head.topleft)
                snake.insert(0, head)
                score += 1
                respawn_food()
            else:
                snake.insert(0, head)
                snake.pop()

        # Draw tiles
        for y, row in enumerate(level_data):
            for x, tile in enumerate(row):
                if tile:
                    screen.blit(tile["image"], (x * 64, y * 64))

        # Draw food
        food_tile = next((t for t in level_data[0] if t and t["type"] == "food"), None)
        if food_tile:
            for pos in food_positions:
                screen.blit(food_tile["image"], pos)

        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, (0, 255, 0), segment)

        if paused:
            font = pygame.font.SysFont(None, 60)
            text = font.render("Paused", True, (255, 255, 0))
            screen.blit(text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 30))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
