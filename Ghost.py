import pygame
from Settings import *
from Utils import *
from collections import deque
class Ghost(pygame.sprite.Sprite):
    """
    Ghost that can either move on a predefined loop (static ghost)
    or chase Pac-Man using A* (dynamic ghost).
    """
    def __init__(self, row, col, tile_size, path_loop=None, dynamic=False, map=None):
        super().__init__()
        
        self.tile_size = tile_size
        self.row = row
        self.col = col
        self.dynamic = dynamic
        self.path_loop = path_loop or []
        self.loop_index = 0
        self.direction_forward = True
        self.map = map
        self.speed_counter = 0  # Controls speed for both static and dynamic ghosts
        
        # Load images
        if self.dynamic:
            self.original_image = pygame.image.load("png-clipart-red-pac-man-character-illustration-pacman-red-ghost-games-pac-man-thumbnail.png")
        else:
            self.original_image = pygame.image.load("png-transparent-pac-man-blue-ghost-illustration-pac-man-world-3-pong-video-game-pacman-blue-game-smiley-thumbnail.png")
        
        self.image = pygame.transform.scale(self.original_image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * tile_size, row * tile_size)
        
        # For dynamic ghost: store path to chase Pac-Man
        self.chase_path = deque()

    def update(self, current_map, pacman_pos):
        if self.dynamic:
            self._move_dynamic(current_map, pacman_pos)
        else:
            self._move_static()

    def _move_static(self):
        """
        Move along the predefined path loop at a slower speed.
        """
        if not self.path_loop:
            return
        
        self.speed_counter += 1
        if self.speed_counter < 5:  # Slow speed for static ghosts
            return
        self.speed_counter = 0

        # Calculate the next index
        next_index = self.loop_index + (1 if self.direction_forward else -1)
        next_index %= len(self.path_loop)  # Wrap around the loop if needed

        # Get the target cell
        target_row, target_col = self.path_loop[next_index]

        # Check if the target cell is not a wall
        if self.map[target_row][target_col] != 1:  # Not a wall
            self.row, self.col = target_row, target_col
            self.loop_index = next_index
            self.rect.topleft = (self.col * self.tile_size, self.row * self.tile_size)
        else:
            self.direction_forward = not self.direction_forward

    def _move_dynamic(self, level_map, pacman_pos):
        """
        Use A* to chase Pac-Man's current position.
        """
        self.speed_counter += 1
        if self.speed_counter < 3:  # Adjust to slow down dynamic ghost
            return
        self.speed_counter = 0

        if not self.chase_path:
            start = (self.row, self.col)
            came_from = a_star_search(start, pacman_pos, level_map)
            if came_from:
                path = reconstruct_path(came_from, start, pacman_pos)
                if len(path) > 1:
                    path.pop(0)
                self.chase_path = deque(path)
        else:
            next_cell = self.chase_path.popleft()
            self.row, self.col = next_cell
            self.rect.topleft = (self.col * self.tile_size, self.row * self.tile_size)

def check_collision(pacman, ghost):
    """
    Check collision using a reduced ghost rectangle for better accuracy.
    """
    # Shrink ghost rect slightly for finer collision detection
    ghost_rect = ghost.rect.inflate(-ghost.tile_size // 4, -ghost.tile_size // 4)
    return pacman.rect.colliderect(ghost_rect)
