import pygame
import sys
from game_states import MenuState, GameStateManager

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Fighters - Menu")

# Create clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Initialize the game state manager and set initial state to the menu
game_state_manager = GameStateManager()
game_state_manager.set_state(MenuState(game_state_manager, screen))

# Menu Loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Pass events to current state
        game_state_manager.handle_events(event)
    
    # Update current state
    game_state_manager.update()
    
    # Draw current state
    game_state_manager.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(FPS)

# Quit pygame when the game loop ends
pygame.quit()
sys.exit()
