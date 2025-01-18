import pygame 
from Settings import *
from Utils import *
from collections import deque


class Pacman(pygame.sprite.Sprite):
    """
    Pac-Man character. Handles both manual and auto movement.
    """
    def __init__(self, row, col, tile_size, auto_mode):
        super().__init__()

        self.original_image = pygame.image.load("pngtree-scary-pacman-character-game-ghost-png-image_5172925.png")
        self.image = pygame.transform.scale(self.original_image, (tile_size, tile_size))
        
        
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col
        self.tile_size = tile_size
        self.auto_mode = auto_mode

        # For auto-mode path following:
        self.current_path = deque()
    
    def update(self, level_map):
        """
        Update Pac-Man's position each frame.
        - If auto_mode: follow the path from A* to the next target pellet.
        - If manual_mode: rely on keyboard events to move.
        """
        if self.auto_mode:
            self._auto_move(level_map)
        # Else, do nothing here because manual movement is done via events.

        # Update the actual pixel position of Pac-Man based on row, col
        self.rect.topleft = (self.col * self.tile_size, self.row * self.tile_size)

    def move(self, direction, level_map):
        """
        For manual mode: attempt to move Pac-Man if there's no wall.
        direction is one of: (dx, dy) e.g., (0,1) for right, (0,-1) for left, etc.
        """
        drow, dcol = direction
        new_row = self.row + drow
        new_col = self.col + dcol

        # Check boundaries and walls
        if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH:
            if level_map[new_row][new_col] != 1:  # Not a wall
                self.row = new_row
                self.col = new_col

    def _auto_move(self, level_map):
        """
        Move Pac-Man automatically along the current path (if any).
        If path is empty, compute a path to the next pellet or do nothing if no pellets are left.
        """
        if not self.current_path:
            # Find the next closest pellet
            next_pellet = self._find_closest_pellet(level_map)
            if next_pellet is None:
                return  # No pellets left
            
            # Use A* to get a path to that pellet
            start = (self.row, self.col)
            came_from = a_star_search(start, next_pellet, level_map)
            if came_from:
                full_path = reconstruct_path(came_from, start, next_pellet)
                # we remove the first cell in the path (it's the current position)
                if len(full_path) > 1:
                    full_path.pop(0)
                self.current_path = deque(full_path)
        else:
            # Follow the existing path
            next_cell = self.current_path.popleft()
            self.row, self.col = next_cell

    def _find_closest_pellet(self, level_map):
        """
        Find the nearest pellet to Pac-Man's current position using BFS or simple iteration.
        Returns the cell coordinates (row,col) of that pellet or None if none left.
        """
        start = (self.row, self.col)
        min_dist = float('inf')
        closest_pellet = None

        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                if level_map[r][c] == 2:  # This is a pellet
                    # Manhattan distance
                    dist = abs(r - self.row) + abs(c - self.col)
                    if dist < min_dist:
                        min_dist = dist
                        closest_pellet = (r, c)
        return closest_pellet
