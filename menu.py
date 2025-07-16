from game import start_game
from save_system import load_game
from settings import load_settings, save_settings
from level_editor import run_level_editor  # import editor function

def show_main_menu():
    import pygame
    pygame.init()
    settings = load_settings()
    screen = pygame.display.set_mode(settings["window_size"])
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    menu_items = ["Start New Game", "Load Game", "Level Editor", "Settings", "Quit"]  # added "Level Editor"
    selected = 0

    def draw_menu():
        screen.fill((10, 10, 10))
        for i, item in enumerate(menu_items):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = font.render(item, True, color)
            screen.blit(text, (screen.get_width() // 2 - 150, 200 + i * 80))
        pygame.display.flip()

    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    choice = menu_items[selected]
                    if choice == "Start New Game":
                        start_game(load_saved=False)
                    elif choice == "Load Game":
                        if load_game():
                            start_game(load_saved=True)
                        else:
                            print("No saved game found.")
                    elif choice == "Level Editor":
                        run_level_editor()  # Run your editor here
                    elif choice == "Settings":
                        show_settings_menu()
                    elif choice == "Quit":
                        pygame.quit()
                        return
        clock.tick(60)
