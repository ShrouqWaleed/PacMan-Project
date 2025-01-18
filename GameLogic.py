import pygame 
from Settings import *
from Utils import *
from Pacman import Pacman
from Ghost import *
import sys

def run_game(screen, auto_mode, chosen_map):
    """
    Runs the main Pac-Man game on the selected map with either auto or manual mode.
    """
    print(f"Setting CURRENT_LEVEL_MAP to: {chosen_map}")
    CURRENT_LEVEL_MAP = chosen_map  # Assign chosen map to global variable
    print(f"CURRENT_LEVEL_MAP set successfully: {CURRENT_LEVEL_MAP}")# One of LEVEL_MAP_1, LEVEL_MAP_2, LEVEL_MAP_3

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    # -----------------------------
    # 1) CREATE PACMAN
    #    Start somewhere that is not a wall. For example: row=1, col=1
    # -----------------------------
    pacman = Pacman(row=1, col=1, tile_size=TILE_SIZE, auto_mode=auto_mode)
    all_sprites.add(pacman)

    # -----------------------------
    # 2) CREATE GHOSTS
    #    4 static ghosts + 1 dynamic ghost
    # -----------------------------
    # Example static ghosts with simple loops:
    static_paths = [
        [(1, 18), (2, 18), (2, 17), (1, 17)],    # small square loop
        [(10,10), (10,11), (11,11), (11,10)],    # another small square
        [(5,5),   (5,6),   (6,6),   (6,5)],      # etc.
        [(15,15), (15,16), (16,16), (16,15)]
    ]

    ghost_static_1 = Ghost(1, 18, TILE_SIZE, path_loop=static_paths[0], dynamic=False, map=CURRENT_LEVEL_MAP)
    ghost_static_2 = Ghost(10,10, TILE_SIZE, path_loop=static_paths[1], dynamic=False, map=CURRENT_LEVEL_MAP)
    ghost_static_3 = Ghost(5, 5,  TILE_SIZE, path_loop=static_paths[2], dynamic=False, map=CURRENT_LEVEL_MAP)
    ghost_static_4 = Ghost(15,15, TILE_SIZE, path_loop=static_paths[3], dynamic=False, map=CURRENT_LEVEL_MAP)

    all_sprites.add(ghost_static_1, ghost_static_2, ghost_static_3, ghost_static_4)

    # The dynamic ghost
    # Place it somewhere on the map that is not a wall
    ghost_dynamic = Ghost(18, 1, TILE_SIZE, path_loop=None, dynamic=True)
    all_sprites.add(ghost_dynamic)

    # -----------------------------
    # Main Game Loop
    # -----------------------------
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle manual mode continuous movement
        if not auto_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                pacman.move((-1, 0), CURRENT_LEVEL_MAP)
            elif keys[pygame.K_DOWN]:
                pacman.move((1, 0), CURRENT_LEVEL_MAP)
            elif keys[pygame.K_LEFT]:
                pacman.move((0, -1), CURRENT_LEVEL_MAP)
            elif keys[pygame.K_RIGHT]:
                pacman.move((0, 1), CURRENT_LEVEL_MAP)


        # 1) Update Pac-Man and Ghosts
        pacman.update(CURRENT_LEVEL_MAP)
        ghost_static_1.update(CURRENT_LEVEL_MAP, (pacman.row, pacman.col))
        ghost_static_2.update(CURRENT_LEVEL_MAP, (pacman.row, pacman.col))
        ghost_static_3.update(CURRENT_LEVEL_MAP, (pacman.row, pacman.col))
        ghost_static_4.update(CURRENT_LEVEL_MAP, (pacman.row, pacman.col))
        ghost_dynamic.update(CURRENT_LEVEL_MAP, (pacman.row, pacman.col))

        # 2) Check collisions with Ghost → if collision, game over
        for ghost in [ghost_static_1, ghost_static_2, ghost_static_3, ghost_static_4, ghost_dynamic]:
            if check_collision(pacman, ghost):
                print("Game Over! Pac-Man was caught by a ghost.")
                running = False
                break 
        # Collision check in the main loop

        # 3) Check if Pac-Man ate a pellet
        r, c = pacman.row, pacman.col
        if CURRENT_LEVEL_MAP[r][c] == 2:  # 2 means pellet
            CURRENT_LEVEL_MAP[r][c] = 0   # Eat it -> make it empty cell

        # 4) Check if all pellets are collected -> win condition
        if all_pellets_collected(CURRENT_LEVEL_MAP):
            print("You win! All pellets collected.")
            running = False
            break

        # 5) Draw everything
        screen.fill(BLACK)
        draw_level_map(screen, CURRENT_LEVEL_MAP, TILE_SIZE)
        all_sprites.draw(screen)
        pygame.display.flip()

    # End of game loop
    # Could show a "Play Again?" or return to main menu, etc.
    pygame.time.wait(2000)  # Wait 2 seconds before returning
    return

def all_pellets_collected(level_map):
    """
    Check if there are any '2' left in the map.
    """
    for row in level_map:
        if 2 in row:
            return False
    return True


def draw_level_map(screen, level_map, tile_size):
    """
    Draw walls, pellets, etc. based on the current level map.
    """
    for r in range(len(level_map)):
        for c in range(len(level_map[0])):
            cell = level_map[r][c]
            x = c * tile_size
            y = r * tile_size

            if cell == 1:
                # Wall
                pygame.draw.rect(screen, BLUE, (x, y, tile_size, tile_size))
            elif cell == 2:
                # Pellet
                center = (x + tile_size//2, y + tile_size//2)
                pygame.draw.circle(screen, WHITE, center, tile_size//6)
            # 0 -> empty, do nothing
