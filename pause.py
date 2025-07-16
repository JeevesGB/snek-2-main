# pause.py
import pygame

def show_pause_menu():
    print("Game Paused")
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False
