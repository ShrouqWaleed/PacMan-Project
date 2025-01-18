import pygame
from Settings import *
import sys

def map_selection_menu(screen):
   
    font = pygame.font.SysFont(None, 36)  
    clock = pygame.time.Clock()  

    map1_button = pygame.Rect(50, 120, 300, 40)   # (x, y, width, height)
    map2_button = pygame.Rect(50, 180, 300, 40)
    map3_button = pygame.Rect(50, 240, 300, 40)
    back_button = pygame.Rect(50, 300, 300, 40)

    while True:
        screen.fill(BLACK)  

        # Render menu text
        title_text = font.render("Select a Map", True, WHITE)
        map1_text = font.render("Map 1", True, WHITE)
        map2_text = font.render("Map 2", True, WHITE)
        map3_text = font.render("Map 3", True, WHITE)
        back_text = font.render("Back to Main Menu", True, WHITE)

        # Add text for buttons
        screen.blit(title_text, (50, 50))
        screen.blit(map1_text, (map1_button.x + 10, map1_button.y + 5))
        screen.blit(map2_text, (map2_button.x + 10, map2_button.y + 5))
        screen.blit(map3_text, (map3_button.x + 10, map3_button.y + 5))
        screen.blit(back_text, (back_button.x + 10, back_button.y + 5))

        # Draw buttons 
        pygame.draw.rect(screen, BLUE, map1_button, 2)
        pygame.draw.rect(screen, BLUE, map2_button, 2)
        pygame.draw.rect(screen, BLUE, map3_button, 2)
        pygame.draw.rect(screen, BLUE, back_button, 2)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  
                mouse_pos = event.pos  
                if map1_button.collidepoint(mouse_pos):  # Map 1 selected
                    return LEVEL_MAP_1
                elif map2_button.collidepoint(mouse_pos):  # Map 2 selected
                    return LEVEL_MAP_2
                elif map3_button.collidepoint(mouse_pos):  # Map 3 selected
                    return LEVEL_MAP_3
                elif back_button.collidepoint(mouse_pos):  
                    return None  # Return to main menu


def main_menu(screen):
    # Initialize Pygame Mixer for sound and music
    pygame.mixer.init()  # mixer da object ms2ol 3n ay 7aga liha 3laka blsot fy pygame
    
    # Load and play background music
    pygame.mixer.music.load("playing-pac-man-6783.mp3")  # hatla2o file mp3 fy el project ana mdy music.load el path bta3 el sound w hwa haish8lo
    pygame.mixer.music.set_volume(0.9)  
    pygame.mixer.music.play(-1) # play -1 dy 3l4an lma el sound y5ls y3ido tany bs keda da kol el sound lw 3aizin t add ay sound effect haikon keda 

    # Load the background image
    background_image = pygame.image.load("pacman-mtbcc-header-mobile (1).jpg")  # fy el swr el mwdo3 abst bkteer hia function tdiha path el sora 5las hia keda 3mlt a7la read w gahza
    background_image = pygame.transform.scale(background_image, screen.get_size())  

    font = pygame.font.SysFont(None, 36)  # Set up font for menu text
    clock = pygame.time.Clock()  # Set up clock for controlling FPS

    auto_button = pygame.Rect(50, 120, 200, 40)   # (x, y, width, height)
    manual_button = pygame.Rect(50, 160, 200, 40)
    quit_button = pygame.Rect(50, 200, 200, 40)

    while True:
        screen.blit(background_image, (0, 0)) # hena enta bt7ot 3ala el screen bta3t pygame el sora el enta 3aizha fy el 7ala dy hia sort pacman el fy el folder

        # Render menu text
        title_text = font.render("Pac-Man Menu", True, WHITE)
        auto_text = font.render("Auto Mode", True, WHITE)
        manual_text = font.render("Manual Mode", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)

        # Add text for buttons
        screen.blit(title_text, (50, 50))
        screen.blit(auto_text, (auto_button.x + 10, auto_button.y + 5))
        screen.blit(manual_text, (manual_button.x + 10, manual_button.y + 5))
        screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 5))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop music when quitting
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
                mouse_pos = event.pos  # Get mouse position
                if auto_button.collidepoint(mouse_pos):  # Auto Mode selected
                    pygame.mixer.music.stop()  # Stop music before starting the game
                    return True   
                elif manual_button.collidepoint(mouse_pos):  # Manual Mode selected
                    pygame.mixer.music.stop()  # Stop music before starting the game
                    return False  
                elif quit_button.collidepoint(mouse_pos):  # Quit selected
                    pygame.mixer.music.stop()  # Stop music when quitting
                    pygame.quit()
                    sys.exit()


# da test lw 7d 7abb ygrb el main menu

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((640, 480))
#     pygame.display.set_caption("Pac-Man")

#     while True:
#         # Display the main menu
#         auto_mode = main_menu(screen)
#         if auto_mode is None:
#             continue  # Go back to the main menu

#         # Display the map selection menu
#         selected_map = map_selection_menu(screen)
#         if selected_map is None:
#             continue  # Go back to the main menu

#         # Set the CURRENT_LEVEL_MAP
#         global CURRENT_LEVEL_MAP
#         CURRENT_LEVEL_MAP = selected_map

#         # At this point, you can proceed to the game loop with the selected map and mode
#         print(f"Selected Mode: {'Auto' if auto_mode else 'Manual'}")
#         print(f"Selected Map: {CURRENT_LEVEL_MAP}")


# if __name__ == "__main__":
#     main()
