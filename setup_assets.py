"""
Asset setup utility for Zombie Fighters game

This script helps organize game assets by:
1. Creating necessary directories
2. Copying assets from source locations to the game directories
3. Processing sprite sheets if needed
"""

import os
import shutil
import sys
import pygame

def create_directories():
    """Create necessary directories for the game assets"""
    directories = [
        "assets",
        "assets/player",
        "assets/background",
        "assets/enemies",
        "assets/sounds"
    ]
    
    print("Creating asset directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  Created: {directory}")
        else:
            print(f"  Directory already exists: {directory}")

def copy_background_assets():
    """Copy background assets to the appropriate directory"""
    # List of background assets to look for
    background_assets = [
        "assetpack sky1.png",
        "assetpack sky2.png",
        "assetpack bg1.png",
        "assetpack bg2.png",
        "assetpack bg3.png",
        "assetpack smog large.png",
    ]
    
    print("\nCopying background assets...")
    
    # Count how many assets were found
    found_assets = 0
    
    # Check the current directory first
    for asset in background_assets:
        if os.path.exists(asset):
            dest_path = os.path.join("assets/background", asset)
            print(f"  Found: {asset}")
            print(f"  Copying to: {dest_path}")
            shutil.copy2(asset, dest_path)
            found_assets += 1
    
    # Check if we should also look in the "Zombie Asset Pack" directory
    if os.path.exists("Zombie Asset Pack"):
        print("\nChecking Zombie Asset Pack directory...")
        for root, _, files in os.walk("Zombie Asset Pack"):
            for file in files:
                if file in background_assets:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join("assets/background", file)
                    print(f"  Found: {src_path}")
                    print(f"  Copying to: {dest_path}")
                    shutil.copy2(src_path, dest_path)
                    found_assets += 1
    
    # Create symbolic links in the root directory to ensure the game can find them
    print("\nCreating symbolic links to assets...")
    for asset in background_assets:
        src_path = os.path.join("assets/background", asset)
        if os.path.exists(src_path) and not os.path.exists(asset):
            try:
                # On Windows use mklink, on Unix use symlink
                if sys.platform == 'win32':
                    os.system(f'mklink "{asset}" "{src_path}"')
                else:
                    os.symlink(src_path, asset)
                print(f"  Created link: {asset} -> {src_path}")
            except Exception as e:
                print(f"  Error creating link for {asset}: {e}")
                # Fallback to copying the file
                try:
                    shutil.copy2(src_path, asset)
                    print(f"  Fallback: Copied {src_path} to {asset}")
                except Exception as copy_error:
                    print(f"  Error copying {asset}: {copy_error}")
    
    if found_assets == 0:
        print("No background assets found. Please place background images in the game directory.")
    else:
        print(f"Found and processed {found_assets} background assets.")

def process_player_sprites():
    """Process player sprite sheets if they exist"""
    # Check for sprite sheets in the current directory
    sprite_sheets = {
        "idle": "player_idle.png",
        "run": "player_run.png"
    }
    
    # Check if the files exist
    print("\nChecking for player sprite sheets...")
    
    # First check in the current directory
    missing_files = []
    for action, filename in sprite_sheets.items():
        if not os.path.exists(filename):
            missing_files.append(filename)
    
    # If files are missing, check in "Zombie Asset Pack" directory
    if missing_files and os.path.exists("Zombie Asset Pack"):
        print("  Some sprite sheets not found in current directory.")
        print("  Checking Zombie Asset Pack directory...")
        
        for root, _, files in os.walk("Zombie Asset Pack"):
            for file in files:
                if file in missing_files:
                    src_path = os.path.join(root, file)
                    print(f"  Found: {src_path}")
                    print(f"  Copying to current directory")
                    shutil.copy2(src_path, file)
                    missing_files.remove(file)
    
    # Check again if we still have missing files
    for action, filename in sprite_sheets.items():
        if not os.path.exists(filename):
            print(f"  Missing sprite sheet: {filename}")
    
    # Process if we have the files
    if os.path.exists(sprite_sheets["idle"]) and os.path.exists(sprite_sheets["run"]):
        print("  Found all required sprite sheets. Processing...")
        pygame.init()
        
        # Process idle animation
        idle_sheet = pygame.image.load(sprite_sheets["idle"])
        
        # Determine how many frames are in the sprite sheet
        # Assumes sprites are arranged horizontally and are equal width
        idle_sprite_width = idle_sheet.get_width() // 4  # Assuming 4 frames
        idle_sprite_height = idle_sheet.get_height()
        
        print(f"  Idle sprite sheet dimensions: {idle_sheet.get_width()}x{idle_sheet.get_height()}")
        print(f"  Detected sprite size: {idle_sprite_width}x{idle_sprite_height}")
        
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
            print(f"  Saved: {out_filename}")
            
            # Create and save left-facing version (flipped horizontally)
            flipped_frame = pygame.transform.flip(frame, True, False)
            out_filename = f"assets/player/idle_left_{i}.png"
            pygame.image.save(flipped_frame, out_filename)
            print(f"  Saved: {out_filename}")
        
        # Process run animation
        run_sheet = pygame.image.load(sprite_sheets["run"])
        
        # Similar to idle, determine frame dimensions
        run_sprite_width = run_sheet.get_width() // 4  # Assuming 4 frames
        run_sprite_height = run_sheet.get_height()
        
        print(f"  Run sprite sheet dimensions: {run_sheet.get_width()}x{run_sheet.get_height()}")
        print(f"  Detected sprite size: {run_sprite_width}x{run_sprite_height}")
        
        # Extract and save each run frame
        for i in range(4):
            # Create a surface for the frame
            frame = pygame.Surface((run_sprite_width, run_sprite_height), pygame.SRCALPHA)
            
            # Copy the portion of the original image
            frame.blit(run_sheet, (0, 0), (i * run_sprite_width, 0, run_sprite_width, run_sprite_height))
            
            # Save the frame (right facing)
            out_filename = f"assets/player/walking_right_{i}.png"
            pygame.image.save(frame, out_filename)
            print(f"  Saved: {out_filename}")
            
            # Create and save left-facing version (flipped horizontally)
            flipped_frame = pygame.transform.flip(frame, True, False)
            out_filename = f"assets/player/walking_left_{i}.png"
            pygame.image.save(flipped_frame, out_filename)
            print(f"  Saved: {out_filename}")
            
        print("  Sprite processing complete!")
        pygame.quit()
    else:
        print("  Could not find all required sprite sheets. Player will use fallback rectangles.")

def main():
    """Main function to run the asset setup process"""
    print("==== Zombie Fighters - Asset Setup Utility ====")
    
    # Create required directories
    create_directories()
    
    # Process background assets
    copy_background_assets()
    
    # Process player sprites
    process_player_sprites()
    
    print("\n==== Asset Setup Complete ====")
    print("You can now run the game with: python main.py")

if __name__ == "__main__":
    main()