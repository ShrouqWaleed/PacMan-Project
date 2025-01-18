import pygame
from GameLogic import *
from Menu import *

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT))
    pygame.display.set_caption("Pac-Man")

    while True:
        auto_mode = main_menu(screen)
        if auto_mode is None:
            pygame.quit()
            sys.exit()

        chosen_level = map_selection_menu(screen) 
        
        if chosen_level is None:
            continue

        run_game(screen, auto_mode, chosen_level)

if __name__ == "__main__":
    main()