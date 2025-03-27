import pygame
import os
import sys

def process_player_sprites():
    """
    Process the player sprite sheets and save them as individual animation frames.
    This script is specific to the files you have:
    - player_idle.png
    - player_run.png
    """
    pygame.init()
    
    print("Processing player sprite sheets...")
    
    # Create directories if needed
    if not os.path.exists("assets"):
        os.makedirs("assets")
    if not os.path.exists("assets/player"):
        os.makedirs("assets/player")
    
    # Define sprite sheet paths
    sprite_sheets = {
        "idle": "player_idle.png",
        "run": "player_run.png"
    }
    
    # First check if the sprite sheets exist
    missing_files = []
    for action, filename in sprite_sheets.items():
        if not os.path.exists(filename):
            missing_files.append(filename)
    
    if missing_files:
        print(f"Error: Missing sprite sheets: {', '.join(missing_files)}")
        print("Please make sure these files are in the same directory as this script.")
        return
    
    # Process sprite sheets
    try:
        # Process idle animation
        idle_sheet = pygame.image.load(sprite_sheets["idle"])
        
        # Determine how many frames are in the sprite sheet
        # Assumes sprites are arranged horizontally and are equal width
        idle_sprite_width = idle_sheet.get_width() // 4  # Assuming 4 frames
        idle_sprite_height = idle_sheet.get_height()
        
        print(f"Idle sprite sheet dimensions: {idle_sheet.get_width()}x{idle_sheet.get_height()}")
        print(f"Detected sprite size: {idle_sprite_width}x{idle_sprite_height}")
        
        # Extract and save each idle frame
        for i in range(4):
            # Create a surface for the frame
            frame = pygame.Surface((idle_sprite_width, idle_sprite_height), pygame.SRCALPHA)
            
            # Copy the portion of the original image
            # Assumes sprites are arranged left-to-right
            frame.blit(idle_sheet, (0, 0), (i * idle_sprite_width, 0, idle_sprite_width, idle_sprite_height))
            
            # Save the frame (right facing)
            out_filename = f"assets/player/idle_right_{i}.png"
            pygame.image.save(frame, out_filename)
            print(f"Saved: {out_filename}")
            
            # Create and save left-facing version (flipped horizontally)
            flipped_frame = pygame.transform.flip(frame, True, False)
            out_filename = f"assets/player/idle_left_{i}.png"
            pygame.image.save(flipped_frame, out_filename)
            print(f"Saved: {out_filename}")
        
        # Process run animation
        run_sheet = pygame.image.load(sprite_sheets["run"])
        
        # Similar to idle, determine frame dimensions
        run_sprite_width = run_sheet.get_width() // 4  # Assuming 4 frames
        run_sprite_height = run_sheet.get_height()
        
        print(f"Run sprite sheet dimensions: {run_sheet.get_width()}x{run_sheet.get_height()}")
        print(f"Detected sprite size: {run_sprite_width}x{run_sprite_height}")
        
        # Extract and save each run frame
        for i in range(4):
            # Create a surface for the frame
            frame = pygame.Surface((run_sprite_width, run_sprite_height), pygame.SRCALPHA)
            
            # Copy the portion of the original image
            frame.blit(run_sheet, (0, 0), (i * run_sprite_width, 0, run_sprite_width, run_sprite_height))
            
            # Save the frame (right facing)
            out_filename = f"assets/player/walking_right_{i}.png"
            pygame.image.save(frame, out_filename)
            print(f"Saved: {out_filename}")
            
            # Create and save left-facing version (flipped horizontally)
            flipped_frame = pygame.transform.flip(frame, True, False)
            out_filename = f"assets/player/walking_left_{i}.png"
            pygame.image.save(flipped_frame, out_filename)
            print(f"Saved: {out_filename}")
        
        print("\nSprite processing complete!")
        print(f"All sprites saved to the assets/player directory")
        
    except Exception as e:
        print(f"Error processing sprite sheets: {e}")
        return

if __name__ == "__main__":
    process_player_sprites()
    pygame.quit()
    sys.exit()