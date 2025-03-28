import pygame
import sys
import os
from settings import WIDTH, HEIGHT, FPS
from debug import add_debug, log_to_file

# Add startup diagnostics
def run_diagnostics():
    """Run startup diagnostics to check for sprite files and background assets"""
    add_debug("=== STARTUP DIAGNOSTICS ===")
    
    # Check for player sprites
    if os.path.exists("assets"):
        add_debug("Assets directory exists")
        
        # Check for player directory
        if os.path.exists("assets/player"):
            add_debug("Player assets directory exists")
            
            # List files in player directory
            try:
                files = os.listdir("assets/player")
                add_debug(f"Found {len(files)} files in assets/player/")
                
                # Look for specific sprite patterns
                idle_right = [f for f in files if f.startswith("idle_right_")]
                walking_right = [f for f in files if f.startswith("walking_right_")]
                idle_left = [f for f in files if f.startswith("idle_left_")]
                walking_left = [f for f in files if f.startswith("walking_left_")]
                
                add_debug(f"Idle right sprites: {len(idle_right)}")
                add_debug(f"Walking right sprites: {len(walking_right)}")
                add_debug(f"Idle left sprites: {len(idle_left)}")
                add_debug(f"Walking left sprites: {len(walking_left)}")
                
                # List all files for reference
                for file in files:
                    add_debug(f"  Found: {file}")
            except Exception as e:
                add_debug(f"Error listing files: {e}")
        else:
            add_debug("Player assets directory MISSING")
    else:
        add_debug("Assets directory MISSING")
    
    # Check for background assets
    background_assets = [
        "assetpack sky1.png",
        "assetpack sky2.png",
        "assetpack bg1.png",
        "assetpack bg2.png",
        "assetpack bg3.png",
        "assetpack smog large.png",
    ]
    
    # Check in the root directory
    add_debug("Checking for background assets in root directory...")
    for asset in background_assets:
        if os.path.exists(asset):
            add_debug(f"  Found: {asset}")
        else:
            add_debug(f"  Missing: {asset}")
    
    # Check in the assets/background directory
    add_debug("Checking for background assets in assets/background directory...")
    for asset in background_assets:
        asset_path = os.path.join("assets", "background", asset)
        if os.path.exists(asset_path):
            add_debug(f"  Found: {asset_path}")
        else:
            add_debug(f"  Missing: {asset_path}")
    
    add_debug("=== END DIAGNOSTICS ===")

def main():
    # Initialize pygame
    pygame.init()
    
    # Run diagnostics before creating the game window
    run_diagnostics()
    
    # Create the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zombie Fighters")
    
    # Only import game_states after pygame display is initialized
    from game_states import GameStateManager
    
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
    
    # Log game closing
    add_debug("Game closing")
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()