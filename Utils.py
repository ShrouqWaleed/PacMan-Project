from Settings import *  
import heapq  

def get_neighbors(row, col, current_level_map):
    
    if current_level_map is None:
        print("Error: CURRENT_LEVEL_MAP is not set!")
        raise ValueError("CURRENT_LEVEL_MAP must be initialized before calling get_neighbors.")
    
    neighbors = []
    for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = row + drow, col + dcol
        if 0 <= nr < GRID_HEIGHT and 0 <= nc < GRID_WIDTH:
            if current_level_map[nr][nc] != 1:
                neighbors.append((nr, nc))
    return neighbors


def heuristic(a, b, p=1):
    """
    Calculates the Minkowski distance heuristic between two points.

                (|r1 - r2|^p + |c1 - c2|^p)^(1/p) 
            
    Args:
        a (tuple): The current position as (row, col).
        b (tuple): The target position as (row, col).
        p (int or float): The order of the distance. 
                          - p=1: Manhattan distance
                          - p=2: Euclidean distance
                          - p>2: Higher-order Minkowski distances

    Returns:
        float: Distance between the two points.
    """
    r1, c1 = a
    r2, c2 = b
    return (abs(r1 - r2) ** p + abs(c1 - c2) ** p) ** (1 / p) 

def a_star_search(start, goal, current_level_map):
    """
    A* algorithm

    Args:
        start (tuple): Starting position as (row, col).
        goal (tuple): Target position as (row, col).

    Returns:
        dict or None: A dictionary mapping each cell to its parent in the path.
                      If no path is found, returns None.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))  # Add the starting cell with priority 0

    # parent of each cell 
    came_from = {start: None}

    # Dictionary to store the cost of reaching each cell from the start
    g_score = {start: 0}

    while open_set: 
        _, current = heapq.heappop(open_set)  
        
        if current == goal:  
            return came_from

        # Explore each valid neighbor of the current cell
        for neighbor in get_neighbors(*current, current_level_map): # current (r, c)
            tentative_g = g_score[current] + 1  # Cost to reach neighbor from current cell

            # If this path to the neighbor is shorter or the neighbor hasn't been explored yet
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                
                g_score[neighbor] = tentative_g  # Update the cost to reach the neighbor
                f_score = tentative_g + heuristic(neighbor, goal, 1.6)  # Calculate total estimated cost
                
                heapq.heappush(open_set, (f_score, neighbor))  
                came_from[neighbor] = current  

    return None  

def reconstruct_path(came_from, start, goal):
    """
    Reconstructs the path from the start to the goal

    Args:
        came_from (dict): A dictionary mapping each cell to its parent.
        start (tuple): Starting position as (row, col).
        goal (tuple): Target position as (row, col).

    Returns:
        list: A list of cells representing the path from start to goal.
              If no path exists, returns an empty list.
    """
    if came_from is None:  
        return []  

    path = []  
    current = goal  # Start -> goal cell

    # backtrack from the goal to the start 
    while current is not None and current != start:
        path.append(current)  
        current = came_from[current]  # Move to the parent cell

    if current == start:  # If we reached the start cell
        path.append(start)  # Add the start cell to the path

    path.reverse()  # to get th correct order
    return path