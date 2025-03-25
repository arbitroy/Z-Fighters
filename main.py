import pygame
import sys
import os
from game_states import GameStateManager
from settings import WIDTH, HEIGHT, FPS
# Initialize pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Fighters")

# Create clock for controlling frame rate
clock = pygame.time.Clock()

# Initialize the game state manager
game_manager = GameStateManager()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Pass events to game state manager
        game_manager.handle_events(event)
    
    # Update current state
    game_manager.update()
    
    # Draw current state
    game_manager.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()